

# Importación de librerías necesarias
import numpy as np  # Para operaciones numéricas
from typing import Dict, Tuple, List  # Para anotaciones de tipo
from itertools import product  # Para generar combinaciones
from collections import defaultdict  # Para diccionarios con valores por defecto

class ConditionalIndependence:
    def __init__(self):
        """Inicializa el verificador de independencia condicional"""
        # Diccionario para contar frecuencias conjuntas de (X,Y,Z)
        self.joint_counts = defaultdict(int)
        # Diccionario para contar frecuencias marginales
        self.marginal_counts = defaultdict(int)
        # Contador total de observaciones
        self.total_observations = 0
    
    def add_observation(self, x: str, y: str, z: str) -> None:
        """
        Registra una observación de las variables X, Y y Z.
        
        Args:
            x: Valor de la variable X
            y: Valor de la variable Y 
            z: Valor de la variable Z (condicionante)
        """
        # Incrementa el contador para la combinación (X,Y,Z)
        self.joint_counts[(x, y, z)] += 1
        # Incrementa el contador marginal para (X,Z)
        self.marginal_counts[(x, z)] += 1
        # Incrementa el contador marginal para (Y,Z)
        self.marginal_counts[(y, z)] += 1
        # Incrementa el contador marginal para Z
        self.marginal_counts[z] += 1
        # Incrementa el contador total
        self.total_observations += 1
    
    def joint_probability(self, x: str, y: str, z: str) -> float:
        """
        Calcula la probabilidad conjunta P(X=x, Y=y, Z=z).
        
        Args:
            x: Valor de X
            y: Valor de Y
            z: Valor de Z
            
        Returns:
            Probabilidad conjunta estimada
        """
        # Maneja caso cuando no hay observaciones
        if self.total_observations == 0:
            return 0.0
        # Calcula P(X,Y,Z) = conteo(X,Y,Z) / total_observaciones
        return self.joint_counts[(x, y, z)] / self.total_observations
    
    def conditional_probability(self, a: str, b: str, z: str) -> float:
        """
        Calcula la probabilidad condicional P(A=a|B=b, Z=z).
        
        Args:
            a: Valor de A
            b: Valor de B
            z: Valor de Z
            
        Returns:
            Probabilidad condicional estimada
        """
        # Maneja caso cuando no hay observaciones para (B,Z)
        if self.marginal_counts[(b, z)] == 0:
            return 0.0
        # Calcula P(A|B,Z) = P(A,B,Z) / P(B,Z)
        return self.joint_counts[(a, b, z)] / self.marginal_counts[(b, z)]
    
    def check_conditional_independence(self, x: str, y: str, z: str, 
                                   threshold: float = 0.01) -> bool:
        """
        Verifica si X es independiente de Y dado Z comparando probabilidades.
        
        Args:
            x: Nombre de variable X
            y: Nombre de variable Y
            z: Nombre de variable Z (condicionante)
            threshold: Umbral de diferencia aceptable
            
        Returns:
            True si son condicionalmente independientes, False en caso contrario
        """
        # Obtener todos los valores únicos observados para cada variable
        x_vals = set(v[0] for v in self.joint_counts.keys())
        y_vals = set(v[1] for v in self.joint_counts.keys())
        z_vals = set(v[2] for v in self.joint_counts.keys())
        
        # Verificar para cada valor de Z
        for zi in z_vals:
            # Verificar todas las combinaciones de X e Y
            for xi, yi in product(x_vals, y_vals):
                # Calcular P(X,Y|Z) = P(X,Y,Z)/P(Z)
                p_xy_z = self.joint_probability(xi, yi, zi) / \
                         (self.marginal_counts[zi] / self.total_observations)
                
                # Calcular P(X|Z)*P(Y|Z)
                p_x_z = self.conditional_probability(xi, z, zi)
                p_y_z = self.conditional_probability(yi, z, zi)
                p_product = p_x_z * p_y_z
                
                # Comparar con umbral de tolerancia
                if abs(p_xy_z - p_product) > threshold:
                    print(f"Falla independencia para X={xi}, Y={yi}, Z={zi}:")
                    print(f"P(X,Y|Z)={p_xy_z:.4f} != P(X|Z)*P(Y|Z)={p_product:.4f}")
                    return False
        return True
    
    def chi_squared_test(self, x: str, y: str, z: str, alpha: float = 0.05) -> bool:
        """
        Realiza test estadístico chi-cuadrado de independencia condicional.
        
        Args:
            x: Nombre de variable X
            y: Nombre de variable Y
            z: Nombre de variable Z (condicionante)
            alpha: Nivel de significancia (default 0.05)
            
        Returns:
            True si no se rechaza H0 (independencia), False si se rechaza
        """
        from scipy.stats import chi2_contingency
        
        # Obtener valores únicos ordenados para cada variable
        x_vals = sorted(set(v[0] for v in self.joint_counts.keys()))
        y_vals = sorted(set(v[1] for v in self.joint_counts.keys()))
        z_vals = sorted(set(v[2] for v in self.joint_counts.keys()))
        
        # Realizar test para cada valor de Z
        for zi in z_vals:
            # Construir tabla de contingencia para Z=zi
            contingency_table = []
            for xi in x_vals:
                row = []
                for yi in y_vals:
                    row.append(self.joint_counts[(xi, yi, zi)])
                contingency_table.append(row)
            
            # Realizar test chi-cuadrado
            chi2, p, dof, expected = chi2_contingency(contingency_table)
            
            # Comparar p-valor con nivel de significancia
            if p < alpha:
                print(f"Se rechaza independencia para Z={zi}: p-value={p:.4f}")
                return False
        
        return True


