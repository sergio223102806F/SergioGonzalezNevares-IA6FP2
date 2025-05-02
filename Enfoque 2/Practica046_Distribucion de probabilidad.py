

# Importación de librerías necesarias
import numpy as np  # Para operaciones numéricas
import matplotlib.pyplot as plt  # Para visualización gráfica
from math import factorial, exp, sqrt, pi  # Funciones matemáticas
from typing import Dict, List, Tuple, Union  # Para anotaciones de tipo
from collections import defaultdict  # Para diccionarios con valores por defecto
from enum import Enum  # Para enumeraciones

# Enumeración para tipos de distribuciones
class DistributionType(Enum):
    DISCRETE = 1  # Distribuciones discretas
    CONTINUOUS = 2  # Distribuciones continuas

# Clase base abstracta para distribuciones de probabilidad
class ProbabilityDistribution:
    def __init__(self):
        """Inicializa la clase base para distribuciones"""
        self.type = None  # Será definido por las clases hijas
    
    # Métodos abstractos que deben ser implementados por las clases hijas
    def pmf(self, x: Union[int, float]) -> float:
        """Función de masa de probabilidad (para discretas)"""
        raise NotImplementedError("Debe implementarse en subclases")
    
    def pdf(self, x: float) -> float:
        """Función de densidad de probabilidad (para continuas)"""
        raise NotImplementedError("Debe implementarse en subclases")
    
    def cdf(self, x: Union[int, float]) -> float:
        """Función de distribución acumulativa"""
        raise NotImplementedError("Debe implementarse en subclases")
    
    def mean(self) -> float:
        """Calcula la media/valor esperado"""
        raise NotImplementedError("Debe implementarse en subclases")
    
    def variance(self) -> float:
        """Calcula la varianza"""
        raise NotImplementedError("Debe implementarse en subclases")
    
    def sample(self, n: int = 1) -> List[float]:
        """Genera muestras aleatorias de la distribución"""
        raise NotImplementedError("Debe implementarse en subclases")
    
    # Método para graficar la distribución
    def plot(self, start: float, end: float, num_points: int = 100):
        """Grafica la PMF o PDF según el tipo de distribución"""
        if self.type == DistributionType.DISCRETE:
            # Para discretas: gráfico de bastones
            x_vals = np.arange(start, end + 1)  # Valores enteros
            y_vals = [self.pmf(x) for x in x_vals]  # PMF para cada x
            plt.stem(x_vals, y_vals, use_line_collection=True)
            plt.title('Función de Masa de Probabilidad (PMF)')
        else:
            # Para continuas: gráfico de línea suave
            x_vals = np.linspace(start, end, num_points)  # Puntos equiespaciados
            y_vals = [self.pdf(x) for x in x_vals]  # PDF para cada x
            plt.plot(x_vals, y_vals)
            plt.title('Función de Densidad de Probabilidad (PDF)')
        
        # Configuración común del gráfico
        plt.xlabel('x')
        plt.ylabel('Probabilidad')
        plt.grid(True)
        plt.show()

# Implementación de distribución uniforme discreta
class DiscreteUniform(ProbabilityDistribution):
    """Distribución uniforme discreta entre a y b (inclusive)"""
    def __init__(self, a: int, b: int):
        super().__init__()
        self.type = DistributionType.DISCRETE
        self.a = a  # Límite inferior
        self.b = b  # Límite superior
        self.n = b - a + 1  # Número de valores posibles
    
    def pmf(self, x: int) -> float:
        """Función de masa de probabilidad"""
        if x < self.a or x > self.b:
            return 0.0  # Probabilidad 0 fuera del rango
        return 1.0 / self.n  # Probabilidad uniforme
    
    def cdf(self, x: int) -> float:
        """Función de distribución acumulativa"""
        if x < self.a:
            return 0.0  # Acumulada 0 antes del rango
        elif x > self.b:
            return 1.0  # Acumulada 1 después del rango
        return (x - self.a + 1) / self.n  # Lineal entre a y b
    
    def mean(self) -> float:
        """Calcula la media (a + b)/2"""
        return (self.a + self.b) / 2
    
    def variance(self) -> float:
        """Calcula la varianza ((n^2 - 1)/12)"""
        return (self.n**2 - 1) / 12
    
    def sample(self, n: int = 1) -> List[int]:
        """Genera n muestras aleatorias"""
        return np.random.randint(self.a, self.b + 1, n).tolist()

