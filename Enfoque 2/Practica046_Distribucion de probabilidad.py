# -*- coding: utf-8 -*-
"""
Script para implementación de distribuciones de probabilidad
Incluye distribuciones discretas y continuas con funcionalidades básicas
"""

# Importación de numpy para operaciones numéricas eficientes
import numpy as np

# Importación de matplotlib para visualización gráfica
import matplotlib.pyplot as plt

# Importación de funciones matemáticas específicas
from math import factorial  # Para cálculo de factoriales
from math import exp  # Para función exponencial
from math import sqrt  # Para raíz cuadrada
from math import pi  # Para constante π

# Importación de tipos para anotaciones de tipo
from typing import Dict  # Para diccionarios tipados
from typing import List  # Para listas tipadas
from typing import Tuple  # Para tuplas tipadas
from typing import Union  # Para tipos unión

# Importación de defaultdict para diccionarios con valores por defecto
from collections import defaultdict

# Importación de Enum para crear enumeraciones
from enum import Enum

# Definición de enumeración para tipos de distribución
class DistributionType(Enum):
    """
    Enumeración para clasificar distribuciones como discretas o continuas
    
    Valores:
        DISCRETE: Para distribuciones discretas (ej: Binomial)
        CONTINUOUS: Para distribuciones continuas (ej: Normal)
    """
    DISCRETE = 1  # Representa distribuciones discretas
    CONTINUOUS = 2  # Representa distribuciones continuas

# Clase base abstracta para distribuciones de probabilidad
class ProbabilityDistribution:
    """
    Clase base abstracta para implementar distribuciones de probabilidad
    
    Métodos abstractos que deben implementar las clases hijas:
        pmf/pdf: Función de masa/densidad de probabilidad
        cdf: Función de distribución acumulativa
        mean: Cálculo de la media
        variance: Cálculo de la varianza
        sample: Generación de muestras aleatorias
    """
    def __init__(self):
        """Inicializa la distribución con tipo None (debe ser definido por subclases)"""
        self.type = None  # Será definido por las clases hijas
    
    def pmf(self, x: Union[int, float]) -> float:
        """
        Función de masa de probabilidad (para distribuciones discretas)
        
        Args:
            x: Punto donde evaluar la PMF
            
        Returns:
            Probabilidad en el punto x
            
        Raises:
            NotImplementedError: Si no está implementado en la subclase
        """
        raise NotImplementedError("Debe implementarse en subclases")
    
    def pdf(self, x: float) -> float:
        """
        Función de densidad de probabilidad (para distribuciones continuas)
        
        Args:
            x: Punto donde evaluar la PDF
            
        Returns:
            Densidad de probabilidad en el punto x
            
        Raises:
            NotImplementedError: Si no está implementado en la subclase
        """
        raise NotImplementedError("Debe implementarse en subclases")
    
    def cdf(self, x: Union[int, float]) -> float:
        """
        Función de distribución acumulativa
        
        Args:
            x: Punto donde evaluar la CDF
            
        Returns:
            Probabilidad acumulada hasta x
            
        Raises:
            NotImplementedError: Si no está implementado en la subclase
        """
        raise NotImplementedError("Debe implementarse en subclases")
    
    def mean(self) -> float:
        """
        Calcula la media o valor esperado de la distribución
        
        Returns:
            Valor de la media
            
        Raises:
            NotImplementedError: Si no está implementado en la subclase
        """
        raise NotImplementedError("Debe implementarse en subclases")
    
    def variance(self) -> float:
        """
        Calcula la varianza de la distribución
        
        Returns:
            Valor de la varianza
            
        Raises:
            NotImplementedError: Si no está implementado en la subclase
        """
        raise NotImplementedError("Debe implementarse en subclases")
    
    def sample(self, n: int = 1) -> List[float]:
        """
        Genera muestras aleatorias de la distribución
        
        Args:
            n: Número de muestras a generar
            
        Returns:
            Lista con las n muestras generadas
            
        Raises:
            NotImplementedError: Si no está implementado en la subclase
        """
        raise NotImplementedError("Debe implementarse en subclases")
    
    def plot(self, start: float, end: float, num_points: int = 100):
        """
        Grafica la función de probabilidad (PMF o PDF según el tipo)
        
        Args:
            start: Valor inicial del rango a graficar
            end: Valor final del rango a graficar
            num_points: Número de puntos para distribuciones continuas
        """
        if self.type == DistributionType.DISCRETE:
            # Para distribuciones discretas: gráfico de bastones
            x_vals = np.arange(start, end + 1)  # Valores enteros en el rango
            y_vals = [self.pmf(x) for x in x_vals]  # Calcula PMF para cada punto
            plt.stem(x_vals, y_vals, use_line_collection=True)  # Gráfico de bastones
            plt.title('Función de Masa de Probabilidad (PMF)')  # Título
        else:
            # Para distribuciones continuas: gráfico de línea suave
            x_vals = np.linspace(start, end, num_points)  # Puntos equiespaciados
            y_vals = [self.pdf(x) for x in x_vals]  # Calcula PDF para cada punto
            plt.plot(x_vals, y_vals)  # Gráfico de línea
            plt.title('Función de Densidad de Probabilidad (PDF)')  # Título
        
        # Configuración común del gráfico
        plt.xlabel('x')  # Etiqueta eje X
        plt.ylabel('Probabilidad')  # Etiqueta eje Y
        plt.grid(True)  # Activar cuadrícula
        plt.show()  # Mostrar gráfico

