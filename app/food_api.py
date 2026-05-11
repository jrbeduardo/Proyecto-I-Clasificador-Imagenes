import io
import json
import os
from typing import List

import timm
import torch
import torch.nn.functional as F
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from PIL import Image, UnidentifiedImageError
from torchvision import transforms

# Cargar variables de entorno desde .env (si existe)
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Configurable paths and model metadata
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "vit_b16_food101_finetuned.pth")
MODEL_PATH = os.getenv("FOOD_MODEL_PATH", DEFAULT_MODEL_PATH)
MODEL_ARCH = os.getenv("FOOD_MODEL_ARCH", "vit_base_patch16_224.augreg_in21k_ft_in1k")

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


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
                "Checkpoint not found. "
                f"Expected at: {self.model_path}. "
                "Set FOOD_MODEL_PATH to the correct .pth file."
            )

        ckpt = torch.load(self.model_path, map_location="cpu", weights_only=False)

        # Support both metadata-rich checkpoints and raw state_dict checkpoints.
        if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
            state_dict = ckpt["model_state_dict"]
            num_classes = int(ckpt.get("num_classes", 101))
            arch = ckpt.get("arch", MODEL_ARCH)
            classes = ckpt.get("classes")
        elif isinstance(ckpt, dict):
            state_dict = ckpt
            num_classes = 101
            arch = MODEL_ARCH
            classes = None
        else:
            raise ValueError("Unsupported checkpoint format.")

        self.model = timm.create_model(arch, pretrained=False, num_classes=num_classes)
        self.model.load_state_dict(state_dict)
        self.model = self.model.to(self.device).eval()

        if classes and isinstance(classes, list):
            self.classes = classes
        else:
            self.classes = self._load_food101_classes()

        if len(self.classes) != num_classes:
            raise ValueError(
                f"Class count mismatch: checkpoint expects {num_classes}, "
                f"but classes list has {len(self.classes)} entries."
            )

    @staticmethod
    def _load_food101_classes() -> List[str]:
        from torchvision.datasets import Food101

        dataset = Food101(root="./data", split="train", download=False)
        return dataset.classes

    def predict_topk(self, image_bytes: bytes, topk: int = 5) -> dict:
        if self.model is None:
            raise RuntimeError("Model is not loaded.")

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except UnidentifiedImageError as exc:
            raise ValueError("Invalid image file.") from exc

        x = self.eval_tf(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(x)
            probs = F.softmax(logits, dim=1)[0]

        top_probs, top_idx = torch.topk(probs, k=topk)

        predictions = []
        for idx, prob in zip(top_idx.tolist(), top_probs.tolist()):
            predictions.append(
                {
                    "class_id": idx,
                    "class_name": self.classes[idx].replace("_", " "),
                    "probability": float(prob),
                }
            )

        return {
            "top1": predictions[0],
            "topk": predictions,
            "model_path": self.model_path,
            "device": str(self.device),
        }


def _gemini_recommend(food_name: str, top5: list) -> str:
    """Llama a Gemini para generar una recomendacion estructurada basada en la prediccion."""
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
            "recommendation": "Configura GEMINI_API_KEY para habilitar recomendaciones con IA.",
        }

    top5_str = "\n".join(
        f"  {i+1}. {p['class_name']} ({p['probability']*100:.1f}%)"
        for i, p in enumerate(top5)
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
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    text = (response.text or "").strip()

    # Si Gemini devuelve bloque markdown, extraer el JSON interno.
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            text = "\n".join(lines[1:-1]).strip()

    try:
        parsed = json.loads(text)
        return {
            "title": parsed.get("title", f"Recomendacion para {food_name}"),
            "summary": parsed.get("summary", ""),
            "ingredients": parsed.get("ingredients", []),
            "nutrition": {
                "calories_kcal": parsed.get("nutrition", {}).get("calories_kcal", "N/D"),
                "protein_g": parsed.get("nutrition", {}).get("protein_g", "N/D"),
                "carbs_g": parsed.get("nutrition", {}).get("carbs_g", "N/D"),
                "fat_g": parsed.get("nutrition", {}).get("fat_g", "N/D"),
                "health_assessment": parsed.get("nutrition", {}).get("health_assessment", "N/D"),
            },
            "recommendation": parsed.get("recommendation", ""),
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


app = FastAPI(
    title="Food-101 ViT-B/16 API",
    description="API for Food-101 inference using a fine-tuned ViT-B/16 checkpoint.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = FoodModelService(MODEL_PATH)


@app.on_event("startup")
def startup_event() -> None:
    service.load()


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "model_loaded": service.model is not None,
        "num_classes": len(service.classes),
        "model_path": service.model_path,
        "device": str(service.device),
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> dict:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upload must be an image file.")

    try:
        image_bytes = await file.read()
        result = service.predict_topk(image_bytes=image_bytes, topk=5)
        result["filename"] = file.filename
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction error: {exc}") from exc


@app.get("/models")
def list_models() -> dict:
    """Lista los modelos de Gemini disponibles para esta API key."""
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY no configurada.")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        models = [
            {"name": m.name, "supported_actions": m.supported_actions}
            for m in client.models.list()
        ]
        return {"models": models}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/recommend")
async def recommend(file: UploadFile = File(...)) -> dict:
    """Clasifica la imagen y devuelve una recomendacion generada por Gemini."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upload must be an image file.")

    try:
        image_bytes = await file.read()
        prediction = service.predict_topk(image_bytes=image_bytes, topk=5)
        food_name = prediction["top1"]["class_name"]
        recommendation = _gemini_recommend(food_name, prediction["topk"])
        return {
            "filename": file.filename,
            "top1": prediction["top1"],
            "topk": prediction["topk"],
            "recommendation": recommendation,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {exc}") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("food_api:app", host="0.0.0.0", port=8000, reload=True)
