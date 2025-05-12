# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:46:43 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import numpy as np  # Operaciones numéricas y manejo de arrays
from scipy.stats import norm, beta, dirichlet  # Distribuciones probabilísticas comunes
import matplotlib.pyplot as plt  # Biblioteca para graficar

class AprendizajeBayesiano:
    """
    Clase para realizar aprendizaje bayesiano con modelos conjugados.
    Contiene métodos para actualización y visualización de distribuciones.
    """

    def __init__(self):
        # Inicializar historial para seguimiento opcional de priors y posteriors
        self.historial_priors = []  # Lista de parámetros prior
        self.historial_posteriors = []  # Lista de parámetros posterior
    
    def actualizacion_normal(self, data, mu_prior=0, sigma_prior=1, sigma_likelihood=1):
        """
        Actualiza la distribución normal conjugada dado un prior y datos observados.
        
        Args:
            data: Datos observados (array de números reales)
            mu_prior: Media del prior normal
            sigma_prior: Desviación estándar del prior
            sigma_likelihood: Desviación estándar conocida de los datos
        
        Returns:
            Tupla con la media y desviación estándar posterior
        """
        n = len(data)  # Número de datos observados
        
        # Calcular varianzas una sola vez por eficiencia
        sigma_likelihood_sq = sigma_likelihood**2  # Varianza del likelihood
        sigma_prior_sq = sigma_prior**2  # Varianza del prior
        
        # Calcular media posterior con fórmula conjugada
        mu_posterior = (mu_prior/sigma_prior_sq + np.sum(data)/sigma_likelihood_sq) / \
                       (1/sigma_prior_sq + n/sigma_likelihood_sq)
        
        # Calcular desviación estándar posterior
        sigma_posterior = np.sqrt(1/(1/sigma_prior_sq + n/sigma_likelihood_sq))
        
        return mu_posterior, sigma_posterior  # Retornar parámetros actualizados
    
    def actualizacion_binomial(self, data, alpha_prior=1, beta_prior=1):
        """
        Actualiza los parámetros de una distribución Beta conjugada a una Binomial.
        
        Args:
            data: Lista o array de 1s (éxito) y 0s (fracaso)
            alpha_prior: Parámetro alpha del prior Beta
            beta_prior: Parámetro beta del prior Beta
        
        Returns:
            Tupla con los nuevos parámetros alpha y beta
        """
        n_éxitos = np.sum(data)  # Sumar los éxitos (valores 1)
        n_fracasos = len(data) - n_éxitos  # Fracasos = total - éxitos
        
        # Actualizar parámetros con fórmula conjugada
        alpha_posterior = alpha_prior + n_éxitos
        beta_posterior = beta_prior + n_fracasos
        
        return alpha_posterior, beta_posterior  # Retornar nuevos parámetros
    
    def actualizacion_multinomial(self, counts, alpha_prior):
        """
        Actualiza los parámetros de una distribución Dirichlet conjugada a una Multinomial.
        
        Args:
            counts: Array con conteos por categoría
            alpha_prior: Array de parámetros Dirichlet prior
        
        Returns:
            Array con los nuevos parámetros de la Dirichlet posterior
        """
        return alpha_prior + counts  # Sumar conteos al prior y retornar
    
    def graficar_actualizacion(self, prior_params, posterior_params, dist_type='normal'):
        """
        Grafica la distribución prior y posterior para comparación visual.
        
        Args:
            prior_params: Parámetros de la prior
            posterior_params: Parámetros de la posterior
            dist_type: Tipo de distribución ('normal' o 'beta')
        """
        plt.figure(figsize=(10, 4))  # Crear figura de tamaño ancho
        
        if dist_type == 'normal':
            x = np.linspace(-3, 3, 1000)  # Rango continuo para normal
            prior = norm(prior_params[0], prior_params[1]).pdf(x)  # PDF del prior
            posterior = norm(posterior_params[0], posterior_params[1]).pdf(x)  # PDF del posterior
            plt.plot(x, prior, 'r-', label='Prior')  # Graficar prior en rojo
            plt.plot(x, posterior, 'b-', label='Posterior')  # Graficar posterior en azul
            plt.title('Actualización Bayesiana - Distribución Normal')  # Título del gráfico
        
        elif dist_type == 'beta':
            x = np.linspace(0, 1, 1000)  # Rango [0,1] para la beta
            prior = beta(prior_params[0], prior_params[1]).pdf(x)  # PDF del prior beta
            posterior = beta(posterior_params[0], posterior_params[1]).pdf(x)  # PDF del posterior beta
            plt.plot(x, prior, 'r-', label='Prior')  # Graficar prior en rojo
            plt.plot(x, posterior, 'b-', label='Posterior')  # Graficar posterior en azul
            plt.title('Actualización Bayesiana - Distribución Beta')  # Título
        
        plt.xlabel('Valor')  # Etiqueta del eje x
        plt.ylabel('Densidad de Probabilidad')  # Etiqueta del eje y
        plt.legend()  # Mostrar leyenda
        plt.grid(True)  # Activar cuadrícula
        plt.show()  # Mostrar gráfico

# Bloque de ejecución principal
if __name__ == "__main__":
    # Crear instancia del aprendiz bayesiano
    bayes = AprendizajeBayesiano()
    
    # === Ejemplo 1: Normal ===
    print("=== Ejemplo 1: Actualización Normal ===")
    data_normal = np.random.normal(1.0, 1, 100)  # Datos simulados de N(1, 1)
    mu_post, sigma_post = bayes.actualizacion_normal(data_normal, mu_prior=0, sigma_prior=1)  # Actualizar posterior
    print(f"Posterior: μ = {mu_post:.2f}, σ = {sigma_post:.2f}")  # Mostrar resultados
    bayes.graficar_actualizacion((0, 1), (mu_post, sigma_post), 'normal')  # Graficar
    
    # === Ejemplo 2: Binomial ===
    print("\n=== Ejemplo 2: Actualización Binomial ===")
    data_binom = np.random.binomial(1, 0.7, 100)  # Datos simulados con p=0.7
    alpha_post, beta_post = bayes.actualizacion_binomial(data_binom)  # Actualizar posterior
    print(f"Posterior: α = {alpha_post}, β = {beta_post}")  # Mostrar resultados
    bayes.graficar_actualizacion((1, 1), (alpha_post, beta_post), 'beta')  # Graficar
    
    # === Ejemplo 3: Multinomial ===
    print("\n=== Ejemplo 3: Actualización Multinomial ===")
    data_multinom = np.random.choice(3, 100, p=[0.2, 0.3, 0.5])  # Simular datos categóricos
    counts = np.bincount(data_multinom, minlength=3)  # Contar ocurrencias por categoría
    alpha_prior = np.ones(3)  # Prior uniforme Dirichlet(1,1,1)
    alpha_post = bayes.actualizacion_multinomial(counts, alpha_prior)  # Actualizar posterior
    print(f"Posterior: α = {alpha_post}")  # Mostrar resultados
    
    # Graficar comparación de parámetros
    plt.figure(figsize=(6, 4))
    categories = ['Categoría 1', 'Categoría 2', 'Categoría 3']  # Nombres de categorías
    plt.bar(categories, alpha_prior, alpha=0.5, label='Prior')  # Graficar prior
    plt.bar(categories, alpha_post, alpha=0.5, label='Posterior')  # Graficar posterior
    plt.title('Actualización Bayesiana - Distribución Dirichlet')  # Título del gráfico
    plt.ylabel('Parámetros α')  # Etiqueta eje y
    plt.legend()  # Mostrar leyenda
    plt.show()  # Mostrar gráfico
