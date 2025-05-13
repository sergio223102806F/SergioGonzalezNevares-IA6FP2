# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 14:39:04 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
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

from typing import List, Optional, Tuple                               # Importa tipos para anotaciones de tipo
import sys                                                                 # Importa el módulo sys para interactuar con el intérprete

class Backtracking:                                                        # Define una clase base llamada Backtracking
    """
    Clase base para algoritmos de backtracking.                          # Documentación de la clase Backtracking
    
    Atributos:                                                              # Documentación de los atributos
        soluciones (List): Lista de soluciones encontradas                 # Lista para almacenar las soluciones encontradas
        n_soluciones (int): Número de soluciones encontradas              # Contador del número de soluciones encontradas
    """
    def __init__(self):                                                     # Define el constructor de la clase
        self.soluciones = []                                                # Inicializa una lista vacía para las soluciones
        self.n_soluciones = 0                                               # Inicializa el contador de soluciones a cero
    
    def es_prometedora(self, solucion_parcial: List, paso: int) -> bool:     # Define un método abstracto para verificar si una solución parcial es prometedora
        """
        Verifica si una solución parcial es prometedora.                 # Documentación del método es_prometedora
        
        Args:                                                              # Documentación de los argumentos
            solucion_parcial: Solución en construcción                     # La solución que se está construyendo
            paso: Nivel actual de profundidad en el árbol de búsqueda      # El nivel actual en el árbol de búsqueda
            
        Returns:                                                          # Documentación del valor de retorno
            bool: True si la solución puede llevar a una solución válida   # True si la solución parcial puede llevar a una solución válida
        """
        raise NotImplementedError("Método abstracto")                      # Lanza una excepción si el método no se implementa en una subclase
    
    def es_completa(self, solucion_parcial: List, paso: int) -> bool:       # Define un método abstracto para verificar si una solución parcial es completa
        """
        Verifica si una solución parcial es completa.                   # Documentación del método es_completa
        
        Args:                                                              # Documentación de los argumentos
            solucion_parcial: Solución en construcción                     # La solución que se está construyendo
            paso: Nivel actual de profundidad en el árbol de búsqueda      # El nivel actual en el árbol de búsqueda
            
        Returns:                                                          # Documentación del valor de retorno
            bool: True si la solución es completa y válida               # True si la solución parcial es completa y válida
        """
        raise NotImplementedError("Método abstracto")                      # Lanza una excepción si el método no se implementa en una subclase
    
    def generar_candidatos(self, solucion_parcial: List, paso: int) -> List: # Define un método abstracto para generar candidatos
        """
        Genera los posibles candidatos para el siguiente paso.            # Documentación del método generar_candidatos
        
        Args:                                                              # Documentación de los argumentos
            solucion_parcial: Solución en construcción                     # La solución que se está construyendo
            paso: Nivel actual de profundidad en el árbol de búsqueda      # El nivel actual en el árbol de búsqueda
            
        Returns:                                                          # Documentación del valor de retorno
            List: Lista de candidatos para el siguiente paso              # Lista de posibles candidatos para el siguiente paso
        """
        raise NotImplementedError("Método abstracto")                      # Lanza una excepción si el método no se implementa en una subclase
    
    def backtrack(self, solucion_parcial: Optional[List] = None, paso: int = 0) -> None: # Define el método principal de backtracking recursivo
        """
        Algoritmo principal de backtracking recursivo.                   # Documentación del método backtrack
        
        Args:                                                              # Documentación de los argumentos
            solucion_parcial: Solución en construcción (None al inicio)    # La solución que se está construyendo (inicialmente None)
            paso: Nivel actual de profundidad en el árbol de búsqueda      # El nivel actual en el árbol de búsqueda (inicialmente 0)
        """
        if solucion_parcial is None:                                     # Si la solución parcial es None (inicio)
            solucion_parcial = []                                         # Inicializa una lista vacía para la solución parcial
        
        # Verificar si la solución parcial es completa                   # Comentario indicando la verificación de si la solución es completa
        if self.es_completa(solucion_parcial, paso):                      # Si la solución parcial es completa
            self.soluciones.append(solucion_parcial.copy())              # Agrega una copia de la solución parcial a la lista de soluciones
            self.n_soluciones += 1                                        # Incrementa el contador de soluciones
            return                                                         # Regresa de la llamada recursiva
        
        # Verificar si la solución parcial es prometedora                # Comentario indicando la verificación de si la solución es prometedora
        if not self.es_prometedora(solucion_parcial, paso):               # Si la solución parcial no es prometedora
            return                                                         # Regresa de la llamada recursiva (poda)
        
        # Generar y probar todos los candidatos válidos                 # Comentario indicando la generación y prueba de candidatos
        for candidato in self.generar_candidatos(solucion_parcial, paso): # Itera sobre los candidatos generados
            solucion_parcial.append(candidato)                            # Agrega el candidato a la solución parcial
            self.backtrack(solucion_parcial, paso + 1)                   # Llama recursivamente a backtrack con la solución parcial actualizada y el siguiente paso
            solucion_parcial.pop()                                        # Retrocede (elimina el último candidato para probar otras opciones)
    
    def resolver(self) -> None:                                           # Define el método para iniciar el proceso de resolución
        """Inicia el proceso de backtracking."""                           # Documentación del método resolver
        self.soluciones = []                                                # Reinicializa la lista de soluciones
        self.n_soluciones = 0                                               # Reinicializa el contador de soluciones
        self.backtrack()                                                   # Llama al método principal de backtracking