# Implementación de distribución binomial
class Binomial(ProbabilityDistribution):
    """Distribución binomial (n ensayos, p probabilidad de éxito)"""
    def __init__(self, n: int, p: float):
        super().__init__()
        self.type = DistributionType.DISCRETE
        self.n = n  # Número de ensayos
        self.p = p  # Probabilidad de éxito
        self.q = 1 - p  # Probabilidad de fracaso
    
    def pmf(self, k: int) -> float:
        """Función de masa de probabilidad"""
        if k < 0 or k > self.n:
            return 0.0  # Probabilidad 0 fuera de rango
        # Fórmula binomial: combinaciones(n,k) * p^k * q^(n-k)
        return (factorial(self.n) / (factorial(k) * factorial(self.n - k))) * \
               (self.p**k) * (self.q**(self.n - k))
    
    def cdf(self, k: int) -> float:
        """Función de distribución acumulativa"""
        return sum(self.pmf(i) for i in range(0, k + 1))  # Suma de PMFs
    
    def mean(self) -> float:
        """Media (n*p)"""
        return self.n * self.p
    
    def variance(self) -> float:
        """Varianza (n*p*q)"""
        return self.n * self.p * self.q
    
    def sample(self, n: int = 1) -> List[int]:
        """Genera n muestras aleatorias"""
        return np.random.binomial(self.n, self.p, n).tolist()

# Implementación de distribución de Poisson
class Poisson(ProbabilityDistribution):
    """Distribución de Poisson (λ = tasa de ocurrencia)"""
    def __init__(self, lam: float):
        super().__init__()
        self.type = DistributionType.DISCRETE
        self.lam = lam  # Parámetro lambda (tasa)
    
    def pmf(self, k: int) -> float:
        """Función de masa de probabilidad"""
        if k < 0:
            return 0.0  # Probabilidad 0 para k negativo
        # Fórmula de Poisson: (λ^k * e^-λ) / k!
        return (self.lam**k * exp(-self.lam)) / factorial(k)
    
    def cdf(self, k: int) -> float:
        """Función de distribución acumulativa"""
        return sum(self.pmf(i) for i in range(0, k + 1))  # Suma de PMFs
    
    def mean(self) -> float:
        """Media (λ)"""
        return self.lam
    
    def variance(self) -> float:
        """Varianza (λ)"""
        return self.lam
    
    def sample(self, n: int = 1) -> List[int]:
        """Genera n muestras aleatorias"""
        return np.random.poisson(self.lam, n).tolist()

# Implementación de distribución normal
class Normal(ProbabilityDistribution):
    """Distribución normal (μ = media, σ = desviación estándar)"""
    def __init__(self, mu: float = 0, sigma: float = 1):
        super().__init__()
        self.type = DistributionType.CONTINUOUS
        self.mu = mu  # Media
        self.sigma = sigma  # Desviación estándar
    
    def pdf(self, x: float) -> float:
        """Función de densidad de probabilidad"""
        # Fórmula normal: (1/(σ√(2π))) * e^(-(x-μ)²/(2σ²))
        return (1 / (self.sigma * sqrt(2 * pi))) * \
               exp(-0.5 * ((x - self.mu) / self.sigma)**2)
    
    def cdf(self, x: float) -> float:
        """Función de distribución acumulativa"""
        from scipy.stats import norm  # Importación diferida
        return norm.cdf(x, self.mu, self.sigma)  # Usa scipy para precisión
    
    def mean(self) -> float:
        """Media (μ)"""
        return self.mu
    
    def variance(self) -> float:
        """Varianza (σ²)"""
        return self.sigma**2
    
    def sample(self, n: int = 1) -> List[float]:
        """Genera n muestras aleatorias"""
        return np.random.normal(self.mu, self.sigma, n).tolist()

# Implementación de distribución exponencial
class Exponential(ProbabilityDistribution):
    """Distribución exponencial (λ = tasa)"""
    def __init__(self, lam: float = 1):
        super().__init__()
        self.type = DistributionType.CONTINUOUS
        self.lam = lam  # Parámetro lambda (tasa)
    
    def pdf(self, x: float) -> float:
        """Función de densidad de probabilidad"""
        if x < 0:
            return 0.0  # Probabilidad 0 para x negativo
        # Fórmula exponencial: λ * e^(-λx)
        return self.lam * exp(-self.lam * x)
    
    def cdf(self, x: float) -> float:
        """Función de distribución acumulativa"""
        if x < 0:
            return 0.0  # Acumulada 0 para x negativo
        # Fórmula acumulativa: 1 - e^(-λx)
        return 1 - exp(-self.lam * x)
    
    def mean(self) -> float:
        """Media (1/λ)"""
        return 1 / self.lam
    
    def variance(self) -> float:
        """Varianza (1/λ²)"""
        return 1 / (self.lam**2)
    
    def sample(self, n: int = 1) -> List[float]:
        """Genera n muestras aleatorias"""
        return np.random.exponential(1/self.lam, n).tolist()

