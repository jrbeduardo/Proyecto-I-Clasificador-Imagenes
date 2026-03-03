# PyTorch

## Que es PyTorch

PyTorch es una biblioteca open-source de machine learning desarrollada por Meta (Facebook). Proporciona tensores multidimensionales optimizados para GPU y un sistema de diferenciacion automatica para construir y entrenar redes neuronales.

### Caracteristicas principales

- **Tensores**: Estructuras similares a arrays de NumPy con soporte para GPU
- **Autograd**: Calculo automatico de gradientes para backpropagation
- **nn.Module**: Sistema modular para construir arquitecturas de redes neuronales
- **Dinamico**: Grafos computacionales construidos dinаmicamente (eager execution)
- **GPU Acceleration**: Soporte nativo para CUDA y computation en GPU

## Instalacion

### Con pip

```bash
pip install torch torchvision
```

### Con conda

```bash
conda install pytorch torchvision -c pytorch
```

### Con uv (recomendado para este proyecto)

```bash
uv pip install torch torchvision
```

### Verificar instalacion

```python
import torch
print(torch.__version__)
print(torch.cuda.is_available())  # True si hay GPU disponible
```

## Uso basico

### Crear tensores

```python
import torch

# Desde lista
x = torch.tensor([1, 2, 3])

# Tensor aleatorio
x = torch.randn(3, 4)

# Desde NumPy
import numpy as np
arr = np.array([1, 2, 3])
x = torch.from_numpy(arr)
```

### Operaciones con GPU

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x = x.to(device)  # Mover tensor a GPU
```

### Red neuronal simple

```python
import torch.nn as nn
import torch.nn.functional as F

model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)

# Forward pass
output = model(x)

# Loss y optimizacion
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
```

## Recursos

- Documentacion oficial: https://pytorch.org/docs/
- Tutoriales: https://pytorch.org/tutorials/
- Forum: https://discuss.pytorch.org/
