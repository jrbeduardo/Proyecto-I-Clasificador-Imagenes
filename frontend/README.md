# Frontend React (fronnend)

Aplicacion React para consumir la API de clasificacion de comida.

## Funcionalidades

- Subir imagen de comida.
- Ver vista previa de la imagen.
- Enviar la imagen al endpoint `/recommend`.
- Mostrar prediccion principal, top-5 y recomendacion.

## Configuracion

1. Copia `.env.example` a `.env`.
2. Ajusta `VITE_API_URL` si tu API corre en otra URL.

Ejemplo:

```
VITE_API_URL=http://127.0.0.1:8000
```

## Ejecutar

```
npm install
npm run dev
```

Abre el navegador en `http://localhost:5173`.
