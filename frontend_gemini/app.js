// Configuración global
const API_URL = "http://127.0.0.1:8000";

// Elementos del DOM
const fileInput = document.getElementById('file-input');
const dropZone = document.getElementById('drop-zone');
const previewImg = document.getElementById('preview-img');
const dropText = document.getElementById('drop-text');
const btnPredict = document.getElementById('btn-predict');
const btnHealth = document.getElementById('btn-health');
const healthResult = document.getElementById('health-result');
const loader = document.getElementById('loader');
const errorMsg = document.getElementById('error-message');
const resultsContent = document.getElementById('results-content');

/** * Lógica de conexión con /health 
 */
btnHealth.addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        healthResult.textContent = `Estado: Conectado (${data.status || 'OK'})`;
        healthResult.style.background = "#2ecc71";
    } catch (err) {
        healthResult.textContent = "Estado: Error de conexión";
        healthResult.style.background = "#e74c3c";
    }
});

/**
 * Gestión de la imagen y vista previa
 */
dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            previewImg.classList.remove('hidden');
            dropText.classList.add('hidden');
            btnPredict.disabled = false;
        };
        reader.readAsDataURL(file);
    } else {
        alert("Por favor, selecciona un archivo de imagen válido.");
    }
});

/**
 * Función principal para llamar a /predict
 */
btnPredict.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) return;

    // Resetear UI
    errorMsg.classList.add('hidden');
    resultsContent.classList.add('hidden');
    loader.classList.remove('hidden');
    btnPredict.disabled = true;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Error en el servidor");
        }

        displayResults(data);

    } catch (err) {
        errorMsg.textContent = `Error: ${err.message}`;
        errorMsg.classList.remove('hidden');
    } finally {
        loader.classList.add('hidden');
        btnPredict.disabled = false;
    }
});

/**
 * Renderiza los datos en la interfaz
 */
function displayResults(data) {
    resultsContent.classList.remove('hidden');

    // 1. Predicción Principal
    const top = data.top1;
    const probPct = (top.probability * 100).toFixed(2);
    document.getElementById('top-prediction').innerHTML = 
        `${top.class_name} <span style="float:right">${probPct}%</span>`;

    // 2. Top K
    const topkList = document.getElementById('topk-list');
    topkList.innerHTML = '';
    data.topk.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `<span>${item.class_name}</span> 
                        <span>${(item.probability * 100).toFixed(2)}%</span>`;
        topkList.appendChild(li);
    });

    // 3. Recomendación Nutricional
    const rec = data.recommendation;
    const nut = rec.nutrition;

    document.getElementById('rec-title').textContent = rec.title;
    document.getElementById('rec-summary').textContent = rec.summary;
    document.getElementById('rec-text').textContent = rec.recommendation;
    
    document.getElementById('nut-cal').textContent = `${nut.calories_kcal} kcal`;
    document.getElementById('nut-prot').textContent = `${nut.protein_g} g`;
    document.getElementById('nut-carb').textContent = `${nut.carbs_g} g`;
    document.getElementById('nut-fat').textContent = `${nut.fat_g} g`;
    document.getElementById('nut-health').textContent = nut.health_assessment;

    // Lista de ingredientes
    const ingList = document.getElementById('rec-ingredients');
    ingList.innerHTML = '';
    rec.ingredients.forEach(ing => {
        const li = document.createElement('li');
        li.textContent = ing;
        ingList.appendChild(li);
    });
}