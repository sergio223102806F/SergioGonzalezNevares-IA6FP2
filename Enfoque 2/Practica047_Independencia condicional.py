# Importación de la librería numpy para operaciones numéricas avanzadas
import numpy as np

# Importación de tipos de datos para anotaciones de tipo (mejorar legibilidad del código)
from typing import Dict, Tuple, List

# Importación de la función product para generar producto cartesiano de conjuntos
from itertools import product

# Importación de defaultdict para diccionarios con valores por defecto
from collections import defaultdict


# Definición de la clase principal para verificar independencia condicional
class ConditionalIndependence:
    # Método constructor de la clase
    def __init__(self):
        """Inicializa el verificador de independencia condicional"""
        
        # Diccionario para contar frecuencias conjuntas de (X,Y,Z)
        # Formato: {(valor_x, valor_y, valor_z): conteo}
        self.joint_counts = defaultdict(int)
        
        # Diccionario para contar frecuencias marginales
        # Almacena conteos para: (X,Z), (Y,Z), y Z solo
        self.marginal_counts = defaultdict(int)
        
        # Contador total de observaciones registradas
        self.total_observations = 0

    # Método para agregar una nueva observación al modelo
    def add_observation(self, x: str, y: str, z: str) -> None:
        """
        Registra una observación de las variables X, Y y Z.
        
        Parámetros:
            x: Valor de la variable X (ej: 'si'/'no')
            y: Valor de la variable Y (ej: 'si'/'no')
            z: Valor de la variable Z (condicionante, ej: 'lluvia'/'soleado')
        """
        
        # Incrementa el contador para la combinación (X,Y,Z)
        self.joint_counts[(x, y, z)] += 1
        
        # Incrementa el contador marginal para (X,Z)
        self.marginal_counts[(x, z)] += 1
        
        # Incrementa el contador marginal para (Y,Z)
        self.marginal_counts[(y, z)] += 1
        
        # Incrementa el contador marginal para Z solo
        self.marginal_counts[z] += 1
        
        # Incrementa el contador total de observaciones
        self.total_observations += 1

    # Método para calcular probabilidad conjunta P(X=x, Y=y, Z=z)
    def joint_probability(self, x: str, y: str, z: str) -> float:
        """
        Calcula la probabilidad conjunta P(X=x, Y=y, Z=z).
        
        Parámetros:
            x: Valor de X
            y: Valor de Y
            z: Valor de Z
            
        Retorna:
            float: Probabilidad estimada (0 si no hay observaciones)
        """
        
        # Manejo de caso cuando no hay observaciones
        if self.total_observations == 0:
            return 0.0
            
        # Cálculo de la probabilidad conjunta como conteo(X,Y,Z)/total
        return self.joint_counts[(x, y, z)] / self.total_observations

    # Método para calcular probabilidad condicional P(A=a|B=b, Z=z)
    def conditional_probability(self, a: str, b: str, z: str) -> float:
        """
        Calcula la probabilidad condicional P(A=a|B=b, Z=z).
        
        Parámetros:
            a: Valor de A (variable objetivo)
            b: Valor de B (variable condicionante)
            z: Valor de Z (variable condicionante)
            
        Retorna:
            float: Probabilidad condicional estimada (0 si no hay datos)
        """
        
        # Manejo de caso cuando no hay observaciones para (B,Z)
        if self.marginal_counts[(b, z)] == 0:
            return 0.0
            
        # Cálculo de probabilidad condicional como P(A,B,Z)/P(B,Z)
        return self.joint_counts[(a, b, z)] / self.marginal_counts[(b, z)]

    # Método principal para verificar independencia condicional
    def check_conditional_independence(self, x: str, y: str, z: str, 
                                   threshold: float = 0.01) -> bool:
        """
        Verifica independencia condicional X⊥Y|Z comparando probabilidades.
        
        Parámetros:
            x: Nombre de variable X (solo para referencia)
            y: Nombre de variable Y (solo para referencia)
            z: Nombre de variable Z (condicionante)
            threshold: Umbral de diferencia aceptable (default 0.01)
            
        Retorna:
            bool: True si son independientes, False si no
        """
        
        # Obtención de valores únicos observados para cada variable
        x_vals = set(v[0] for v in self.joint_counts.keys())  # Valores de X
        y_vals = set(v[1] for v in self.joint_counts.keys())  # Valores de Y
        z_vals = set(v[2] for v in self.joint_counts.keys())  # Valores de Z
        
        # Iteración sobre cada valor posible de Z
        for zi in z_vals:
            # Generación de todas las combinaciones posibles de X e Y
            for xi, yi in product(x_vals, y_vals):
                # Cálculo de P(X,Y|Z) = P(X,Y,Z)/P(Z)
                p_xy_z = self.joint_probability(xi, yi, zi) / \
                         (self.marginal_counts[zi] / self.total_observations)
                
                # Cálculo de P(X|Z) y P(Y|Z) por separado
                p_x_z = self.conditional_probability(xi, z, zi)
                p_y_z = self.conditional_probability(yi, z, zi)
                
                # Producto de probabilidades P(X|Z)*P(Y|Z)
                p_product = p_x_z * p_y_z
                
                # Comparación con umbral de tolerancia
                if abs(p_xy_z - p_product) > threshold:
                    # Mensaje detallado cuando falla la independencia
                    print(f"Falla independencia para X={xi}, Y={yi}, Z={zi}:")
                    print(f"P(X,Y|Z)={p_xy_z:.4f} != P(X|Z)*P(Y|Z)={p_product:.4f}")
                    return False
                    
        # Si pasa todas las comparaciones, retorna True
        return True

    # Método para realizar prueba estadística chi-cuadrado
    def chi_squared_test(self, x: str, y: str, z: str, alpha: float = 0.05) -> bool:
        """
        Realiza test chi-cuadrado de independencia condicional X⊥Y|Z.
        
        Parámetros:
            x: Nombre de variable X (solo para referencia)
            y: Nombre de variable Y (solo para referencia)
            z: Nombre de variable Z (condicionante)
            alpha: Nivel de significancia (default 0.05)
            
        Retorna:
            bool: True si no se rechaza H0 (independencia), False si se rechaza
        """
        
        # Importación local de chi2_contingency para evitar dependencia innecesaria
        from scipy.stats import chi2_contingency
        
        # Obtención de valores únicos ordenados alfabéticamente
        x_vals = sorted(set(v[0] for v in self.joint_counts.keys()))
        y_vals = sorted(set(v[1] for v in self.joint_counts.keys()))
        z_vals = sorted(set(v[2] for v in self.joint_counts.keys()))
        
        # Iteración sobre cada valor posible de Z
        for zi in z_vals:
            # Construcción de tabla de contingencia para Z=zi
            contingency_table = []
            
            # Construcción de filas de la tabla
            for xi in x_vals:
                row = []
                # Construcción de columnas de la tabla
                for yi in y_vals:
                    # Agregar conteo observado para (X=xi,Y=yi,Z=zi)
                    row.append(self.joint_counts[(xi, yi, zi)])
                # Agregar fila completa a la tabla
                contingency_table.append(row)
            
            # Realización del test chi-cuadrado
            # chi2: valor del estadístico
            # p: p-valor
            # dof: grados de libertad
            # expected: valores esperados bajo H0
            chi2, p, dof, expected = chi2_contingency(contingency_table)
            
            # Comparación de p-valor con nivel de significancia
            if p < alpha:
                # Mensaje cuando se rechaza la independencia
                print(f"Se rechaza independencia para Z={zi}: p-value={p:.4f}")
                return False
                
        # Si pasa todas las pruebas, retorna True
        return True


