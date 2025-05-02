# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:36:37 2025

@author: elvin
"""

"""
Implementación de Tablas de Verdad para Lógica Proposicional

Este código permite:
1. Generar tablas de verdad para expresiones lógicas
2. Evaluar proposiciones con múltiples variables
3. Analizar sintaxis y semántica de expresiones booleanas
4. Visualizar resultados de manera clara
"""

# Importar itertools para generar combinaciones de valores de verdad
import itertools

def generar_tabla_verdad(variables, expresion):
    """
    Genera una tabla de verdad para una expresión lógica dada.
    
    Args:
        variables (list): Lista de nombres de variables (ej. ['p', 'q'])
        expresion (str): Expresión lógica a evaluar (ej. 'p and q')
        
    Returns:
        list: Lista de diccionarios con cada combinación y resultado
    """
    
    # Determinar el número de variables
    num_vars = len(variables)
    
    # Generar todas las combinaciones posibles de valores de verdad
    # itertools.product genera el producto cartesiano para True/False
    combinaciones = list(itertools.product([False, True], repeat=num_vars))
    
    tabla = []
    
    # Evaluar cada combinación de valores
    for combinacion in combinaciones:
        # Crear contexto con los valores actuales de las variables
        contexto = dict(zip(variables, combinacion))
        
        try:
            # Evaluar la expresión en el contexto actual
            # NOTA: Usar eval puede ser peligroso con input no confiable
            resultado = eval(expresion, {}, contexto)
        except:
            # Manejar errores de sintaxis en la expresión
            print(f"Error al evaluar la expresión: {expresion}")
            return None
        
        # Crear entrada para la tabla de verdad
        entrada = contexto.copy()
        entrada['resultado'] = resultado
        tabla.append(entrada)
    
    return tabla

def imprimir_tabla_verdad(tabla, variables):
    """
    Imprime la tabla de verdad en formato legible.
    
    Args:
        tabla (list): Tabla generada por generar_tabla_verdad
        variables (list): Lista de nombres de variables
    """
    
    if not tabla:
        print("No hay datos para mostrar")
        return
    
    # Encabezado de la tabla
    encabezado = variables + ['Resultado']
    print(" | ".join(encabezado))
    print("-" * (len(" | ".join(encabezado))))
    
    # Imprimir cada fila de la tabla
    for fila in tabla:
        valores = []
        for var in variables:
            # Convertir booleanos a 'V' (True) y 'F' (False)
            valores.append('V' if fila[var] else 'F')
        # Añadir resultado
        valores.append('V' if fila['resultado'] else 'F')
        print(" | ".join(valores))

def analizar_expresion(expresion):
    """
    Realiza análisis básico de sintaxis y semántica de una expresión lógica.
    
    Args:
        expresion (str): Expresión lógica a analizar
        
    Returns:
        dict: Diccionario con información del análisis
    """
    
    analisis = {
        'variables': set(),
        'operadores': set(),
        'valida': True,
        'errores': []
    }
    
    # Palabras reservadas y operadores permitidos
    operadores_permitidos = {'and', 'or', 'not', '(', ')'}
    palabras_reservadas = {'True', 'False'} | operadores_permitidos
    
    # Tokenización básica (esto es una simplificación)
    tokens = expresion.split()
    
    for token in tokens:
        # Verificar si es un operador
        if token in operadores_permitidos:
            analisis['operadores'].add(token)
        # Verificar si es un valor booleano
        elif token in {'True', 'False'}:
            continue
        # Verificar si es una variable (debe comenzar con letra)
        elif token.isidentifier():
            analisis['variables'].add(token)
        else:
            analisis['valida'] = False
            analisis['errores'].append(f"Token inválido: '{token}'")
    
    # Verificación adicional de paréntesis balanceados
    balance = 0
    for char in expresion:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
            if balance < 0:
                analisis['valida'] = False
                analisis['errores'].append("Paréntesis no balanceados")
                break
    
    if balance != 0:
        analisis['valida'] = False
        analisis['errores'].append("Paréntesis no balanceados")
    
    return analisis

def demostrar_equivalencia(expresion1, expresion2):
    """
    Demuestra si dos expresiones lógicas son equivalentes mediante tabla de verdad.
    
    Args:
        expresion1 (str): Primera expresión lógica
        expresion2 (str): Segunda expresión lógica
        
    Returns:
        bool: True si son equivalentes, False si no
    """
    
    # Analizar ambas expresiones
    analisis1 = analizar_expresion(expresion1)
    analisis2 = analizar_expresion(expresion2)
    
    # Verificar que ambas expresiones sean válidas
    if not analisis1['valida'] or not analisis2['valida']:
        print("Una o ambas expresiones no son válidas")
        return False
    
    # Obtener todas las variables involucradas
    variables = list(analisis1['variables'].union(analisis2['variables']))
    
    # Generar tablas de verdad
    tabla1 = generar_tabla_verdad(variables, expresion1)
    tabla2 = generar_tabla_verdad(variables, expresion2)
    
    # Comparar resultados
    for fila1, fila2 in zip(tabla1, tabla2):
        if fila1['resultado'] != fila2['resultado']:
            return False
    
    return True

# Ejemplo de uso
if __name__ == "__main__":
    print("DEMOSTRADOR DE TABLAS DE VERDAD")
    print("=" * 40)
    
    # Ejemplo 1: Expresión simple
    variables = ['p', 'q']
    expresion = "p and q"
    
    print(f"\nAnalizando expresión: {expresion}")
    analisis = analizar_expresion(expresion)
    print(f"Variables encontradas: {analisis['variables']}")
    print(f"Operadores encontrados: {analisis['operadores']}")
    print(f"Expresión válida: {analisis['valida']}")
    
    if analisis['valida']:
        tabla = generar_tabla_verdad(variables, expresion)
        print("\nTabla de Verdad:")
        imprimir_tabla_verdad(tabla, variables)
    
    # Ejemplo 2: Comparación de equivalencias
    exp1 = "not (p and q)"
    exp2 = "(not p) or (not q)"
    
    print(f"\nComparando expresiones:")
    print(f"1: {exp1}")
    print(f"2: {exp2}")
    
    if demostrar_equivalencia(exp1, exp2):
        print("\nLas expresiones SON equivalentes (Leyes de De Morgan)")
    else:
        print("\nLas expresiones NO SON equivalentes")
    
    # Generar tabla para la primera expresión de comparación
    print("\nTabla de verdad para la primera expresión:")
    tabla_exp1 = generar_tabla_verdad(variables, exp1)
    imprimir_tabla_verdad(tabla_exp1, variables)
    
    # Generar tabla para la segunda expresión de comparación
    print("\nTabla de verdad para la segunda expresión:")
    tabla_exp2 = generar_tabla_verdad(variables, exp2)
    imprimir_tabla_verdad(tabla_exp2, variables)