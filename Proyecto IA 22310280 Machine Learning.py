# -*- coding: utf-8 -*-

# ==================== IMPORTS NECESARIOS ====================
# Importa la librería 'os' para interactuar con el sistema operativo.
# Se utiliza para acceder y manipular variables de entorno.
import os

# Configura la variable de entorno 'KMP_DUPLICATE_LIB_OK'.
# Este es un 'workaround' para evitar el error "OMP: Error #15"
# que ocurre cuando múltiples librerías (como NumPy, SciPy, PyTorch, etc.)
# que utilizan OpenMP intentan inicializar su propia copia del entorno de ejecución.
# Aunque la documentación lo describe como un "unsafe, unsupported, undocumented workaround",
# a menudo soluciona el problema en entornos de desarrollo sin efectos adversos significativos.
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Importa 'pandas' bajo el alias 'pd'.
# Es una librería fundamental para la manipulación y análisis de datos en Python,
# especialmente para trabajar con estructuras de datos tabulares como DataFrames.
import pandas as pd

# Nota: La dependencia de 'quandl' ha sido eliminada.
# 'quandl' se utilizaba anteriormente para descargar datos financieros directamente.
# Si se necesitaran datos reales, se podría considerar cargar un archivo CSV local
# o usar una alternativa de API de datos financieros que no sea Quandl.

# Importa 'train_test_split' del módulo 'sklearn.model_selection'.
# Esta función es crucial para dividir el conjunto de datos en subconjuntos
# de entrenamiento y prueba, lo que permite evaluar el rendimiento del modelo
# en datos no vistos.
from sklearn.model_selection import train_test_split
# Importa 'LinearRegression' del módulo 'sklearn.linear_model'.
# Esta clase implementa el algoritmo de regresión lineal simple y múltiple,
# que modela la relación entre una variable dependiente (objetivo) y una o más
# variables independientes (características) ajustando una ecuación lineal.
from sklearn.linear_model import LinearRegression
# Importa 'StandardScaler' del módulo 'sklearn.preprocessing'.
# Esta herramienta se utiliza para escalar (normalizar) las características
# del conjunto de datos, transformándolas para que tengan una media de 0 y una
# desviación estándar de 1. Esto es importante para muchos algoritmos de ML
# que son sensibles a la escala de los datos.
from sklearn.preprocessing import StandardScaler
# Importa 'mean_squared_error' para calcular el error cuadrático medio.
# Es una métrica común de evaluación para modelos de regresión, que mide
# el promedio de los cuadrados de los errores, es decir, la diferencia
# cuadrada promedio entre los valores estimados y el valor real.
from sklearn.metrics import mean_squared_error, r2_score
# Importa 'r2_score' para calcular el coeficiente de determinación (R-squared).
# El $R^2$ es otra métrica de evaluación para regresión que indica la proporción
# de la varianza en la variable dependiente que es predecible a partir de las
# variables independientes. Un valor más cercano a 1 indica un mejor ajuste del modelo.

# Importa 'matplotlib.pyplot' bajo el alias 'plt'.
# Es una librería de graficación ampliamente utilizada en Python para crear
# visualizaciones estáticas, animadas e interactivas en Python.
import matplotlib.pyplot as plt
# Importa 'numpy' bajo el alias 'np'.
# Es una librería fundamental para el cálculo numérico en Python, proporcionando
# soporte para arrays y matrices, junto con una gran colección de funciones
# matemáticas para operar sobre estos arrays de manera eficiente.
import numpy as np

# ==================== CONFIGURACIÓN DE DEPENDENCIAS Y DATOS ====================
# Lista las librerías necesarias que deben estar instaladas en el entorno de Python
# para que este script se ejecute correctamente.
# pip install numpy
# pip install scikit-learn
# pip install matplotlib
# pip install pandas

# ==================== CARGA DE DATOS INICIAL (AHORA SINTÉTICOS) ====================

# Imprime un mensaje indicando que se están generando datos sintéticos.
# Esto es para informar al usuario que no se está realizando una conexión a una fuente externa.
print("Generando datos sintéticos para simular precios de acciones...")

# Define el número de muestras (filas) que tendrá el conjunto de datos sintéticos.
n_samples = 500
# Establece la "semilla" para el generador de números aleatorios de NumPy.
# Esto asegura que los datos generados sean los mismos cada vez que se ejecuta
# el script, lo que es útil para la reproducibilidad.
np.random.seed(42)