# Ejemplo de uso principal
if __name__ == "__main__":
    print("=== Verificación de Independencia Condicional ===\n")
    
    # Crear instancia del verificador
    ci = ConditionalIndependence()
    
    # Datos de ejemplo donde X e Y son independientes dado Z
    data_independent = [
        ('si', 'si', 'lluvia'), ('si', 'si', 'lluvia'), ('si', 'no', 'lluvia'),
        ('no', 'si', 'lluvia'), ('no', 'no', 'lluvia'), ('no', 'no', 'lluvia'),
        ('si', 'si', 'soleado'), ('si', 'no', 'soleado'), ('si', 'no', 'soleado'),
        ('no', 'si', 'soleado'), ('no', 'si', 'soleado'), ('no', 'no', 'soleado')
    ]
    
    # Datos donde X e Y NO son independientes dado Z
    data_dependent = [
        ('si', 'si', 'lluvia'), ('si', 'si', 'lluvia'), ('si', 'no', 'lluvia'),
        ('no', 'no', 'lluvia'), ('no', 'no', 'lluvia'), ('no', 'no', 'lluvia'),
        ('si', 'no', 'soleado'), ('si', 'no', 'soleado'), ('si', 'no', 'soleado'),
        ('no', 'si', 'soleado'), ('no', 'si', 'soleado'), ('no', 'no', 'soleado')
    ]
    
    # Caso 1: Verificar independencia condicional
    print("1. Caso con independencia condicional:")
    for obs in data_independent:
        ci.add_observation(*obs)
    
    print("Verificación por fórmula de probabilidad:")
    is_indep = ci.check_conditional_independence('X', 'Y', 'Z')
    print(f"¿X es independiente de Y dado Z? {is_indep}")
    
    print("\nTest Chi-cuadrado:")
    chi_result = ci.chi_squared_test('X', 'Y', 'Z')
    print(f"¿No se rechaza independencia? {chi_result}")
    
    # Caso 2: Verificar dependencia condicional
    print("\n2. Caso SIN independencia condicional:")
    ci_dep = ConditionalIndependence()
    for obs in data_dependent:
        ci_dep.add_observation(*obs)
    
    print("Verificación por fórmula de probabilidad:")
    is_indep = ci_dep.check_conditional_independence('X', 'Y', 'Z')
    print(f"¿X es independiente de Y dado Z? {is_indep}")
    
    print("\nTest Chi-cuadrado:")
    chi_result = ci_dep.chi_squared_test('X', 'Y', 'Z')
    print(f"¿No se rechaza independencia? {chi_result}")