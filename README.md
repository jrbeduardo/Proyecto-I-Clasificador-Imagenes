# Proyecto I · Clasificador de imágenes con redes neuronales

**Universidad Nacional Autónoma de México**  
**Facultad de Ciencias**  
**Plan de Trabajo · Proyecto I**

## Datos del curso

- **Semestre:** 2026-2
- **Clave:** 2130035
- **Grupo:** 6013
- **Profesor:** José Eduardo Rodríguez Barrios — jrbeduardo@gmail.com
- **Horario:** Lunes, miércoles y viernes · 17:00–18:00
- **Ayudante:** Carlos Cuauhtémoc Gutiérrez Salazar — carloscuauhtemoc310123@gmail.com
- **Horario de ayudante:** Martes y jueves · 17:00–18:00

## Objetivo del seminario-taller

Desarrollar un proyecto de tesis en aprendizaje profundo aplicado a visión por computadora. Cada estudiante completará un clasificador de imágenes con un flujo integral: definición del problema, preparación de datos, entrenamiento, evaluación, despliegue y documentación profesional.


## Estructura del repositorio

```
Proyecto-I-Clasificador-Imagenes/
├── app/                   # API FastAPI para inferencia y recomendacion
├── frontend/              # Interfaz web React + Vite
├── README.md              # Este archivo
├── clases/                # Material de clases
├── notebooks/             # Notebooks con ejercicios y ejemplos
├── papers/                # Artículos científicos y lecturas del curso
└── .gitignore             # Archivos y directorios a ignorar
```

## Notebooks y enlaces de Google Colab

> Puedes abrir cualquier notebook directamente en Colab con los siguientes enlaces.

| Notebook | GitHub | Colab |
|---|---|---|
| atencion_simple_numpy.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/atencion_simple_numpy.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/atencion_simple_numpy.ipynb) |
| batch_normalization.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/batch_normalization.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/batch_normalization.ipynb) |
| cnn_introduccion.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/cnn_introduccion.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/cnn_introduccion.ipynb) |
| data_augmentation_basico_pytorch.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/data_augmentation_basico_pytorch.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/data_augmentation_basico_pytorch.ipynb) |
| data_augmentation_fine_tune_pytorch.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/data_augmentation_fine_tune_pytorch.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/data_augmentation_fine_tune_pytorch.ipynb) |
| filtros_cnn_leonora.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/filtros_cnn_leonora.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/filtros_cnn_leonora.ipynb) |
| mnist_loader.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/mnist_loader.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/mnist_loader.ipynb) |
| oxford_pet_EDA.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/oxford_pet_EDA.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/oxford_pet_EDA.ipynb) |
| pixelado_residuo_resnet.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/pixelado_residuo_resnet.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/pixelado_residuo_resnet.ipynb) |
| positional_embeddings_sinusoidales.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/positional_embeddings_sinusoidales.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/positional_embeddings_sinusoidales.ipynb) |
| primer-clasificador.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/primer-clasificador.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/primer-clasificador.ipynb) |
| PyTorch_load_model.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/PyTorch_load_model.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/PyTorch_load_model.ipynb) |
| pytorch_red_neuronal.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/pytorch_red_neuronal.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/pytorch_red_neuronal.ipynb) |
| pytorch_red_neuronal_hyper.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/pytorch_red_neuronal_hyper.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/pytorch_red_neuronal_hyper.ipynb) |
| pytorch_red_neuronal_Optimer.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/pytorch_red_neuronal_Optimer.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/pytorch_red_neuronal_Optimer.ipynb) |
| red_CNN_cifar10.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/red_CNN_cifar10.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/red_CNN_cifar10.ipynb) |
| red_CNN_cifar10_early_stopping.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/red_CNN_cifar10_early_stopping.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/red_CNN_cifar10_early_stopping.ipynb) |
| red_neuronal_2_capas.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/red_neuronal_2_capas.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/red_neuronal_2_capas.ipynb) |
| resnet56_cifar10.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/resnet56_cifar10.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/resnet56_cifar10.ipynb) |
| resnet56_cifar10_clase.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/resnet56_cifar10_clase.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/resnet56_cifar10_clase.ipynb) |
| skipgram_embeddings_pytorch.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/skipgram_embeddings_pytorch.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/skipgram_embeddings_pytorch.ipynb) |
| transformer_model.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/transformer_model.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/transformer_model.ipynb) |
| transfer_learning_resnet18_oxford.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/transfer_learning_resnet18_oxford.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/transfer_learning_resnet18_oxford.ipynb) |
| vit_parches_16x16_explicacion.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/vit_parches_16x16_explicacion.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/vit_parches_16x16_explicacion.ipynb) |
| word_embeddings.ipynb | [![Ver en GitHub](https://img.shields.io/badge/Ver%20en-GitHub-181717?logo=github&logoColor=white)](notebooks/word_embeddings.ipynb) | [![Abrir en Colab](https://img.shields.io/badge/Abrir%20en-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/jrbeduardo/Proyecto-I-Clasificador-Imagenes/blob/main/notebooks/word_embeddings.ipynb) |

## Licencia

Material de uso académico para la Facultad de Ciencias, UNAM.
