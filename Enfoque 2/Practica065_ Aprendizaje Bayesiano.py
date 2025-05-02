# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 15:46:43 2025

@author: elvin
"""

# Importación de bibliotecas necesarias
import numpy as np  # Operaciones numéricas y manejo de arrays
from scipy.stats import norm, beta, dirichlet  # Distribuciones probabilísticas
import matplotlib.pyplot as plt  # Visualización de resultados

class AprendizajeBayesiano:
    """
    Clase principal que implementa:
    - Actualización de distribuciones conjugadas
    - Inferencia paramétrica bayesiana
    - Visualización de priors/posteriors
    """

    def __init__(self):
        # Listas para guardar historial de distribuciones (uso opcional)
        self.historial_priors = []  # Almacena parámetros iniciales
        self.historial_posteriors = []  # Almacena parámetros actualizados
    
    def actualizacion_normal(self, data, mu_prior=0, sigma_prior=1, sigma_likelihood=1):
        """
        Actualización bayesiana para la media de una Normal con varianza conocida.
        Modelo conjugado Normal-Normal.
        
        Args:
            data: Array de observaciones
            mu_prior: Media de la distribución prior
            sigma_prior: Desviación estándar del prior
            sigma_likelihood: Desviación estándar conocida de los datos
            
        Returns:
            Tuple (mu_posterior, sigma_posterior): Parámetros actualizados
        """
        n = len(data)  # Número de observaciones
        
        # Pre-cálculo de varianzas (más eficiente)
        sigma_likelihood_sq = sigma_likelihood**2
        sigma_prior_sq = sigma_prior**2
        
        # Cálculo de la media posterior (fórmula conjugada)
        mu_posterior = (mu_prior/sigma_prior_sq + np.sum(data)/sigma_likelihood_sq) / \
                       (1/sigma_prior_sq + n/sigma_likelihood_sq)
        
        # Cálculo de la desviación estándar posterior
        sigma_posterior = np.sqrt(1/(1/sigma_prior_sq + n/sigma_likelihood_sq))
        
        return mu_posterior, sigma_posterior
    
    def actualizacion_binomial(self, data, alpha_prior=1, beta_prior=1):
        """
        Actualización bayesiana para distribución binomial.
        Modelo conjugado Beta-Binomial.
        
        Args:
            data: Array de éxitos (1) y fracasos (0)
            alpha_prior: Parámetro alpha de la Beta prior
            beta_prior: Parámetro beta de la Beta prior
            
        Returns:
            Tuple (alpha_posterior, beta_posterior): Parámetros actualizados
        """
        # Conteo de éxitos y fracasos
        n_éxitos = np.sum(data)  # Suma de 1s
        n_fracasos = len(data) - n_éxitos  # Total - éxitos
        
        # Fórmula de actualización conjugada
        alpha_posterior = alpha_prior + n_éxitos
        beta_posterior = beta_prior + n_fracasos
        
        return alpha_posterior, beta_posterior
    
    def actualizacion_multinomial(self, counts, alpha_prior):
        """
        Actualización bayesiana para distribución multinomial.
        Modelo conjugado Dirichlet-Multinomial.
        
        Args:
            counts: Array de conteos por categoría
            alpha_prior: Parámetros de la Dirichlet prior
            
        Returns:
            Array: Parámetros de la Dirichlet posterior
        """
        # Fórmula simple de actualización
        return alpha_prior + counts
    
    def graficar_actualizacion(self, prior_params, posterior_params, dist_type='normal'):
        """
        Visualiza comparación entre distribuciones prior y posterior.
        
        Args:
            prior_params: Parámetros de la distribución prior
            posterior_params: Parámetros de la distribución posterior
            dist_type: Tipo de distribución ('normal' o 'beta')
        """
        plt.figure(figsize=(10, 4))  # Tamaño de figura
        
        if dist_type == 'normal':
            # Crear rango de valores para graficar
            x = np.linspace(-3, 3, 1000)
            
            # Calcular PDFs
            prior = norm(prior_params[0], prior_params[1]).pdf(x)
            posterior = norm(posterior_params[0], posterior_params[1]).pdf(x)
            
            # Graficar
            plt.plot(x, prior, 'r-', label='Prior')
            plt.plot(x, posterior, 'b-', label='Posterior')
            plt.title('Actualización Bayesiana - Distribución Normal')
            
        elif dist_type == 'beta':
            # Rango para distribución beta [0,1]
            x = np.linspace(0, 1, 1000)
            
            # Calcular PDFs
            prior = beta(prior_params[0], prior_params[1]).pdf(x)
            posterior = beta(posterior_params[0], posterior_params[1]).pdf(x)
            
            # Graficar
            plt.plot(x, prior, 'r-', label='Prior')
            plt.plot(x, posterior, 'b-', label='Posterior')
            plt.title('Actualización Bayesiana - Distribución Beta')
        
        # Configuración común de gráfico
        plt.xlabel('Valor')
        plt.ylabel('Densidad de Probabilidad')
        plt.legend()  # Mostrar leyenda
        plt.grid(True)  # Activar cuadrícula
        plt.show()

# Bloque principal de ejecución
if __name__ == "__main__":
    # 1. Instanciar el aprendiz bayesiano
    bayes = AprendizajeBayesiano()
    
    # Ejemplo 1: Actualización Normal
    print("=== Ejemplo 1: Actualización Normal ===")
    # Generar datos de una normal(μ=1, σ=1)
    data_normal = np.random.normal(1.0, 1, 100)
    
    # Prior inicial: creemos que μ≈0 con σ=1
    mu_post, sigma_post = bayes.actualizacion_normal(data_normal, mu_prior=0, sigma_prior=1)
    print(f"Posterior: μ = {mu_post:.2f}, σ = {sigma_post:.2f}")
    
    # Visualizar actualización
    bayes.graficar_actualizacion((0, 1), (mu_post, sigma_post), 'normal')
    
    # Ejemplo 2: Actualización Binomial
    print("\n=== Ejemplo 2: Actualización Binomial ===")
    # Generar datos binomiales (p=0.7)
    data_binom = np.random.binomial(1, 0.7, 100)
    
    # Prior uniforme Beta(1,1)
    alpha_post, beta_post = bayes.actualizacion_binomial(data_binom)
    print(f"Posterior: α = {alpha_post}, β = {beta_post}")
    
    # Visualizar
    bayes.graficar_actualizacion((1, 1), (alpha_post, beta_post), 'beta')
    
    # Ejemplo 3: Actualización Multinomial
    print("\n=== Ejemplo 3: Actualización Multinomial ===")
    # Generar datos categóricos con probabilidades [0.2, 0.3, 0.5]
    data_multinom = np.random.choice(3, 100, p=[0.2, 0.3, 0.5])
    counts = np.bincount(data_multinom, minlength=3)
    
    # Prior uniforme Dirichlet(1,1,1)
    alpha_prior = np.ones(3)
    alpha_post = bayes.actualizacion_multinomial(counts, alpha_prior)
    print(f"Posterior: α = {alpha_post}")
    
    # Visualización simplificada
    plt.figure(figsize=(6, 4))
    categories = ['Categoría 1', 'Categoría 2', 'Categoría 3']
    plt.bar(categories, alpha_prior, alpha=0.5, label='Prior')
    plt.bar(categories, alpha_post, alpha=0.5, label='Posterior')
    plt.title('Actualización Bayesiana - Distribución Dirichlet')
    plt.ylabel('Parámetros α')
    plt.legend()
    plt.show()