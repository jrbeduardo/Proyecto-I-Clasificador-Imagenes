FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para Pillow y torch
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements-food-api.txt .
RUN pip install --no-cache-dir -r requirements-food-api.txt

# Copiar el codigo de la API
COPY food_api.py .

# Copiar el modelo
COPY models/vit_b16_food101_finetuned.pth models/vit_b16_food101_finetuned.pth

EXPOSE 8000

CMD ["uvicorn", "food_api:app", "--host", "0.0.0.0", "--port", "8000"]
