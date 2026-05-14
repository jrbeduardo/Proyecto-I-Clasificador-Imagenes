# Frontends Generados por IA (Vibe Coding)

Las carpetas observadas en el proyecto:

- [frontend_gemimi_cli](./frontend_gemimi_cli) 
- [frontend_gemini](./frontend_gemini)

contienen interfaces gráficas básicas diseñadas para consumir la API de clasificación de comida. 

Estos frontends fueron creados utilizando la metodología de **Vibe Coding**, es decir, desarrollados íntegramente mediante instrucciones en lenguaje natural dirigidas a una Inteligencia Artificial, sin escribir el código manualmente.

## Características de los Frontends

- **Vanilla Web:** Creados exclusivamente con HTML5, CSS3 y JavaScript puro.
- **Sin Frameworks:** No utilizan React, Vue, Angular, Bootstrap ni librerías externas (cero red tape).
- **Responsive:** Diseño adaptable a dispositivos móviles y escritorio.
- **Integración API:** Configurados para usar `fetch` y `FormData` apuntando al backend en Python (FastAPI).

## Prompt Utilizado (Ejemplo Base)

El siguiente prompt fue la directriz principal que la IA utilizó para maquetar la estructura completa (HTML, CSS, JS):

```text
Quiero que generes un frontend basico, sin frameworks, para consumir una API de clasificacion de comida. Debe estar hecho solo con HTML, CSS y JavaScript vanilla. 

Contexto de la API: 
- Base URL configurable en una constante llamada API_URL, por defecto http://127.0.0.1:8000 
- Endpoint GET /health para verificar estado 
- Endpoint POST /predict que recibe multipart/form-data con el campo file (imagen) 

Si todo sale bien, /predict responde JSON con esta forma aproximada: 
- top1: { class_id, class_name, probability } 
- topk: arreglo de 5 elementos con { class_id, class_name, probability } 
- recommendation: { title, summary, ingredients: [], nutrition: { calories_kcal, protein_g, carbs_g, fat_g, health_assessment }, recommendation } 
- filename, device, model_path 

Si hay error, responde con detail 

Requisitos de interfaz: 
- Titulo y descripcion corta. 
- Boton para probar conexion con /health y mostrar resultado. 
- Input para subir imagen, con vista previa. 
- Boton Enviar para llamar /predict. 
- Estado de carga mientras procesa. 
- Manejo de errores legible para el usuario. 
- Mostrar resultado: Prediccion principal (nombre y probabilidad en porcentaje), Lista top 5, Recomendacion nutricional completa (title, summary, ingredients, nutrition, recommendation) 
- Diseno limpio y simple, responsive, sin librerias externas. 

Requisitos tecnicos: 
- Entrega 3 archivos separados: index.html, styles.css y app.js. 
- Usa fetch + FormData. 
- Valida que el archivo exista y sea imagen antes de enviar. 
- Convierte probabilidades a porcentaje con 2 decimales. 
- Comenta brevemente las partes importantes del JS. 
- No uses React, Vue, Bootstrap ni dependencias externas. 

Entrega final: Devuelveme el contenido completo de los 3 archivos, en secciones separadas y claramente rotuladas.
```
