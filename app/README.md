# Food-101 API

API REST para clasificar imágenes de comida usando el modelo ViT-B/16 fine-tuned en Food-101 (101 clases, ~91.8% top-1).

## Estructura

```
app/
├── food_api.py                        # Código de la API (FastAPI)
├── requirements-food-api.txt          # Dependencias Python
├── Dockerfile                         # Imagen Docker
└── models/
    └── vit_b16_food101_finetuned.pth  # Checkpoint del modelo
```

## Correr localmente

```bash
pip install -r requirements-food-api.txt
uvicorn food_api:app --reload
```

## Correr con Docker

```bash
docker build -t food-api .
docker run -p 8000:8000 food-api
```

## Endpoints

| Método | Ruta       | Descripción                          |
|--------|------------|--------------------------------------|
| GET    | `/health`  | Estado del servidor y modelo cargado |
| POST   | `/predict` | Clasifica una imagen (multipart/form-data, campo `file`) |
| GET    | `/docs`    | Documentación interactiva (Swagger)  |

## Ejemplo con curl

```bash
curl -X POST "http://localhost:8000/predict" \
     -F "file=@mi_comida.jpg"
```

Respuesta:
```json
{
  "top1": {"class_id": 57, "class_name": "pizza", "probability": 0.94},
  "topk": [...],
  "filename": "mi_comida.jpg"
}
```
