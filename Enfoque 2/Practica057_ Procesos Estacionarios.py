# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:17:27 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import numpy as np  # Para operaciones numéricas y manejo de arrays
import matplotlib.pyplot as plt  # Para visualización de gráficos
from statsmodels.tsa.stattools import adfuller  # Para la prueba de Dickey-Fuller aumentada
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf  # Para gráficos de autocorrelación

class ProcesoEstacionario:
    """
    Clase principal que encapsula la funcionalidad para analizar y trabajar con procesos estacionarios.
    Proporciona métodos para verificar estacionariedad, transformar series y simular procesos ARMA.
    """
    
    def __init__(self, serie_temporal=None):
        """
        Constructor de la clase. Inicializa el objeto con una serie temporal opcional.
        
        Args:
            serie_temporal (array-like, opcional): Serie temporal a analizar. Por defecto es None.
        """
        # Convierte la serie a numpy array si se proporciona
        self.serie = np.array(serie_temporal) if serie_temporal is not None else None
        # Atributo para almacenar si la serie es estacionaria (inicialmente desconocido)
        self.es_estacionario = None
        # Atributo para almacenar resultados de la prueba ADF
        self.resultados_adf = None
    
    def verificar_estacionariedad(self, metodo='adf', visualizar=True, **kwargs):
        """
        Método principal para verificar la estacionariedad de una serie temporal.
        
        Args:
            metodo (str, opcional): Método de análisis ('adf' o 'visual'). Por defecto 'adf'.
            visualizar (bool, opcional): Si True, muestra gráficos de diagnóstico. Por defecto True.
            **kwargs: Argumentos adicionales para las pruebas estadísticas.
            
        Returns:
            bool: True si la serie es estacionaria, False si no lo es, None si el método es visual.
            
        Raises:
            ValueError: Si no se ha proporcionado una serie temporal para analizar.
        """
        # Verifica que exista una serie para analizar
        if self.serie is None:
            raise ValueError("No se ha proporcionado ninguna serie temporal para analizar.")
            
        # Método de Dickey-Fuller aumentada (ADF)
        if metodo == 'adf':
            # Realiza la prueba ADF
            self.resultados_adf = adfuller(self.serie, **kwargs)
            # Extrae el p-valor (posición 1 en los resultados)
            p_valor = self.resultados_adf[1]
            # Considera estacionaria si p-valor < 0.05 (rechaza hipótesis nula)
            self.es_estacionario = p_valor < 0.05
            
            # Muestra resultados si visualizar es True
            if visualizar:
                print(f"Resultado prueba ADF: p-valor = {p_valor:.4f}")
                print(f"La serie {'es' if self.es_estacionario else 'no es'} estacionaria")
                
        # Método visual (sin prueba estadística)
        elif metodo == 'visual':
            # Solo muestra gráficos si visualizar es True
            if visualizar:
                self._visualizar_serie()
            # No hay conclusión estadística con método visual
            self.es_estacionario = None  
        
        return self.es_estacionario
    
    def _visualizar_serie(self):
        """
        Método interno para visualización de la serie y sus propiedades.
        Muestra cuatro gráficos para evaluar estacionariedad visualmente.
        """
        # Crea figura con 4 subplots (2 filas x 2 columnas)
        plt.figure(figsize=(12, 8))
        
        # Subplot 1: Serie temporal original
        plt.subplot(2, 2, 1)
        plt.plot(self.serie)
        plt.title('Serie Temporal')
        plt.grid(True)
        
        # Subplot 2: Media móvil y desviación estándar móvil
        # Calcula media móvil con ventana de 12 periodos
        rolling_mean = pd.Series(self.serie).rolling(window=12).mean()
        # Calcula desviación estándar móvil con ventana de 12 periodos
        rolling_std = pd.Series(self.serie).rolling(window=12).std()
        
        plt.subplot(2, 2, 2)
        plt.plot(self.serie, label='Original')
        plt.plot(rolling_mean, color='red', label='Media Móvil')
        plt.plot(rolling_std, color='black', label='Desv. Estándar Móvil')
        plt.legend()
        plt.title('Media y Desviación Estándar Móviles')
        plt.grid(True)
        
        # Subplot 3: Función de Autocorrelación (ACF)
        plt.subplot(2, 2, 3)
        plot_acf(self.serie, lags=20, ax=plt.gca())  # ACF para 20 lags
        plt.title('Función de Autocorrelación (ACF)')
        
        # Subplot 4: Función de Autocorrelación Parcial (PACF)
        plt.subplot(2, 2, 4)
        plot_pacf(self.serie, lags=20, ax=plt.gca())  # PACF para 20 lags
        plt.title('Función de Autocorrelación Parcial (PACF)')
        
        # Ajusta el espaciado entre subplots
        plt.tight_layout()
        # Muestra todos los gráficos
        plt.show()
    
    def hacer_estacionaria(self, metodo='diff', orden=1, **kwargs):
        """
        Transforma la serie temporal para hacerla estacionaria.
        
        Args:
            metodo (str, opcional): Método de transformación ('diff' o 'log'). Por defecto 'diff'.
            orden (int, opcional): Orden de diferenciación si metodo='diff'. Por defecto 1.
            **kwargs: Argumentos adicionales para las transformaciones.
            
        Returns:
            np.array: Serie transformada.
            
        Raises:
            ValueError: Si no hay serie para transformar o método no reconocido.
        """
        # Verifica que exista una serie para transformar
        if self.serie is None:
            raise ValueError("No se ha proporcionado ninguna serie temporal para transformar.")
            
        # Método de diferenciación
        if metodo == 'diff':
            # Aplica diferenciación de orden 'orden'
            serie_transformada = np.diff(self.serie, n=orden)
        # Método de transformación logarítmica
        elif metodo == 'log':
            # Aplica logaritmo natural
            serie_transformada = np.log(self.serie)
        else:
            raise ValueError(f"Método {metodo} no reconocido.")
            
        return serie_transformada
    
    @staticmethod
    def simular_arma(n_muestras=100, ar_coef=None, ma_coef=None, sigma=1.0):
        """
        Simula un proceso ARMA (AutoRegresivo de Media Móvil) estacionario.
        
        Args:
            n_muestras (int, opcional): Número de puntos a simular. Por defecto 100.
            ar_coef (list, opcional): Coeficientes AR (autorregresivos). Por defecto None.
            ma_coef (list, opcional): Coeficientes MA (media móvil). Por defecto None.
            sigma (float, opcional): Desviación estándar del ruido. Por defecto 1.0.
            
        Returns:
            np.array: Serie temporal simulada.
        """
        # Coeficientes AR (si no se proporcionan, lista vacía)
        ar_coef = ar_coef or []
        # Coeficientes MA (si no se proporcionan, lista vacía)
        ma_coef = ma_coef or []
        # Orden AR (número de coeficientes AR)
        p = len(ar_coef)
        # Orden MA (número de coeficientes MA)
        q = len(ma_coef)
        
        # Inicializa array para la serie simulada
        serie = np.zeros(n_muestras)
        # Genera errores normales (ruido blanco)
        errores = np.random.normal(0, sigma, n_muestras + q)
        
        # Simula cada punto de la serie
        for t in range(max(p, q), n_muestras):
            # Componente AR: suma de coeficientes AR * valores pasados
            ar_component = 0
            for i in range(p):
                ar_component += ar_coef[i] * serie[t-1-i]
            
            # Componente MA: suma de coeficientes MA * errores pasados
            ma_component = 0
            for j in range(q):
                ma_component += ma_coef[j] * errores[t-j]
            
            # Combina componentes y añade error actual
            serie[t] = ar_component + ma_component + errores[t]
        
        return serie