# Genera datos simulados para la columna 'Adj. Close' (Precio de Cierre Ajustado).
# Se crea una base aleatoria entre 50 y 150 (0-1 * 100 + 50).
adj_close_base = np.random.rand(n_samples) * 100 + 50
# Genera datos simulados para la columna 'Adj. Open' (Precio de Apertura Ajustado).
# Se basa en el precio de cierre, añadiendo un pequeño ruido aleatorio.
adj_open = adj_close_base + (np.random.rand(n_samples) - 0.5) * 5
# Genera datos simulados para la columna 'Adj. High' (Precio Máximo Ajustado).
# Asegura que sea al menos tan alto como la apertura o el cierre base, más un ruido positivo.
adj_high = np.maximum(adj_open, adj_close_base) + np.random.rand(n_samples) * 5
# Genera datos simulados para la columna 'Adj. Low' (Precio Mínimo Ajustado).
# Asegura que sea al menos tan bajo como la apertura o el cierre base, menos un ruido positivo.
adj_low = np.minimum(adj_open, adj_close_base) - np.random.rand(n_samples) * 5
# Genera datos simulados para la columna 'Adj. Volume' (Volumen Ajustado).
# Se crea un volumen aleatorio con un valor base.
adj_volume = np.random.rand(n_samples) * 1000000 + 100000

# Se asegura que 'Adj. High' siempre sea mayor o igual que 'Adj. Open' y 'Adj. Close'.
adj_high = np.maximum(adj_high, np.maximum(adj_open, adj_close_base))
# Se asegura que 'Adj. Low' siempre sea menor o igual que 'Adj. Open' y 'Adj. Close'.
adj_low = np.minimum(adj_low, np.minimum(adj_open, adj_close_base))

# Crea un diccionario con los datos simulados para cada columna.
data = {
    'Adj. Open': adj_open,
    'Adj. High': adj_high,
    'Adj. Low': adj_low,
    'Adj. Close': adj_close_base,
    'Adj. Volume': adj_volume
}
# Convierte el diccionario en un DataFrame de pandas.
df = pd.DataFrame(data)

# Imprime un mensaje de confirmación de la generación de datos.
print("Datos sintéticos generados.")

# Imprime las primeras 5 filas del DataFrame para una inspección rápida
# de la estructura y los valores iniciales de los datos sintéticos.
print("\n--- DataFrame inicial (primeras 5 filas) ---")
print(df.head())

# ==================== SELECCIÓN DE CARACTERÍSTICAS Y PREPROCESAMIENTO ====================

# Selecciona un subconjunto específico de columnas del DataFrame original.
# Estas columnas serán las características base para nuestro modelo,
# enfocándose en los precios ajustados de apertura, máximo, mínimo, cierre y volumen.
df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]

# Crea una nueva característica llamada 'HL_PCT' (High-Low Percentage Change).
# Esta característica calcula la variación diaria del precio como un porcentaje
# del precio de cierre ajustado. Representa la volatilidad intradiaria.
# Se añade 1e-9 (un número muy pequeño) al denominador para evitar
# una posible división por cero si 'Adj. Close' fuera 0.
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / (df['Adj. Close'] + 1e-9) * 100.0

# Crea otra nueva característica llamada 'PCT_change' (Percentage Change).
# Esta característica calcula el cambio porcentual del precio de cierre ajustado
# con respecto al precio de apertura ajustado del mismo día. Representa la
# ganancia o pérdida porcentual del día.
# Se añade 1e-9 al denominador para evitar una posible división por cero
# si 'Adj. Open' fuera 0.
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / (df['Adj. Open'] + 1e-9) * 100.0

# ==================== DEFINICIÓN DEL DATAFRAME FINAL PARA REGRESIÓN ====================

# Re-define el DataFrame 'df' para incluir solo las columnas que se utilizarán
# como características (variables independientes) para el modelo de regresión.
# En este caso, 'Adj. Close' se incluye como característica de entrada,
# además de las dos características recién creadas ('HL_PCT' y 'PCT_change')
# y el volumen ajustado.
df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

# Imprime las primeras 5 filas del DataFrame después de la ingeniería de características.
# Esto permite verificar que las nuevas columnas se han añadido correctamente
# y que los datos tienen el formato esperado para el modelado.
print("\n--- DataFrame con características generadas (primeras 5 filas) ---")
print(df.head())

