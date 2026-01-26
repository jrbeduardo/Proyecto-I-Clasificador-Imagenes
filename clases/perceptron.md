# El Perceptrón

## Introducción

El perceptrón es el modelo más simple de una neurona artificial y representa la base fundamental de las redes neuronales modernas. Fue propuesto por Frank Rosenblatt en 1957 y constituye un clasificador binario lineal.

## Definición

Un perceptrón es una función matemática que toma un vector de entrada $\mathbf{x} = (x_1, x_2, \ldots, x_n)$ y produce una salida binaria:

$$
y = f\left(\sum_{i=1}^{n} w_i x_i + b\right)
$$

Donde:
- $x_i$ son las entradas
- $w_i$ son los pesos sinápticos
- $b$ es el sesgo (bias)
- $f$ es la función de activación (típicamente una función escalón)

## Componentes

### 1. Entradas
Las características o atributos del problema que queremos clasificar.

### 2. Pesos
Valores que determinan la importancia de cada entrada. Se ajustan durante el entrenamiento.

### 3. Sesgo (Bias)
Permite desplazar la función de decisión, aumentando la flexibilidad del modelo.

### 4. Función de Activación
Transforma la suma ponderada en una salida. Para el perceptrón clásico:

$$
f(z) = \begin{cases}
1 & \text{si } z \geq 0 \\
0 & \text{si } z < 0
\end{cases}
$$

## Regla de Aprendizaje

El perceptrón aprende mediante un algoritmo iterativo:

1. Inicializar pesos y sesgo aleatoriamente
2. Para cada ejemplo de entrenamiento:
   - Calcular la salida predicha
   - Actualizar pesos: $w_i = w_i + \eta (y_{real} - y_{pred}) x_i$
   - Actualizar sesgo: $b = b + \eta (y_{real} - y_{pred})$

Donde $\eta$ es la tasa de aprendizaje.

## Limitaciones

### Problema XOR
El perceptrón solo puede clasificar problemas linealmente separables. No puede resolver el problema XOR, lo que llevó al desarrollo de redes multicapa.

### Funciones No Lineales
Para problemas más complejos, se requieren perceptrones multicapa (MLP) con funciones de activación no lineales.

## Importancia Histórica

El perceptrón sentó las bases para:
- Redes neuronales multicapa
- Algoritmo de retropropagación
- Deep Learning moderno

A pesar de sus limitaciones, sigue siendo fundamental para entender cómo funcionan las redes neuronales actuales.

## Referencias

- Rosenblatt, F. (1958). "The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain"
- Minsky, M., & Papert, S. (1969). "Perceptrons: An Introduction to Computational Geometry"
