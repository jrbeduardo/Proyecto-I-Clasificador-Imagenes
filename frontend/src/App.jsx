import { useMemo, useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export default function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const imageUrl = useMemo(() => (file ? URL.createObjectURL(file) : ''), [file]);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setResult(null);

    if (!file) {
      setError('Selecciona una imagen.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Error al predecir.');
      setResult(data);
    } catch (err) {
      setError(err.message || 'Error inesperado.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <h1>Food AI</h1>

      <form onSubmit={handleSubmit} className="form">
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button type="submit" disabled={loading}>{loading ? 'Analizando...' : 'Predecir'}</button>
      </form>

      {error && <p className="error">{error}</p>}

      {file && <img src={imageUrl} alt="preview" className="preview" />}

      {result && (
        <section className="result">
          <p><strong>Top-1:</strong> {result.top1.class_name} ({(result.top1.probability * 100).toFixed(1)}%)</p>

          <h3>Top-5</h3>
          <ul>
            {result.topk.map((item) => (
              <li key={item.class_id}>{item.class_name} - {(item.probability * 100).toFixed(1)}%</li>
            ))}
          </ul>

          {result.recommendation?.title && <h3>{result.recommendation.title}</h3>}
          {result.recommendation?.summary && <p>{result.recommendation.summary}</p>}

          {!!result.recommendation?.ingredients?.length && (
            <>
              <h4>Ingredientes</h4>
              <ul>
                {result.recommendation.ingredients.map((ingredient, idx) => (
                  <li key={`${ingredient}-${idx}`}>{ingredient}</li>
                ))}
              </ul>
            </>
          )}

          {result.recommendation?.nutrition && (
            <>
              <h4>Informacion nutricional</h4>
              <div className="nutritionGrid">
                <div><span>Calorias</span><strong>{result.recommendation.nutrition.calories_kcal}</strong></div>
                <div><span>Proteinas</span><strong>{result.recommendation.nutrition.protein_g}</strong></div>
                <div><span>Carbohidratos</span><strong>{result.recommendation.nutrition.carbs_g}</strong></div>
                <div><span>Grasas</span><strong>{result.recommendation.nutrition.fat_g}</strong></div>
              </div>
              <p>{result.recommendation.nutrition.health_assessment}</p>
            </>
          )}

          {result.recommendation?.recommendation && <p>{result.recommendation.recommendation}</p>}
        </section>
      )}
    </main>
  );
}