class NReinas(Backtracking):                                             # Define una clase NReinas que hereda de Backtracking
    """
    Implementación del problema de las N-Reinas usando backtracking.    # Documentación de la clase NReinas
    
    Atributos:                                                              # Documentación de los atributos
        n (int): Tamaño del tablero y número de reinas                  # El tamaño del tablero y el número de reinas
    """
    def __init__(self, n: int = 8):                                       # Define el constructor de la clase NReinas
        super().__init__()                                                 # Llama al constructor de la clase padre
        self.n = n                                                          # Inicializa el tamaño del tablero
    
    def es_prometedora(self, solucion_parcial: List[int], paso: int) -> bool: # Define el método para verificar si una colocación parcial de reinas es válida
        """
        Verifica si una colocación parcial de reinas es válida.          # Documentación del método es_prometedora para NReinas
        
        Args:                                                              # Documentación de los argumentos
            solucion_parcial: Lista de columnas donde se han colocado reinas # Lista de las columnas donde se han colocado las reinas hasta el momento
            paso: Fila actual que se está considerando                  # La fila actual en la que se intenta colocar una reina
            
        Returns:                                                          # Documentación del valor de retorno
            bool: True si ninguna reina se ataca mutuamente               # True si la colocación parcial de reinas es válida (ninguna se ataca)
        """
        # Verificar todas las reinas colocadas hasta ahora                # Comentario indicando la verificación de las reinas anteriores
        for i in range(paso):                                             # Itera sobre las reinas ya colocadas
            # Misma columna o misma diagonal                               # Comentario indicando la verificación de la misma columna o diagonal
            if (solucion_parcial[i] == solucion_parcial[paso] or          # Si la reina actual está en la misma columna que una reina anterior
                abs(solucion_parcial[i] - solucion_parcial[paso]) == paso - i): # O si la reina actual está en la misma diagonal que una reina anterior
                return False                                               # La colocación no es prometedora
        return True                                                        # La colocación es prometedora
    
    def es_completa(self, solucion_parcial: List[int], paso: int) -> bool:   # Define el método para verificar si se han colocado todas las reinas válidamente
        """
        Verifica si se han colocado todas las reinas válidamente.        # Documentación del método es_completa para NReinas
        
        Args:                                                              # Documentación de los argumentos
            solucion_parcial: Lista de columnas donde se han colocado reinas # Lista de las columnas donde se han colocado las reinas
            paso: Fila actual que se está considerando                  # La fila actual (que sería igual a n si todas las reinas están colocadas)
            
        Returns:                                                          # Documentación del valor de retorno
            bool: True si se colocaron todas las reinas sin conflictos    # True si se han colocado n reinas sin conflictos
        """
        return paso == self.n                                             # La solución es completa si se han colocado n reinas
    
    def generar_candidatos(self, solucion_parcial: List[int], paso: int) -> List[int]: # Define el método para generar las columnas posibles para la siguiente reina
        """
        Genera todas las columnas posibles para la siguiente reina.       # Documentación del método generar_candidatos para NReinas
        
        Args:                                                              # Documentación de los argumentos
            solucion_parcial: Lista de columnas donde se han colocado reinas # Lista de las columnas donde se han colocado las reinas
            paso: Fila actual que se está considerando                  # La fila actual en la que se intenta colocar una reina
            
        Returns:                                                          # Documentación del valor de retorno
            List[int]: Lista de columnas posibles (0 a n-1)              # Lista de todas las columnas posibles para la siguiente reina
        """
        return list(range(self.n))                                         # Los candidatos son todas las columnas del tablero (0 a n-1)
    
    def imprimir_tablero(self, solucion: List[int]) -> None:                # Define el método para imprimir el tablero con las reinas
        """
        Imprime un tablero con las reinas colocadas.                      # Documentación del método imprimir_tablero
        
        Args:                                                              # Documentación de los argumentos
            solucion: Lista de columnas donde se colocaron las reinas      # Lista de las columnas donde se han colocado las reinas
        """
        for fila in range(self.n):                                         # Itera sobre cada fila del tablero
            linea = ""                                                     # Inicializa una cadena vacía para la fila
            for col in range(self.n):                                      # Itera sobre cada columna del tablero
                if solucion[fila] == col:                                 # Si hay una reina en esta celda
                    linea += "Q "                                         # Agrega "Q " a la línea
                else:                                                      # Si no hay reina
                    linea += ". "                                         # Agrega ". " a la línea
            print(linea)                                                   # Imprime la línea de la fila
        print()                                                            # Imprime una línea en blanco después del tablero
    
    def resolver(self, imprimir_todas: bool = False, limite_soluciones: Optional[int] = None) -> None: # Define el método para resolver el problema de las N-Reinas con opciones de visualización
        """
        Resuelve el problema de las N-Reinas con opciones de visualización. # Documentación del método resolver para NReinas
        
        Args:                                                              # Documentación de los argumentos
            imprimir_todas: Si True, imprime todas las soluciones         # Booleano para indicar si se deben imprimir todas las soluciones encontradas
            limite_soluciones: Límite máximo de soluciones a encontrar    # Número máximo de soluciones a encontrar (None para encontrar todas)
        """
        self.soluciones = []                                                # Reinicializa la lista de soluciones
        self.n_soluciones = 0                                               # Reinicializa el contador de soluciones
        self.backtrack()                                                   # Llama al método principal de backtracking
        
        print(f"\nTotal de soluciones encontradas para {self.n}-Reinas: {self.n_soluciones}") # Imprime el número total de soluciones encontradas
        
        if imprimir_todas and self.soluciones:                             # Si se solicita imprimir todas las soluciones y hay soluciones
            print("\nTodas las soluciones:")                               # Imprime un encabezado para todas las soluciones
            for i, sol in enumerate(self.soluciones, 1):                   # Itera sobre cada solución encontrada con su índice
                print(f"\nSolución {i}:")                                 # Imprime el número de la solución
                self.imprimir_tablero(sol)                                 # Imprime el tablero para la solución actual
                
                if limite_soluciones and i >= limite_soluciones:           # Si hay un límite de soluciones y se ha alcanzado
                    print(f"Mostrando {limite_soluciones} de {self.n_soluciones} soluciones...") # Imprime un mensaje indicando el límite alcanzado
                    break                                                  # Sale del bucle
        elif self.soluciones:                                              # Si hay soluciones pero no se solicitó imprimir todas
            print("\nPrimera solución encontrada:")                        # Imprime un encabezado para la primera solución
            self.imprimir_tablero(self.soluciones[0])                      # Imprime el tablero de la primera solución encontrada