# Implementación de distribución uniforme discreta
class DiscreteUniform(ProbabilityDistribution):
    """
    Distribución uniforme discreta entre a y b (inclusive)
    
    Atributos:
        a: Límite inferior del rango
        b: Límite superior del rango
        n: Número de valores posibles (b - a + 1)
    """
    def __init__(self, a: int, b: int):
        """
        Inicializa la distribución uniforme discreta
        
        Args:
            a: Valor mínimo (entero)
            b: Valor máximo (entero)
        """
        super().__init__()  # Llama al constructor de la clase padre
        self.type = DistributionType.DISCRETE  # Define el tipo como discreto
        self.a = a  # Establece límite inferior
        self.b = b  # Establece límite superior
        self.n = b - a + 1  # Calcula número de valores posibles
    
    def pmf(self, x: int) -> float:
        """
        Función de masa de probabilidad en x
        
        Args:
            x: Punto a evaluar
            
        Returns:
            Probabilidad en x (1/n si está en [a,b], 0 sino)
        """
        if x < self.a or x > self.b:
            return 0.0  # Probabilidad 0 fuera del rango
        return 1.0 / self.n  # Probabilidad uniforme dentro del rango
    
    def cdf(self, x: int) -> float:
        """
        Función de distribución acumulativa en x
        
        Args:
            x: Punto a evaluar
            
        Returns:
            Probabilidad acumulada hasta x
        """
        if x < self.a:
            return 0.0  # Acumulada 0 antes del rango
        elif x > self.b:
            return 1.0  # Acumulada 1 después del rango
        return (x - self.a + 1) / self.n  # Lineal entre a y b
    
    def mean(self) -> float:
        """
        Calcula la media de la distribución
        
        Returns:
            Media (a + b)/2
        """
        return (self.a + self.b) / 2  # Fórmula para media de uniforme discreta
    
    def variance(self) -> float:
        """
        Calcula la varianza de la distribución
        
        Returns:
            Varianza (n² - 1)/12
        """
        return (self.n**2 - 1) / 12  # Fórmula para varianza de uniforme discreta
    
    def sample(self, n: int = 1) -> List[int]:
        """
        Genera muestras aleatorias de la distribución
        
        Args:
            n: Número de muestras a generar
            
        Returns:
            Lista con n muestras aleatorias
        """
        return np.random.randint(self.a, self.b + 1, n).tolist()  # Muestras uniformes