# Implementación de distribución empírica
class EmpiricalDistribution(ProbabilityDistribution):
    """Distribución empírica a partir de datos observados"""
    def __init__(self, data: List[Union[int, float]]):
        super().__init__()
        self.data = np.array(data)  # Almacena los datos
        
        # Determina si es discreta (todos enteros) o continua
        if all(isinstance(x, int) for x in data):
            self.type = DistributionType.DISCRETE
            # Para discretas: conteo de frecuencias
            self.counts = defaultdict(int)
            for x in data:
                self.counts[x] += 1
            self.total = len(data)
        else:
            self.type = DistributionType.CONTINUOUS
            # Para continuas: estimación de densidad kernel (KDE)
            from scipy.stats import gaussian_kde
            self.kde = gaussian_kde(data)
    
    def pmf(self, x: int) -> float:
        """Función de masa de probabilidad (solo para discretas)"""
        if self.type != DistributionType.DISCRETE:
            raise ValueError("PMF solo para distribuciones discretas")
        return self.counts.get(x, 0) / self.total  # Frecuencia relativa
    
    def pdf(self, x: float) -> float:
        """Función de densidad (solo para continuas)"""
        if self.type != DistributionType.CONTINUOUS:
            raise ValueError("PDF solo para distribuciones continuas")
        return self.kde.evaluate(x)[0]  # Estimación KDE
    
    def cdf(self, x: float) -> float:
        """Función de distribución acumulativa empírica"""
        return np.mean(self.data <= x)  # Proporción de datos ≤ x
    
    def mean(self) -> float:
        """Media muestral"""
        return np.mean(self.data)
    
    def variance(self) -> float:
        """Varianza muestral"""
        return np.var(self.data)
    
    def sample(self, n: int = 1) -> List[float]:
        """Muestreo aleatorio de los datos (con reemplazo)"""
        return np.random.choice(self.data, n).tolist()

# Ejemplos de uso
if __name__ == "__main__":
    print("=== Distribuciones de Probabilidad ===\n")
    
    # 1. Ejemplo con distribución uniforme discreta (dado de 6 caras)
    print("1. Uniforme Discreta (a=1, b=6):")
    uniform_disc = DiscreteUniform(1, 6)
    print(f"PMF(3) = {uniform_disc.pmf(3):.3f}")  # Probabilidad de sacar 3
    print(f"CDF(3) = {uniform_disc.cdf(3):.3f}")  # Probabilidad de sacar ≤3
    print(f"Media = {uniform_disc.mean():.1f}, Varianza = {uniform_disc.variance():.2f}")
    print(f"Muestra: {uniform_disc.sample(5)}")  # 5 lanzamientos simulados
    uniform_disc.plot(0, 7)  # Gráfico de la distribución
    
    # 2. Ejemplo con distribución binomial (10 ensayos, p=0.3)
    print("\n2. Binomial(n=10, p=0.3):")
    binomial = Binomial(10, 0.3)
    print(f"PMF(3) = {binomial.pmf(3):.4f}")  # Probabilidad de exactamente 3 éxitos
    print(f"CDF(3) = {binomial.cdf(3):.4f}")  # Probabilidad de 3 o menos éxitos
    print(f"Media = {binomial.mean():.1f}, Varianza = {binomial.variance():.2f}")
    print(f"Muestra: {binomial.sample(5)}")  # 5 simulaciones
    binomial.plot(0, 10)  # Gráfico de la distribución
    
    # 3. Ejemplo con distribución de Poisson (λ=2.5 eventos por intervalo)
    print("\n3. Poisson(λ=2.5):")
    poisson = Poisson(2.5)
    print(f"PMF(3) = {poisson.pmf(3):.4f}")  # Probabilidad de exactamente 3 eventos
    print(f"CDF(3) = {poisson.cdf(3):.4f}")  # Probabilidad de 3 o menos eventos
    print(f"Media = {poisson.mean():.1f}, Varianza = {poisson.variance():.2f}")
    print(f"Muestra: {poisson.sample(5)}")  # 5 simulaciones
    poisson.plot(0, 10)  # Gráfico de la distribución
    
    # 4. Ejemplo con distribución normal estándar (μ=0, σ=1)
    print("\n4. Normal(μ=0, σ=1):")
    normal = Normal(0, 1)
    print(f"PDF(0) = {normal.pdf(0):.4f}")  # Densidad en la media
    print(f"CDF(0) = {normal.cdf(0):.4f}")  # Probabilidad acumulada en la media
    print(f"Media = {normal.mean():.1f}, Varianza = {normal.variance():.2f}")
    print(f"Muestra: {normal.sample(5)}")  # 5 valores simulados
    normal.plot(-4, 4)  # Gráfico de la distribución
    
    # 5. Ejemplo con distribución exponencial (λ=1.5)
    print("\n5. Exponencial(λ=1.5):")
    exponential = Exponential(1.5)
    print(f"PDF(1) = {exponential.pdf(1):.4f}")  # Densidad en x=1
    print(f"CDF(1) = {exponential.cdf(1):.4f}")  # Probabilidad acumulada en x=1
    print(f"Media = {exponential.mean():.3f}, Varianza = {exponential.variance():.3f}")
    print(f"Muestra: {exponential.sample(5)}")  # 5 valores simulados
    exponential.plot(0, 5)  # Gráfico de la distribución
    
    # 6. Ejemplo con distribución empírica
    print("\n6. Distribución Empírica:")
    data = [1.2, 1.5, 2.1, 2.1, 2.1, 2.8, 3.0, 3.2, 3.9, 4.0]  # Datos de ejemplo
    empirical = EmpiricalDistribution(data)
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
    plt.title('Distribución Empírica')
    plt.xlabel('Valor')
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid(True)
    plt.show()