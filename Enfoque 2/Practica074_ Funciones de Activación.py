# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 17:39:10 2025

@author: elvin
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class FuncionesActivacion:
    def __init__(self):
        """Inicializa los valores para graficar las funciones"""
        self.x = np.linspace(-5, 5, 500)  # Rango de valores de entrada
    
    # ------------------------------------------
    # FUNCIONES DE ACTIVACIÓN
    # ------------------------------------------
    
    def sigmoide(self, x):
        """Función Sigmoide: Transforma valores al rango (0, 1)"""
        return 1 / (1 + np.exp(-x))
    
    def tanh(self, x):
        """Función Tangente Hiperbólica: Transforma valores al rango (-1, 1)"""
        return np.tanh(x)
    
    def relu(self, x):
        """Función ReLU (Rectified Linear Unit): Devuelve el máximo entre 0 y x"""
        return np.maximum(0, x)
    
    def leaky_relu(self, x, alpha=0.1):
        """Versión mejorada de ReLU que permite pequeños valores negativos"""
        return np.where(x > 0, x, alpha * x)
    
    def softmax(self, x):
        """Usada para problemas de clasificación múltiple, normaliza salidas a probabilidades"""
        exps = np.exp(x - np.max(x))  # Estabilidad numérica
        return exps / np.sum(exps)
    
    # ------------------------------------------
    # DERIVADAS (Para backpropagation)
    # ------------------------------------------
    
    def derivada_sigmoide(self, x):
        """Derivada de la función Sigmoide"""
        s = self.sigmoide(x)
        return s * (1 - s)
    
    def derivada_tanh(self, x):
        """Derivada de la función Tanh"""
        return 1 - np.tanh(x)**2
    
    def derivada_relu(self, x):
        """Derivada de la función ReLU"""
        return np.where(x > 0, 1, 0)
    
    def derivada_leaky_relu(self, x, alpha=0.1):
        """Derivada de Leaky ReLU"""
        return np.where(x > 0, 1, alpha)
    
    # ------------------------------------------
    # VISUALIZACIÓN
    # ------------------------------------------
    
    def graficar_funciones(self):
        """Crea una figura con las gráficas de todas las funciones de activación"""
        fig = plt.figure(figsize=(12, 8))
        gs = GridSpec(2, 3, figure=fig)
        
        # Configuración común para los subplots
        config_plots = {
            'xlabel': 'Input (x)',
            'ylabel': 'Output',
            'grid': True,
            'xlim': (-5, 5),
            'ylim': (-1.5, 1.5)  # Ajustado para visualizar mejor
        }
        
        # 1. Sigmoide
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(self.x, self.sigmoide(self.x), label='Sigmoide', color='blue')
        ax1.plot(self.x, self.derivada_sigmoide(self.x), label='Derivada', linestyle='--', color='red')
        ax1.set_title('Sigmoide y su Derivada', pad=10)
        ax1.legend()
        
        # 2. Tanh
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.plot(self.x, self.tanh(self.x), label='Tanh', color='green')
        ax2.plot(self.x, self.derivada_tanh(self.x), label='Derivada', linestyle='--', color='orange')
        ax2.set_title('Tanh y su Derivada', pad=10)
        ax2.legend()
        
        # 3. ReLU
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.plot(self.x, self.relu(self.x), label='ReLU', color='purple')
        ax3.plot(self.x, self.derivada_relu(self.x), label='Derivada', linestyle='--', color='brown')
        ax3.set_title('ReLU y su Derivada', pad=10)
        ax3.legend()
        
        # 4. Leaky ReLU
        ax4 = fig.add_subplot(gs[1, 0])
        ax4.plot(self.x, self.leaky_relu(self.x), label='Leaky ReLU (α=0.1)', color='teal')
        ax4.plot(self.x, self.derivada_leaky_relu(self.x), label='Derivada', linestyle='--', color='magenta')
        ax4.set_title('Leaky ReLU y su Derivada', pad=10)
        ax4.legend()
        
        # 5. Softmax (ejemplo con 3 valores)
        ax5 = fig.add_subplot(gs[1, 1:])
        sample_input = np.array([1.0, 2.0, 3.0])
        output = self.softmax(sample_input)
        
        bars = ax5.bar(range(len(output)), output, color=['blue', 'green', 'red'])
        ax5.set_title('Softmax (Ejemplo con inputs [1.0, 2.0, 3.0])', pad=10)
        ax5.set_xticks(range(len(output)))
        ax5.set_xticklabels(['Input 1', 'Input 2', 'Input 3'])
        ax5.set_ylabel('Probabilidad')
        
        # Añadir valores en las barras
        for bar in bars:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom')
        
        # Aplicar configuración común
        for ax in [ax1, ax2, ax3, ax4]:
            for key, value in config_plots.items():
                getattr(ax, f'set_{key}')(value)
        
        plt.tight_layout()
        plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    print("➡️ Visualización de Funciones de Activación en Redes Neuronales")
    activaciones = FuncionesActivacion()
    activaciones.graficar_funciones()
    
    # Demostración práctica
    print("\n🔍 Ejemplo Práctico:")
    valores = np.array([-2.0, -0.5, 0.0, 0.5, 2.0])
    print("Valores de entrada:", valores)
    print("Sigmoide:", np.round(activaciones.sigmoide(valores), 4))
    print("Tanh:", np.round(activaciones.tanh(valores), 4))
    print("ReLU:", np.round(activaciones.relu(valores), 4))
    print("Leaky ReLU:", np.round(activaciones.leaky_relu(valores), 4))
    print("Softmax (para [1.0, 2.0, 3.0]):", np.round(activaciones.softmax(np.array([1.0, 2.0, 3.0])), 4))