# Implementación de distribución binomial
class Binomial(ProbabilityDistribution):
    """
    Distribución binomial (n ensayos independientes con probabilidad p de éxito)
    
    Atributos:
        n: Número de ensayos
        p: Probabilidad de éxito en cada ensayo
        q: Probabilidad de fracaso (1 - p)
    """
    def __init__(self, n: int, p: float):
        """
        Inicializa la distribución binomial
        
        Args:
            n: Número de ensayos (entero positivo)
            p: Probabilidad de éxito (en [0,1])
        """
        super().__init__()  # Llama al constructor de la clase padre
        self.type = DistributionType.DISCRETE  # Define el tipo como discreto
        self.n = n  # Establece número de ensayos
        self.p = p  # Establece probabilidad de éxito
        self.q = 1 - p  # Calcula probabilidad de fracaso
    
    def pmf(self, k: int) -> float:
        """
        Función de masa de probabilidad en k éxitos
        
        Args:
            k: Número de éxitos a evaluar
            
        Returns:
            Probabilidad de exactamente k éxitos
        """
        if k < 0 or k > self.n:
            return 0.0  # Probabilidad 0 fuera de rango válido
        # Fórmula binomial: combinaciones(n,k) * p^k * q^(n-k)
        return (factorial(self.n) / (factorial(k) * factorial(self.n - k))) * \
               (self.p**k) * (self.q**(self.n - k))
    
    def cdf(self, k: int) -> float:
        """
        Función de distribución acumulativa hasta k éxitos
        
        Args:
            k: Número máximo de éxitos
            
        Returns:
            Probabilidad de k o menos éxitos
        """
        return sum(self.pmf(i) for i in range(0, k + 1))  # Suma de PMFs
    
    def mean(self) -> float:
        """
        Calcula la media de la distribución
        
        Returns:
            Media n*p
        """
        return self.n * self.p  # Fórmula para media binomial
    
    def variance(self) -> float:
        """
        Calcula la varianza de la distribución
        
        Returns:
            Varianza n*p*q
        """
        return self.n * self.p * self.q  # Fórmula para varianza binomial
    
    def sample(self, n: int = 1) -> List[int]:
        """
        Genera muestras aleatorias de la distribución
        
        Args:
            n: Número de muestras a generar
            
        Returns:
            Lista con n muestras aleatorias
        """
        return np.random.binomial(self.n, self.p, n).tolist()  # Muestras binomiales

# Implementación de distribución de Poisson
class Poisson(ProbabilityDistribution):
    """
    Distribución de Poisson para eventos raros con tasa λ
    
    Atributos:
        lam: Parámetro λ (tasa promedio de ocurrencia)
    """
    def __init__(self, lam: float):
        """
        Inicializa la distribución de Poisson
        
        Args:
            lam: Tasa promedio de ocurrencia (λ > 0)
        """
        super().__init__()  # Llama al constructor de la clase padre
        self.type = DistributionType.DISCRETE  # Define el tipo como discreto
        self.lam = lam  # Establece parámetro lambda
    
    def pmf(self, k: int) -> float:
        """
        Función de masa de probabilidad para k ocurrencias
        
        Args:
            k: Número de ocurrencias a evaluar
            
        Returns:
            Probabilidad de exactamente k ocurrencias
        """
        if k < 0:
            return 0.0  # Probabilidad 0 para valores negativos
        # Fórmula de Poisson: (λ^k * e^-λ) / k!
        return (self.lam**k * exp(-self.lam)) / factorial(k)
    
    def cdf(self, k: int) -> float:
        """
        Función de distribución acumulativa hasta k ocurrencias
        
        Args:
            k: Número máximo de ocurrencias
            
        Returns:
            Probabilidad de k o menos ocurrencias
        """
        return sum(self.pmf(i) for i in range(0, k + 1))  # Suma de PMFs
    
    def mean(self) -> float:
        """
        Calcula la media de la distribución
        
        Returns:
            Media λ
        """
        return self.lam  # La media es igual a λ
    
    def variance(self) -> float:
        """
        Calcula la varianza de la distribución
        
        Returns:
            Varianza λ
        """
        return self.lam  # La varianza es igual a λ
    
    def sample(self, n: int = 1) -> List[int]:
        """
        Genera muestras aleatorias de la distribución
        
        Args:
            n: Número de muestras a generar
            
        Returns:
            Lista con n muestras aleatorias
        """
        return np.random.poisson(self.lam, n).tolist()  # Muestras de Poisson