# ==================== MANEJO DE VALORES FALTANTES ====================
# Rellena cualquier valor 'NaN' (Not a Number) en el DataFrame con 0.
# Esto se hace para asegurar que no haya valores nulos que puedan causar errores
# en cálculos posteriores, especialmente después de operaciones como divisiones
# que pueden generar infinitos (que luego se convierten a NaN).
df.fillna(0, inplace=True)
# Reemplaza cualquier valor infinito (positivo o negativo) en el DataFrame por NaN.
# Esto es una precaución extra en caso de divisiones por cero que no se manejaron
# completamente con el 1e-9, o si los datos originales contenían infinitos.
df.replace([np.inf, -np.inf], np.nan, inplace=True)
# Elimina cualquier fila que aún contenga valores NaN.
# Esto asegura que el conjunto de datos final no tenga entradas incompletas,
# lo cual es crucial para la mayoría de los algoritmos de Machine Learning.
df.dropna(inplace=True)
# Imprime el número de filas restantes en el DataFrame después de la limpieza.
print(f"\nNúmero de filas después de eliminar valores NaN: {len(df)}")

# ==================== DEFINICIÓN DE CARACTERÍSTICAS (X) Y ETIQUETA (y) ====================

# Crea la columna 'Label', que será nuestra variable objetivo (lo que queremos predecir).
# En este caso, 'Label' se establece como el 'Adj. Close' (Precio de Cierre Ajustado)
# del *siguiente* día. El método '.shift(-1)' mueve los valores de la columna
# una posición hacia arriba, de modo que cada fila contenga el precio de cierre
# del día siguiente como su etiqueta.
df['Label'] = df['Adj. Close'].shift(-1)

# Elimina la última fila del DataFrame.
# La última fila, después de aplicar '.shift(-1)', tendrá un valor NaN en su columna 'Label'
# (ya que no hay un día siguiente para el último registro). Por lo tanto, esta fila
# se elimina para mantener la consistencia del conjunto de datos.
df.dropna(inplace=True)

# Define las características (variables independientes) del modelo.
# Se crea un array NumPy 'X' eliminando la columna 'Label' del DataFrame.
# 'axis=1' indica que se eliminará una columna.
X = np.array(df.drop(['Label'], axis=1))
# Define la etiqueta (variable dependiente o objetivo) del modelo.
# Se crea un array NumPy 'y' que contiene solo los valores de la columna 'Label'.
y = np.array(df['Label'])

# Imprime las dimensiones (forma) del array de características 'X'.
# Esto muestra el número de filas y columnas de las características.
print(f"\nDimensiones de las características (X): {X.shape}")
# Imprime las dimensiones (forma) del array de etiquetas 'y'.
# Esto muestra el número de elementos en la variable objetivo.
print(f"Dimensiones de la etiqueta (y): {y.shape}")

# ==================== ESCALADO DE CARACTERÍSTICAS ====================
# Inicializa una instancia de 'StandardScaler'.
# Este objeto se utilizará para estandarizar las características,
# transformándolas para que tengan una media de 0 y una desviación estándar de 1.
scaler = StandardScaler()
# Ajusta el escalador a los datos de las características (X) y luego las transforma.
# 'fit_transform' calcula la media y la desviación estándar de cada característica
# y luego aplica esa transformación.
X_scaled = scaler.fit_transform(X)
# Imprime un mensaje confirmando que las características han sido escaladas.
print("\nCaracterísticas escaladas.")

# ==================== DIVISIÓN EN CONJUNTOS DE ENTRENAMIENTO Y PRUEBA ====================
# Divide los datos escalados (X_scaled) y las etiquetas (y) en cuatro subconjuntos:
# X_train: Características para entrenamiento.
# X_test: Características para prueba.
# y_train: Etiquetas para entrenamiento.
# y_test: Etiquetas para prueba.
# 'test_size=0.2' especifica que el 20% de los datos se reservarán para el conjunto de prueba,
# y el 80% restante para el entrenamiento.
# 'random_state=42' asegura que la división sea reproducible; si se usa el mismo número,
# la división de los datos será idéntica en cada ejecución.
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Imprime las dimensiones de los conjuntos de entrenamiento y prueba
# para verificar que la división se realizó correctamente.
print(f"Tamaño del conjunto de entrenamiento (X_train): {X_train.shape}")
print(f"Tamaño del conjunto de prueba (X_test): {X_test.shape}")