# Bloque principal de ejecución del script
if __name__ == "__main__":
    # Mensaje inicial
    print("=== Verificación de Independencia Condicional ===\n")
    
    # Caso 1: Datos con independencia condicional
    print("1. Caso CON independencia condicional:")
    
    # Creación de instancia del verificador
    ci = ConditionalIndependence()
    
    # Dataset donde X e Y son independientes dado Z
    data_independent = [
        ('si', 'si', 'lluvia'), ('si', 'si', 'lluvia'), ('si', 'no', 'lluvia'),
        ('no', 'si', 'lluvia'), ('no', 'no', 'lluvia'), ('no', 'no', 'lluvia'),
        ('si', 'si', 'soleado'), ('si', 'no', 'soleado'), ('si', 'no', 'soleado'),
        ('no', 'si', 'soleado'), ('no', 'si', 'soleado'), ('no', 'no', 'soleado')
    ]
    
    # Registro de todas las observaciones del dataset
    for obs in data_independent:
        ci.add_observation(*obs)
    
    # Verificación por método de comparación de probabilidades
    print("\nVerificación por fórmula de probabilidad:")
    is_indep = ci.check_conditional_independence('X', 'Y', 'Z')
    print(f"¿X es independiente de Y dado Z? {is_indep}")
    
    # Verificación por método estadístico chi-cuadrado
    print("\nTest Chi-cuadrado:")
    chi_result = ci.chi_squared_test('X', 'Y', 'Z')
    print(f"¿No se rechaza independencia? {chi_result}")
    
    # Caso 2: Datos SIN independencia condicional
    print("\n2. Caso SIN independencia condicional:")
    
    # Creación de nueva instancia del verificador
    ci_dep = ConditionalIndependence()
    
    # Dataset donde X e Y NO son independientes dado Z
    data_dependent = [
        ('si', 'si', 'lluvia'), ('si', 'si', 'lluvia'), ('si', 'no', 'lluvia'),
        ('no', 'no', 'lluvia'), ('no', 'no', 'lluvia'), ('no', 'no', 'lluvia'),
        ('si', 'no', 'soleado'), ('si', 'no', 'soleado'), ('si', 'no', 'soleado'),
        ('no', 'si', 'soleado'), ('no', 'si', 'soleado'), ('no', 'no', 'soleado')
    ]
    
    # Registro de todas las observaciones del dataset
    for obs in data_dependent:
        ci_dep.add_observation(*obs)
    
    # Verificación por método de comparación de probabilidades
    print("\nVerificación por fórmula de probabilidad:")
    is_indep = ci_dep.check_conditional_independence('X', 'Y', 'Z')
    print(f"¿X es independiente de Y dado Z? {is_indep}")
    
    # Verificación por método estadístico chi-cuadrado
    print("\nTest Chi-cuadrado:")
    chi_result = ci_dep.chi_squared_test('X', 'Y', 'Z')
    print(f"¿No se rechaza independencia? {chi_result}")