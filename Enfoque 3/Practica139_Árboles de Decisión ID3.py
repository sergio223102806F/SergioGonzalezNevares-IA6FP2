# -*- coding: utf-8 -*-
"""
Implementación del algoritmo ID3 para árboles de decisión
Created on [Fecha]
@author: [Tu nombre]
"""

import math                          # Para funciones matemáticas (log2)
from collections import Counter      # Para contar frecuencias de clases

class NodoDecision:                  # Clase que representa un nodo del árbol
    """Nodo de un árbol de decisión, puede ser nodo interno u hoja"""
    def __init__(self, atributo=None, valor=None, ramas=None, resultado=None):
        self.atributo = atributo     # Atributo que se evalúa (None en hojas)
        self.valor = valor           # Valor del atributo que lleva a este nodo
        self.ramas = ramas or {}     # Subárboles: {valor_atributo: nodo_hijo}
        self.resultado = resultado   # Clase predicha (solo en nodos hoja)

    def __str__(self, nivel=0):      # Representación visual del árbol
        """Genera una representación textual del árbol con indentación"""
        prefijo = "  " * nivel       # Indentación según nivel de profundidad
        if self.resultado is not None:  # Si es nodo hoja
            return f"{prefijo}Clase: {self.resultado}"
        else:                        # Si es nodo interno
            s = f"{prefijo}[{self.atributo}?]\n"  # Muestra atributo a evaluar
            for valor, subarbol in self.ramas.items():  # Para cada rama
                s += f"{prefijo}--> {valor}:\n{subarbol.__str__(nivel+1)}\n"
            return s

def entropia(etiquetas):             # Función para calcular entropía
    """Calcula la entropía de un conjunto de etiquetas de clase"""
    conteos = Counter(etiquetas)     # Cuenta frecuencia de cada clase
    total = len(etiquetas)           # Total de ejemplos
    return -sum((count/total) * math.log2(count/total)  # Fórmula de entropía
               for count in conteos.values())           # para cada clase

def ganancia_informacion(datos, atributo, etiqueta_nombre="clase"):
    """Calcula la ganancia de información de dividir por un atributo"""
    # 1. Calcular entropía del conjunto completo
    etiquetas = [d[etiqueta_nombre] for d in datos]  # Extrae todas las clases
    entropia_total = entropia(etiquetas)             # Calcula entropía
    
    # 2. Calcular entropía después de dividir por el atributo
    valores = {d[atributo] for d in datos}           # Valores únicos del atributo
    entropia_atributo = 0.0
    total_muestras = len(datos)
    
    for valor in valores:                            # Para cada valor posible
        subconjunto = [d for d in datos if d[atributo] == valor]  # Filtra datos
        peso = len(subconjunto) / total_muestras     # Peso del subconjunto
        etiquetas_sub = [d[etiqueta_nombre] for d in subconjunto]  # Clases del subconjunto
        entropia_atributo += peso * entropia(etiquetas_sub)  # Entropía ponderada
    
    # 3. Ganancia = entropía_total - entropía_atributo
    return entropia_total - entropia_atributo

def id3(datos, atributos, etiqueta_nombre="clase", default=None):
    """Algoritmo ID3 para construir árboles de decisión de forma recursiva"""
    # Caso base 1: Todos los ejemplos son de la misma clase
    etiquetas = [d[etiqueta_nombre] for d in datos]
    if len(set(etiquetas)) == 1:     # Si solo hay una clase única
        return NodoDecision(resultado=etiquetas[0])  # Crea nodo hoja
    
    # Caso base 2: No quedan atributos para dividir
    if not atributos:                # Si no hay más atributos
        conteo = Counter(etiquetas)   # Usa la clase más frecuente
        return NodoDecision(resultado=conteo.most_common(1)[0][0])
    
    # 1. Seleccionar el mejor atributo (mayor ganancia de información)
    mejor_atributo = max(
        atributos, 
        key=lambda a: ganancia_informacion(datos, a, etiqueta_nombre)
    )
    
    # 2. Crear nodo con el mejor atributo
    nodo = NodoDecision(atributo=mejor_atributo)
    
    # 3. Dividir por cada valor del atributo
    valores = {d[mejor_atributo] for d in datos}  # Valores únicos del atributo
    nuevos_atributos = [a for a in atributos if a != mejor_atributo]  # Atributos restantes
    
    for valor in valores:             # Para cada valor posible del atributo
        subdatos = [d for d in datos if d[mejor_atributo] == valor]  # Filtra datos
        
        # Caso base 3: Subconjunto vacío (usar clase mayoritaria)
        if not subdatos:
            conteo = Counter(etiquetas)
            nodo.ramas[valor] = NodoDecision(resultado=conteo.most_common(1)[0][0])
        else:
            # Llamada recursiva para construir subárbol
            nodo.ramas[valor] = id3(subdatos, nuevos_atributos, etiqueta_nombre, default)
    
    return nodo                       # Devuelve el nodo construido

def clasificar(ejemplo, arbol):       # Función para clasificar nuevos ejemplos
    """Clasifica un ejemplo usando el árbol de decisión"""
    if arbol.resultado is not None:   # Si es nodo hoja
        return arbol.resultado        # Devuelve la clase predicha
    
    valor = ejemplo[arbol.atributo]   # Obtiene valor del atributo del nodo
    if valor not in arbol.ramas:      # Si el valor no se vio en entrenamiento
        return None                   # No se puede clasificar
    
    return clasificar(ejemplo, arbol.ramas[valor])  # Llama recursivamente

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":            # Punto de entrada principal
    # Datos de entrenamiento (clásico ejemplo "jugar golf")
    datos_entrenamiento = [
        {"outlook": "sunny", "temp": "hot", "humidity": "high", "wind": "weak", "clase": "no"},
        {"outlook": "sunny", "temp": "hot", "humidity": "high", "wind": "strong", "clase": "no"},
        {"outlook": "overcast", "temp": "hot", "humidity": "high", "wind": "weak", "clase": "yes"},
        # ... (resto de los datos del ejemplo)
    ]

    # Lista de atributos (excluyendo la clase)
    atributos = ["outlook", "temp", "humidity", "wind"]

    # Construir árbol de decisión
    arbol = id3(datos_entrenamiento, atributos)
    print("Árbol de decisión construido:\n")
    print(arbol)                      # Muestra el árbol generado

    # Clasificar un nuevo ejemplo
    nuevo_ejemplo = {"outlook": "sunny", "temp": "cool", 
                    "humidity": "high", "wind": "strong"}
    prediccion = clasificar(nuevo_ejemplo, arbol)
    print(f"\nPredicción para {nuevo_ejemplo}: {prediccion}")