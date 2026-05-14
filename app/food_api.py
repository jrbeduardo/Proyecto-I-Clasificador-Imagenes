import io
import json
import os
from contextlib import asynccontextmanager
from typing import AsyncIterator, List

import timm
import torch
import torch.nn.functional as F
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from PIL import Image, UnidentifiedImageError
from torchvision import transforms

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "vit_b16_food101_finetuned.pth")
MODEL_PATH = os.getenv("FOOD_MODEL_PATH", DEFAULT_MODEL_PATH)
MODEL_ARCH = os.getenv("FOOD_MODEL_ARCH", "vit_base_patch16_224.augreg_in21k_ft_in1k")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def gemini_recommend_simple(food_name: str, topk: list) -> dict:
    if not GEMINI_API_KEY:
        return {
            "title": f"Recomendacion para {food_name}",
            "summary": "GEMINI_API_KEY no configurada.",
            "ingredients": [],
            "nutrition": {
                "calories_kcal": "N/D",
                "protein_g": "N/D",
                "carbs_g": "N/D",
                "fat_g": "N/D",
                "health_assessment": "No se pudo evaluar.",
            },
            "recommendation": "Configura GEMINI_API_KEY para habilitar recomendaciones.",
        }

    top5_str = "\n".join(
        f"{i+1}. {p['class_name']} ({p['probability']*100:.1f}%)" for i, p in enumerate(topk)
    )
    prompt = (
        f"El modelo de clasificacion de comida identifico la imagen como '{food_name}'.\n"
        f"Las 5 predicciones mas probables fueron:\n{top5_str}\n\n"
        "Responde UNICAMENTE en JSON valido (sin markdown, sin comentarios) con esta estructura exacta:\n"
        "{\n"
        "  \"title\": \"...\",\n"
        "  \"summary\": \"...\",\n"
        "  \"ingredients\": [\"...\", \"...\"],\n"
        "  \"nutrition\": {\n"
        "    \"calories_kcal\": \"...\",\n"
        "    \"protein_g\": \"...\",\n"
        "    \"carbs_g\": \"...\",\n"
        "    \"fat_g\": \"...\",\n"
        "    \"health_assessment\": \"...\"\n"
        "  },\n"
        "  \"recommendation\": \"...\"\n"
        "}\n"
        "Todo en espanol, conciso y claro para interfaz web."
    )

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    text = (response.text or "").strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            text = "\n".join(lines[1:-1]).strip()

    try:
        data = json.loads(text)
        return {
            "title": data.get("title", f"Recomendacion para {food_name}"),
            "summary": data.get("summary", ""),
            "ingredients": data.get("ingredients", []),
            "nutrition": {
                "calories_kcal": data.get("nutrition", {}).get("calories_kcal", "N/D"),
                "protein_g": data.get("nutrition", {}).get("protein_g", "N/D"),
                "carbs_g": data.get("nutrition", {}).get("carbs_g", "N/D"),
                "fat_g": data.get("nutrition", {}).get("fat_g", "N/D"),
                "health_assessment": data.get("nutrition", {}).get("health_assessment", "N/D"),
            },
            "recommendation": data.get("recommendation", ""),
        }
    except json.JSONDecodeError:
        return {
            "title": f"Recomendacion para {food_name}",
            "summary": text,
            "ingredients": [],
            "nutrition": {
                "calories_kcal": "N/D",
                "protein_g": "N/D",
                "carbs_g": "N/D",
                "fat_g": "N/D",
                "health_assessment": "No se pudo estructurar la respuesta automaticamente.",
            },
            "recommendation": text,
        }


def build_eval_transform() -> transforms.Compose:
    return transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ]
    )


class FoodModelService:
    def __init__(self, model_path: str) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = model_path
        self.model = None
        self.classes: List[str] = []
        self.eval_tf = build_eval_transform()

    def load(self) -> None:
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Checkpoint no encontrado en {self.model_path}. "
                "Configura FOOD_MODEL_PATH correctamente."
            )

        ckpt = torch.load(self.model_path, map_location="cpu", weights_only=False)
        if not isinstance(ckpt, dict) or "model_state_dict" not in ckpt:
            raise ValueError("Checkpoint invalido. Se espera model_state_dict y metadata.")

        state_dict = ckpt["model_state_dict"]
        num_classes = int(ckpt.get("num_classes", 101))
        arch = ckpt.get("arch", MODEL_ARCH)
        classes = ckpt.get("classes", [])

        self.model = timm.create_model(arch, pretrained=False, num_classes=num_classes)
        self.model.load_state_dict(state_dict)
        self.model = self.model.to(self.device).eval()

        if not isinstance(classes, list) or len(classes) != num_classes:
            raise ValueError("Classes faltantes o con tamano incorrecto en el checkpoint.")
        self.classes = classes

    def predict_topk(self, image_bytes: bytes, topk: int = 5) -> dict:
        if self.model is None:
            raise RuntimeError("Modelo no cargado.")

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except UnidentifiedImageError as exc:
            raise ValueError("Archivo de imagen invalido.") from exc

        x = self.eval_tf(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            probs = F.softmax(self.model(x), dim=1)[0]

        top_probs, top_idx = torch.topk(probs, k=topk)
        topk_preds = []
        for idx, prob in zip(top_idx.tolist(), top_probs.tolist()):
            topk_preds.append(
                {
                    "class_id": idx,
                    "class_name": self.classes[idx].replace("_", " "),
                    "probability": float(prob),
                }
            )

        return {
            "top1": topk_preds[0],
            "topk": topk_preds,
            "device": str(self.device),
            "model_path": self.model_path,
        }


service = FoodModelService(MODEL_PATH)
model_load_error: str | None = None


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Carga el modelo una sola vez al iniciar la API.
    global model_load_error
    try:
        service.load()
        model_load_error = None
    except Exception as exc:
        model_load_error = str(exc)
    yield


app = FastAPI(title="Food-101 ViT API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    # Estado rapido para verificar API, modelo y configuracion base.
    return {
        "status": "ok",
        "model_loaded": service.model is not None,
        "model_load_error": model_load_error,
        "num_classes": len(service.classes),
        "device": str(service.device),
        "gemini_enabled": bool(GEMINI_API_KEY),
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> dict:
    global model_load_error

    # Reintenta cargar en caliente si el modelo no quedo listo en el arranque.
    if service.model is None:
        try:
            service.load()
            model_load_error = None
        except Exception as exc:
            model_load_error = str(exc)
            raise HTTPException(status_code=503, detail=f"Modelo no disponible: {model_load_error}") from exc

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Debes subir una imagen.")

    try:
        image_bytes = await file.read()
        result = service.predict_topk(image_bytes, topk=5)
        result["recommendation"] = gemini_recommend_simple(result["top1"]["class_name"], result["topk"])
        result["filename"] = file.filename
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error de prediccion: {exc}") from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("food_api:app", host="0.0.0.0", port=8000, reload=True)