# Implementación de distribución normal (gaussiana)
class Normal(ProbabilityDistribution):
    """
    Distribución normal (gaussiana) con media μ y desviación σ
    
    Atributos:
        mu: Media de la distribución
        sigma: Desviación estándar (σ > 0)
    """
    def __init__(self, mu: float = 0, sigma: float = 1):
        """
        Inicializa la distribución normal
        
        Args:
            mu: Media de la distribución (default 0)
            sigma: Desviación estándar (default 1)
        """
        super().__init__()  # Llama al constructor de la clase padre
        self.type = DistributionType.CONTINUOUS  # Define el tipo como continuo
        self.mu = mu  # Establece media
        self.sigma = sigma  # Establece desviación estándar
    
    def pdf(self, x: float) -> float:
        """
        Función de densidad de probabilidad en x
        
        Args:
            x: Punto a evaluar
            
        Returns:
            Densidad de probabilidad en x
        """
        # Fórmula normal: (1/(σ√(2π))) * e^(-(x-μ)²/(2σ²))
        return (1 / (self.sigma * sqrt(2 * pi))) * \
               exp(-0.5 * ((x - self.mu) / self.sigma)**2)
    
    def cdf(self, x: float) -> float:
        """
        Función de distribución acumulativa en x
        
        Args:
            x: Punto a evaluar
            
        Returns:
            Probabilidad acumulada hasta x
        """
        from scipy.stats import norm  # Importación diferida para evitar dependencia
        return norm.cdf(x, self.mu, self.sigma)  # Usa scipy para precisión
    
    def mean(self) -> float:
        """
        Calcula la media de la distribución
        
        Returns:
            Media μ
        """
        return self.mu  # La media es μ
    
    def variance(self) -> float:
        """
        Calcula la varianza de la distribución
        
        Returns:
            Varianza σ²
        """
        return self.sigma**2  # La varianza es σ²
    
    def sample(self, n: int = 1) -> List[float]:
        """
        Genera muestras aleatorias de la distribución
        
        Args:
            n: Número de muestras a generar
            
        Returns:
            Lista con n muestras aleatorias
        """
        return np.random.normal(self.mu, self.sigma, n).tolist()  # Muestras normales

# Implementación de distribución exponencial
class Exponential(ProbabilityDistribution):
    """
    Distribución exponencial con parámetro λ (tasa)
    
    Atributos:
        lam: Parámetro λ (tasa > 0)
    """
    def __init__(self, lam: float = 1):
        """
        Inicializa la distribución exponencial
        
        Args:
            lam: Tasa de la distribución (λ > 0, default 1)
        """
        super().__init__()  # Llama al constructor de la clase padre
        self.type = DistributionType.CONTINUOUS  # Define el tipo como continuo
        self.lam = lam  # Establece parámetro lambda
    
    def pdf(self, x: float) -> float:
        """
        Función de densidad de probabilidad en x
        
        Args:
            x: Punto a evaluar (x ≥ 0)
            
        Returns:
            Densidad de probabilidad en x
        """
        if x < 0:
            return 0.0  # Densidad 0 para valores negativos
        # Fórmula exponencial: λ * e^(-λx)
        return self.lam * exp(-self.lam * x)
    
    def cdf(self, x: float) -> float:
        """
        Función de distribución acumulativa en x
        
        Args:
            x: Punto a evaluar (x ≥ 0)
            
        Returns:
            Probabilidad acumulada hasta x
        """
        if x < 0:
            return 0.0  # Acumulada 0 para valores negativos
        # Fórmula acumulativa: 1 - e^(-λx)
        return 1 - exp(-self.lam * x)
    
    def mean(self) -> float:
        """
        Calcula la media de la distribución
        
        Returns:
            Media 1/λ
        """
        return 1 / self.lam  # La media es 1/λ
    
    def variance(self) -> float:
        """
        Calcula la varianza de la distribución
        
        Returns:
            Varianza 1/λ²
        """
        return 1 / (self.lam**2)  # La varianza es 1/λ²
    
    def sample(self, n: int = 1) -> List[float]:
        """
        Genera muestras aleatorias de la distribución
        
        Args:
            n: Número de muestras a generar
            
        Returns:
            Lista con n muestras aleatorias
        """
        return np.random.exponential(1/self.lam, n).tolist()  # Muestras exponenciales