# Ejemplo de uso principal
if __name__ == "__main__":
    import pandas as pd  # Solo necesario para el ejemplo
    
    print("=== Ejemplo de Procesos Estacionarios ===")
    
    # 1. Crear una serie temporal no estacionaria artificial
    np.random.seed(42)  # Fija semilla para reproducibilidad
    tiempo = np.arange(100)  # Vector de tiempo
    tendencia = 0.1 * tiempo  # Componente de tendencia lineal
    estacionalidad = 5 * np.sin(2 * np.pi * tiempo / 12)  # Componente estacional
    ruido = np.random.normal(0, 2, 100)  # Componente aleatoria (ruido)
    serie_no_estacionaria = tendencia + estacionalidad + ruido  # Combina componentes
    
    # 2. Analizar la serie original
    analizador = ProcesoEstacionario(serie_no_estacionaria)
    print("\nAnalizando serie original:")
    analizador.verificar_estacionariedad(visualizar=True)
    
    # 3. Transformar a estacionaria mediante diferenciación
    print("\nTransformando serie a estacionaria:")
    serie_diff = analizador.hacer_estacionaria(metodo='diff', orden=1)
    analizador_diff = ProcesoEstacionario(serie_diff)
    es_estacionaria = analizador_diff.verificar_estacionariedad(visualizar=True)
    
    # 4. Simular un proceso ARMA(1,1) estacionario
    print("\nSimulando proceso ARMA(1,1) estacionario:")
    arma_simulado = ProcesoEstacionario.simular_arma(
        n_muestras=200,
        ar_coef=[0.7],  # Coeficiente AR(1)
        ma_coef=[0.4],  # Coeficiente MA(1)
        sigma=0.5  # Desviación estándar del ruido
    )
    
    # Visualizar proceso simulado
    plt.figure(figsize=(10, 4))
    plt.plot(arma_simulado)
    plt.title('Proceso ARMA(1,1) Simulado')
    plt.grid(True)
    plt.show()
    
    # Verificar estacionariedad del proceso simulado
    analizador_sim = ProcesoEstacionario(arma_simulado)
    analizador_sim.verificar_estacionariedad(visualizar=True)