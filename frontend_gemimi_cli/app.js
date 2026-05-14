// Constante de configuración (URL Base de la API)
const API_URL = 'http://127.0.0.1:8000';

// Elementos del DOM
const btnHealth = document.getElementById('btn-health');
const healthStatus = document.getElementById('health-status');

const fileInput = document.getElementById('file-input');
const imagePreview = document.getElementById('image-preview');
const btnPredict = document.getElementById('btn-predict');

const loader = document.getElementById('loader');
const errorMsg = document.getElementById('error-msg');
const resultsSection = document.getElementById('results-section');

// Elementos de resultados
const top1Result = document.getElementById('top1-result');
const topkList = document.getElementById('topk-list');
const recTitle = document.getElementById('rec-title');
const recSummary = document.getElementById('rec-summary');
const nutCal = document.getElementById('nut-cal');
const nutProt = document.getElementById('nut-prot');
const nutCarb = document.getElementById('nut-carb');
const nutFat = document.getElementById('nut-fat');
const nutHealth = document.getElementById('nut-health');
const recIngredients = document.getElementById('rec-ingredients');
const recText = document.getElementById('rec-text');

// 1. Verificar estado del servidor (/health)
btnHealth.addEventListener('click', async () => {
    btnHealth.disabled = true;
    healthStatus.textContent = 'Verificando...';
    healthStatus.className = '';
    
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        if (response.ok) {
            healthStatus.textContent = `OK (Modelo cargado: ${data.model_loaded})`;
            healthStatus.classList.add('status-ok');
        } else {
            throw new Error('Servidor respondió con error');
        }
    } catch (error) {
        healthStatus.textContent = 'Error de conexión';
        healthStatus.classList.add('status-error');
    } finally {
        btnHealth.disabled = false;
    }
});

// 2. Manejo de selección de archivo e imagen de vista previa
fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    
    if (file) {
        // Validar que sea una imagen
        if (!file.type.startsWith('image/')) {
            showError('El archivo seleccionado no es una imagen válida.');
            resetUI();
            return;
        }

        // Crear una vista previa de la imagen localmente
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.classList.remove('hidden');
            btnPredict.disabled = false;
            hideError();
        };
        reader.readAsDataURL(file);
    } else {
        resetUI();
    }
});

// 3. Enviar la imagen para inferencia (/predict)
btnPredict.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) return;

    // Preparar UI para la carga
    resultsSection.classList.add('hidden');
    hideError();
    loader.classList.remove('hidden');
    btnPredict.disabled = true;

    // Crear el FormData para enviar como multipart/form-data
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData
        });

        // Intentamos extraer JSON
        const data = await response.json().catch(() => null);

        if (!response.ok) {
            // Manejar errores devueltos por el backend (detail)
            const detailError = data && data.detail ? data.detail : `Error HTTP: ${response.status}`;
            throw new Error(detailError);
        }

        // Si salió bien, mostrar en pantalla
        displayResults(data);

    } catch (error) {
        showError(`Fallo al clasificar la imagen: ${error.message}`);
    } finally {
        loader.classList.add('hidden');
        btnPredict.disabled = false;
    }
});

// 4. Funciones auxiliares

function displayResults(data) {
    // 4.1 Mostrar Predicción principal
    const top1Pct = formatPercentage(data.top1.probability);
    top1Result.textContent = `${data.top1.class_name} (${top1Pct})`;

    // 4.2 Llenar el top 5 (Top K)
    topkList.innerHTML = '';
    if (data.topk && data.topk.length) {
        data.topk.forEach(item => {
            const li = document.createElement('li');
            
            const spanName = document.createElement('span');
            spanName.textContent = item.class_name;
            
            const spanProb = document.createElement('span');
            spanProb.textContent = formatPercentage(item.probability);
            
            li.appendChild(spanName);
            li.appendChild(spanProb);
            topkList.appendChild(li);
        });
    }

    // 4.3 Mostrar Recomendación nutricional
    const rec = data.recommendation;
    if (rec) {
        recTitle.textContent = rec.title || 'Recomendación';
        recSummary.textContent = rec.summary || '';
        
        // Nutrición
        if (rec.nutrition) {
            nutCal.textContent = rec.nutrition.calories_kcal || 'N/D';
            nutProt.textContent = rec.nutrition.protein_g || 'N/D';
            nutCarb.textContent = rec.nutrition.carbs_g || 'N/D';
            nutFat.textContent = rec.nutrition.fat_g || 'N/D';
            nutHealth.textContent = rec.nutrition.health_assessment || 'N/D';
        }

        // Ingredientes
        recIngredients.innerHTML = '';
        if (rec.ingredients && rec.ingredients.length) {
            rec.ingredients.forEach(ing => {
                const li = document.createElement('li');
                li.textContent = ing;
                recIngredients.appendChild(li);
            });
        }

        recText.textContent = rec.recommendation || '';
    }

    // Hacer visible la sección completa
    resultsSection.classList.remove('hidden');
}

// Convertimos la probabilidad (0 a 1) a porcentaje con 2 decimales (0.00% a 100.00%)
function formatPercentage(prob) {
    return (prob * 100).toFixed(2) + '%';
}

function showError(message) {
    errorMsg.textContent = message;
    errorMsg.classList.remove('hidden');
}

function hideError() {
    errorMsg.classList.add('hidden');
    errorMsg.textContent = '';
}

function resetUI() {
    imagePreview.src = '';
    imagePreview.classList.add('hidden');
    btnPredict.disabled = true;
    resultsSection.classList.add('hidden');
    hideError();
}