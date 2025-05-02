# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:39:04 2025

@author: elvin
"""

"""
Implementación del Algoritmo de Backtracking con Ejemplo de las N-Reinas

Este código incluye:
1. Estructura general de backtracking
2. Implementación del problema de las N-Reinas
3. Visualización de soluciones
4. Poda de ramas no prometedoras
5. Contaje de soluciones
"""

from typing import List, Optional, Tuple
import sys

class Backtracking:
    """
    Clase base para algoritmos de backtracking.
    
    Atributos:
        soluciones (List): Lista de soluciones encontradas
        n_soluciones (int): Número de soluciones encontradas
    """
    def __init__(self):
        self.soluciones = []
        self.n_soluciones = 0
    
    def es_prometedora(self, solucion_parcial: List, paso: int) -> bool:
        """
        Verifica si una solución parcial es prometedora.
        
        Args:
            solucion_parcial: Solución en construcción
            paso: Nivel actual de profundidad en el árbol de búsqueda
            
        Returns:
            bool: True si la solución puede llevar a una solución válida
        """
        raise NotImplementedError("Método abstracto")
    
    def es_completa(self, solucion_parcial: List, paso: int) -> bool:
        """
        Verifica si una solución parcial es completa.
        
        Args:
            solucion_parcial: Solución en construcción
            paso: Nivel actual de profundidad en el árbol de búsqueda
            
        Returns:
            bool: True si la solución es completa y válida
        """
        raise NotImplementedError("Método abstracto")
    
    def generar_candidatos(self, solucion_parcial: List, paso: int) -> List:
        """
        Genera los posibles candidatos para el siguiente paso.
        
        Args:
            solucion_parcial: Solución en construcción
            paso: Nivel actual de profundidad en el árbol de búsqueda
            
        Returns:
            List: Lista de candidatos para el siguiente paso
        """
        raise NotImplementedError("Método abstracto")
    
    def backtrack(self, solucion_parcial: Optional[List] = None, paso: int = 0) -> None:
        """
        Algoritmo principal de backtracking recursivo.
        
        Args:
            solucion_parcial: Solución en construcción (None al inicio)
            paso: Nivel actual de profundidad en el árbol de búsqueda
        """
        if solucion_parcial is None:
            solucion_parcial = []
        
        # Verificar si la solución parcial es completa
        if self.es_completa(solucion_parcial, paso):
            self.soluciones.append(solucion_parcial.copy())
            self.n_soluciones += 1
            return
        
        # Verificar si la solución parcial es prometedora
        if not self.es_prometedora(solucion_parcial, paso):
            return
        
        # Generar y probar todos los candidatos válidos
        for candidato in self.generar_candidatos(solucion_parcial, paso):
            solucion_parcial.append(candidato)
            self.backtrack(solucion_parcial, paso + 1)
            solucion_parcial.pop()  # Retroceder (backtrack)
    
    def resolver(self) -> None:
        """Inicia el proceso de backtracking."""
        self.soluciones = []
        self.n_soluciones = 0
        self.backtrack()

class NReinas(Backtracking):
    """
    Implementación del problema de las N-Reinas usando backtracking.
    
    Atributos:
        n (int): Tamaño del tablero y número de reinas
    """
    def __init__(self, n: int = 8):
        super().__init__()
        self.n = n
    
    def es_prometedora(self, solucion_parcial: List[int], paso: int) -> bool:
        """
        Verifica si una colocación parcial de reinas es válida.
        
        Args:
            solucion_parcial: Lista de columnas donde se han colocado reinas
            paso: Fila actual que se está considerando
            
        Returns:
            bool: True si ninguna reina se ataca mutuamente
        """
        # Verificar todas las reinas colocadas hasta ahora
        for i in range(paso):
            # Misma columna o misma diagonal
            if (solucion_parcial[i] == solucion_parcial[paso] or 
                abs(solucion_parcial[i] - solucion_parcial[paso]) == paso - i):
                return False
        return True
    
    def es_completa(self, solucion_parcial: List[int], paso: int) -> bool:
        """
        Verifica si se han colocado todas las reinas válidamente.
        
        Args:
            solucion_parcial: Lista de columnas donde se han colocado reinas
            paso: Fila actual que se está considerando
            
        Returns:
            bool: True si se colocaron todas las reinas sin conflictos
        """
        return paso == self.n
    
    def generar_candidatos(self, solucion_parcial: List[int], paso: int) -> List[int]:
        """
        Genera todas las columnas posibles para la siguiente reina.
        
        Args:
            solucion_parcial: Lista de columnas donde se han colocado reinas
            paso: Fila actual que se está considerando
            
        Returns:
            List[int]: Lista de columnas posibles (0 a n-1)
        """
        return list(range(self.n))
    
    def imprimir_tablero(self, solucion: List[int]) -> None:
        """
        Imprime un tablero con las reinas colocadas.
        
        Args:
            solucion: Lista de columnas donde se colocaron las reinas
        """
        for fila in range(self.n):
            linea = ""
            for col in range(self.n):
                if solucion[fila] == col:
                    linea += "Q "
                else:
                    linea += ". "
            print(linea)
        print()
    
    def resolver(self, imprimir_todas: bool = False, limite_soluciones: Optional[int] = None) -> None:
        """
        Resuelve el problema de las N-Reinas con opciones de visualización.
        
        Args:
            imprimir_todas: Si True, imprime todas las soluciones
            limite_soluciones: Límite máximo de soluciones a encontrar
        """
        self.soluciones = []
        self.n_soluciones = 0
        self.backtrack()
        
        print(f"\nTotal de soluciones encontradas para {self.n}-Reinas: {self.n_soluciones}")
        
        if imprimir_todas and self.soluciones:
            print("\nTodas las soluciones:")
            for i, sol in enumerate(self.soluciones, 1):
                print(f"\nSolución {i}:")
                self.imprimir_tablero(sol)
                
                if limite_soluciones and i >= limite_soluciones:
                    print(f"Mostrando {limite_soluciones} de {self.n_soluciones} soluciones...")
                    break
        elif self.soluciones:
            print("\nPrimera solución encontrada:")
            self.imprimir_tablero(self.soluciones[0])

def ejecutar_n_reinas(n: int = 8, imprimir_todas: bool = False, limite_soluciones: Optional[int] = None) -> None:
    """
    Función para ejecutar el problema de las N-Reinas con diferentes parámetros.
    
    Args:
        n: Tamaño del tablero y número de reinas
        imprimir_todas: Si True, imprime todas las soluciones
        limite_soluciones: Límite máximo de soluciones a imprimir
    """
    print(f"\nResolviendo el problema de las {n}-Reinas:")
    problema = NReinas(n)
    problema.resolver(imprimir_todas, limite_soluciones)

if __name__ == "__main__":
    # Ejemplo de uso con diferentes configuraciones
    ejecutar_n_reinas(4, True)  # Problema de las 4-Reinas, mostrar todas las soluciones
    ejecutar_n_reinas(8)        # Problema clásico de las 8-Reinas, mostrar solo la primera solución
    ejecutar_n_reinas(6, True, 3)  # 6-Reinas, mostrar solo 3 soluciones de las encontradas
    
    # Opcional: permitir al usuario especificar N
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            if n < 1:
                raise ValueError
            ejecutar_n_reinas(n, True, 5)
        except ValueError:
            print("Por favor ingrese un número entero positivo para N.")