# Implementación de distribución empírica
class EmpiricalDistribution(ProbabilityDistribution):
    """
    Distribución empírica construida a partir de datos observados
    
    Atributos:
        data: Datos observados (array numpy)
        type: Tipo inferido (discreto o continuo)
        counts: Conteo de frecuencias (para discretas)
        total: Total de datos (para discretas)
        kde: Estimación de densidad kernel (para continuas)
    """
    def __init__(self, data: List[Union[int, float]]):
        """
        Inicializa la distribución empírica
        
        Args:
            data: Lista de datos observados
        """
        super().__init__()  # Llama al constructor de la clase padre
        self.data = np.array(data)  # Convierte datos a array numpy
        
        # Determina si es discreta (todos enteros) o continua
        if all(isinstance(x, int) for x in data):
            self.type = DistributionType.DISCRETE  # Tipo discreto
            # Para discretas: conteo de frecuencias
            self.counts = defaultdict(int)  # Diccionario para conteos
            for x in data:
                self.counts[x] += 1  # Incrementa conteo para cada valor
            self.total = len(data)  # Total de observaciones
        else:
            self.type = DistributionType.CONTINUOUS  # Tipo continuo
            # Para continuas: estimación de densidad kernel (KDE)
            from scipy.stats import gaussian_kde  # Importación diferida
            self.kde = gaussian_kde(data)  # Crea estimador KDE
    
    def pmf(self, x: int) -> float:
        """
        Función de masa de probabilidad (solo para discretas)
        
        Args:
            x: Valor a evaluar
            
        Returns:
            Probabilidad empírica en x
            
        Raises:
            ValueError: Si se usa en distribución continua
        """
        if self.type != DistributionType.DISCRETE:
            raise ValueError("PMF solo para distribuciones discretas")
        return self.counts.get(x, 0) / self.total  # Frecuencia relativa
    
    def pdf(self, x: float) -> float:
        """
        Función de densidad (solo para continuas)
        
        Args:
            x: Punto a evaluar
            
        Returns:
            Densidad estimada en x
            
        Raises:
            ValueError: Si se usa en distribución discreta
        """
        if self.type != DistributionType.CONTINUOUS:
            raise ValueError("PDF solo para distribuciones continuas")
        return self.kde.evaluate(x)[0]  # Estimación KDE en x
    
    def cdf(self, x: float) -> float:
        """
        Función de distribución acumulativa empírica
        
        Args:
            x: Punto a evaluar
            
        Returns:
            Proporción de datos ≤ x
        """
        return np.mean(self.data <= x)  # Proporción de datos menores o iguales a x
    
    def mean(self) -> float:
        """
        Calcula la media muestral
        
        Returns:
            Media de los datos
        """
        return np.mean(self.data)  # Media muestral
    
    def variance(self) -> float:
        """
        Calcula la varianza muestral
        
        Returns:
            Varianza de los datos
        """
        return np.var(self.data)  # Varianza muestral
    
    def sample(self, n: int = 1) -> List[float]:
        """
        Genera muestras aleatorias (con reemplazo) de los datos
        
        Args:
            n: Número de muestras a generar
            
        Returns:
            Lista con n muestras aleatorias
        """
        return np.random.choice(self.data, n).tolist()  # Muestreo con reemplazo