# ==================== ENTRENAMIENTO DEL MODELO DE REGRESIÓN ====================
# Inicializa una instancia del modelo de Regresión Lineal.
# Este es el algoritmo que aprenderá la relación entre las características y la etiqueta.
model = LinearRegression()

# Imprime un mensaje indicando que el proceso de entrenamiento ha comenzado.
print("\nEntrenando el modelo de Regresión Lineal...")
# Entrena el modelo utilizando los datos de entrenamiento (características escaladas y etiquetas).
# El método 'fit' ajusta los coeficientes del modelo a los datos.
model.fit(X_train, y_train)
# Imprime un mensaje confirmando que el modelo ha sido entrenado exitosamente.
print("Modelo entrenado.")

# ==================== EVALUACIÓN DEL MODELO ====================
# Realiza predicciones sobre el conjunto de características de prueba (X_test).
# El modelo utiliza lo que aprendió durante el entrenamiento para estimar los valores
# de la variable objetivo para datos que nunca ha visto.
y_pred = model.predict(X_test)

# Calcula el Error Cuadrático Medio (Mean Squared Error - MSE).
# Esta métrica mide la diferencia cuadrática promedio entre los valores reales (y_test)
# y las predicciones del modelo (y_pred). Un MSE más bajo indica un mejor ajuste del modelo.
mse = mean_squared_error(y_test, y_pred)
# Imprime el valor del MSE formateado a 4 decimales.
print(f"\nError Cuadrático Medio (MSE): {mse:.4f}")

# Calcula el Coeficiente de Determinación (R-squared o $R^2$).
# Esta métrica indica qué tan bien las predicciones del modelo se ajustan a los valores reales,
# o la proporción de la varianza en la variable dependiente que es predecible a partir de
# las variables independientes. Un valor de $R^2$ cercano a 1 indica un buen ajuste.
r2 = r2_score(y_test, y_pred)
# Imprime el valor del $R^2$ formateado a 4 decimales.
print(f"Coeficiente de Determinación (R^2): {r2:.4f}")

# ==================== PREDICCIÓN Y VISUALIZACIÓN ====================
# Selecciona la primera muestra del conjunto de prueba para realizar una predicción individual.
# '.reshape(1, -1)' es necesario para asegurarse de que el formato de la muestra
# sea compatible con lo que espera el modelo (un array 2D con 1 fila y N columnas).
some_new_data_point_scaled = X_test[0].reshape(1, -1)
# Realiza una predicción utilizando el modelo entrenado sobre la muestra seleccionada.
prediction_for_first_test_point = model.predict(some_new_data_point_scaled)

# Imprime la predicción para el primer punto de prueba, formateada a 2 decimales.
print(f"\nPredicción para el primer punto de prueba: {prediction_for_first_test_point[0]:.2f}")
# Imprime el valor real correspondiente al primer punto de prueba, formateado a 2 decimales.
print(f"Valor real del primer punto de prueba: {y_test[0]:.2f}")

# Crea una nueva figura para el gráfico.
plt.figure(figsize=(10, 6))
# Dibuja un diagrama de dispersión (scatter plot) de los valores reales vs. las predicciones.
# Cada punto representa un par (valor real, valor predicho). 'alpha=0.7' ajusta la transparencia.
plt.scatter(y_test, y_pred, alpha=0.7)
# Dibuja una línea diagonal roja de referencia.
# Si el modelo fuera perfecto, todos los puntos se alinearían sobre esta línea,
# donde el valor predicho es igual al valor real.
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', linewidth=2)
# Establece el título del gráfico.
plt.title('Valores Reales vs. Predicciones')
# Establece la etiqueta del eje X.
plt.xlabel('Precio Real de Cierre Ajustado')
# Establece la etiqueta del eje Y.
plt.ylabel('Precio Predicho de Cierre Ajustado')
# Activa la cuadrícula en el gráfico para facilitar la lectura.
plt.grid(True)
# Muestra el gráfico.
plt.show()

# Imprime un mensaje final indicando que el programa ha terminado su ejecución.
print("\nPrograma de Regresión de Machine Learning finalizado.")