def ejecutar_n_reinas(n: int = 8, imprimir_todas: bool = False, limite_soluciones: Optional[int] = None) -> None: # Define una función para ejecutar el problema de las N-Reinas
    """
    Función para ejecutar el problema de las N-Reinas con diferentes parámetros. # Documentación de la función ejecutar_n_reinas
    
    Args:                                                              # Documentación de los argumentos
        n: Tamaño del tablero y número de reinas                        # El tamaño del tablero (y el número de reinas)
        imprimir_todas: Si True, imprime todas las soluciones           # Booleano para indicar si se deben imprimir todas las soluciones
        limite_soluciones: Límite máximo de soluciones a imprimir      # Número máximo de soluciones a imprimir (None para todas)
    """
    print(f"\nResolviendo el problema de las {n}-Reinas:")            # Imprime un mensaje indicando el problema que se está resolviendo
    problema = NReinas(n)                                               # Crea una instancia de la clase NReinas
    problema.resolver(imprimir_todas, limite_soluciones)                 # Llama al método resolver del objeto NReinas

if __name__ == "__main__":                                               # Bloque de código que se ejecuta cuando el script se llama directamente
    # Ejemplo de uso con diferentes configuraciones                     # Comentario indicando ejemplos de uso
    ejecutar_n_reinas(4, True)                                          # Resuelve el problema de las 4-Reinas e imprime todas las soluciones
    ejecutar_n_reinas(8)                                             # Resuelve el problema de las 8-Reinas e imprime la primera solución
    ejecutar_n_reinas(6, True, 3)                                       # Resuelve el problema de las 6-Reinas e imprime hasta 3 soluciones
    
    # Opcional: permitir al usuario especificar N                        # Comentario indicando la opción de especificar N por argumento de línea de comandos
    if len(sys.argv) > 1:                                               # Si se proporciona un argumento de línea de comandos
        try:                                                           # Intenta convertir el argumento a un entero
            n = int(sys.argv[1])                                       # Convierte el primer argumento a un entero
            if n < 1:                                                   # Si el número es menor que 1
                raise ValueError                                       # Lanza un error de valor
            ejecutar_n_reinas(n, True, 5)                                # Resuelve el problema de las N-Reinas con el valor proporcionado, imprimiendo hasta 5 soluciones
        except ValueError:                                               # Captura la excepción si la conversión a entero falla o el valor es inválido
            print("Por favor ingrese un número entero positivo para N.") # Imprime un mensaje de error