# Bloque principal de ejecución (ejemplos de uso)
if __name__ == "__main__":
    print("=== Ejemplos de Distribuciones de Probabilidad ===\n")
    
    # 1. Ejemplo con distribución uniforme discreta (dado de 6 caras)
    print("1. Uniforme Discreta (a=1, b=6):")
    uniform_disc = DiscreteUniform(1, 6)  # Crea distribución
    print(f"PMF(3) = {uniform_disc.pmf(3):.3f}")  # Probabilidad de sacar 3
    print(f"CDF(3) = {uniform_disc.cdf(3):.3f}")  # Probabilidad de sacar ≤3
    print(f"Media = {uniform_disc.mean():.1f}, Varianza = {uniform_disc.variance():.2f}")
    print(f"Muestra: {uniform_disc.sample(5)}")  # 5 lanzamientos simulados
    uniform_disc.plot(0, 7)  # Gráfico de la distribución
    
    # 2. Ejemplo con distribución binomial (10 ensayos, p=0.3)
    print("\n2. Binomial(n=10, p=0.3):")
    binomial = Binomial(10, 0.3)  # Crea distribución
    print(f"PMF(3) = {binomial.pmf(3):.4f}")  # Probabilidad de exactamente 3 éxitos
    print(f"CDF(3) = {binomial.cdf(3):.4f}")  # Probabilidad de 3 o menos éxitos
    print(f"Media = {binomial.mean():.1f}, Varianza = {binomial.variance():.2f}")
    print(f"Muestra: {binomial.sample(5)}")  # 5 simulaciones
    binomial.plot(0, 10)  # Gráfico de la distribución
    
    # 3. Ejemplo con distribución de Poisson (λ=2.5 eventos por intervalo)
    print("\n3. Poisson(λ=2.5):")
    poisson = Poisson(2.5)  # Crea distribución
    print(f"PMF(3) = {poisson.pmf(3):.4f}")  # Probabilidad de exactamente 3 eventos
    print(f"CDF(3) = {poisson.cdf(3):.4f}")  # Probabilidad de 3 o menos eventos
    print(f"Media = {poisson.mean():.1f}, Varianza = {poisson.variance():.2f}")
    print(f"Muestra: {poisson.sample(5)}")  # 5 simulaciones
    poisson.plot(0, 10)  # Gráfico de la distribución
    
    # 4. Ejemplo con distribución normal estándar (μ=0, σ=1)
    print("\n4. Normal(μ=0, σ=1):")
    normal = Normal(0, 1)  # Crea distribución
    print(f"PDF(0) = {normal.pdf(0):.4f}")  # Densidad en la media
    print(f"CDF(0) = {normal.cdf(0):.4f}")  # Probabilidad acumulada en la media
    print(f"Media = {normal.mean():.1f}, Varianza = {normal.variance():.2f}")
    print(f"Muestra: {normal.sample(5)}")  # 5 valores simulados
    normal.plot(-4, 4)  # Gráfico de la distribución
    
    # 5. Ejemplo con distribución exponencial (λ=1.5)
    print("\n5. Exponencial(λ=1.5):")
    exponential = Exponential(1.5)  # Crea distribución
    print(f"PDF(1) = {exponential.pdf(1):.4f}")  # Densidad en x=1
    print(f"CDF(1) = {exponential.cdf(1):.4f}")  # Probabilidad acumulada en x=1
    print(f"Media = {exponential.mean():.3f}, Varianza = {exponential.variance():.3f}")
    print(f"Muestra: {exponential.sample(5)}")  # 5 valores simulados
    exponential.plot(0, 5)  # Gráfico de la distribución
    
    # 6. Ejemplo con distribución empírica
    print("\n6. Distribución Empírica:")
    data = [1.2, 1.5, 2.1, 2.1, 2.1, 2.8, 3.0, 3.2, 3.9, 4.0]  # Datos de ejemplo
    empirical = EmpiricalDistribution(data)  # Crea distribución empírica
    print(f"Datos: {data}")
    print(f"PDF(2.1) = {empirical.pdf(2.1):.4f}")  # Densidad estimada en 2.1
    print(f"CDF(2.5) = {empirical.cdf(2.5):.4f}")  # Proporción ≤ 2.5
    print(f"Media = {empirical.mean():.3f}, Varianza = {empirical.variance():.3f}")
    print(f"Muestra: {empirical.sample(5)}")  # 5 muestras de los datos
    
    # Gráfico combinado para la distribución empírica
    plt.hist(data, bins=5, density=True, alpha=0.5, label='Histograma')  # Histograma
    x_vals = np.linspace(min(data)-1, max(data)+1, 100)  # Rango para KDE
    if empirical.type == DistributionType.CONTINUOUS:
        plt.plot(x_vals, [empirical.pdf(x) for x in x_vals], label='KDE')  # Curva KDE
    plt.title('Distribución Empírica')  # Título
    plt.xlabel('Valor')  # Etiqueta eje X
    plt.ylabel('Densidad')  # Etiqueta eje Y
    plt.legend()  # Leyenda
    plt.grid(True)  # Cuadrícula
    plt.show()  # Mostrar gráfico