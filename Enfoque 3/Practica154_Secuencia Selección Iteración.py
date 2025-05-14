# =============================================
# ESTRUCTURAS DE CONTROL FUNDAMENTALES -
# -------------------------------------------------------------
# Este código demuestra las tres estructuras básicas de programación estructurada:
# 1. Secuencia - Ejecución lineal de instrucciones
# 2. Selección - Toma de decisiones (if/else)
# 3. Iteración - Bucles (while, for)
# """

# ============ IMPORTACIONES ============
from typing import List, Dict, Optional # Importa tipos para anotaciones de tipo
import random # Importa el módulo random para generar números aleatorios

# ============ SECUENCIA ============
def demostrar_secuencia() -> None:
    """
    DEMOSTRACIÓN DE SECUENCIA
    -------------------------
    Ejecución lineal de instrucciones, una después de otra.
    """
    print("\n=== SECUENCIA ===")
    
    # Instrucción 1
    resultado_suma = 5 + 3 # Realiza una suma
    print(f"1. Suma: 5 + 3 = {resultado_suma}") # Imprime el resultado de la suma
    
    # Instrucción 2
    resultado_resta = 10 - 2 # Realiza una resta
    print(f"2. Resta: 10 - 2 = {resultado_resta}") # Imprime el resultado de la resta
    
    # Instrucción 3
    resultado_final = resultado_suma * resultado_resta # Realiza una multiplicación
    print(f"3. Multiplicación: {resultado_suma} * {resultado_resta} = {resultado_final}") # Imprime el resultado de la multiplicación
    
    # Todas se ejecutan en orden, una tras otra

# ============ SELECCIÓN ============
def demostrar_seleccion(edad: int) -> None:
    """
    DEMOSTRACIÓN DE SELECCIÓN
    -------------------------
    Toma de decisiones basadas en condiciones.
    
    Args:
        edad: Edad para evaluar diferentes casos
    """
    print("\n=== SELECCIÓN (if/elif/else) ===")
    print(f"Edad evaluada: {edad} años")
    
    # Estructura if simple
    if edad >= 18: # Si la edad es mayor o igual a 18
        print(" - Eres mayor de edad") # Imprime que es mayor de edad
    
    # If-else
    if edad < 12: # Si la edad es menor a 12
        print(" - Eres un niño") # Imprime que es un niño
    else: # En caso contrario
        print(" - Ya no eres un niño") # Imprime que ya no es un niño
    
    # If-elif-else múltiple
    if edad < 0: # Si la edad es menor a 0
        print(" - Edad no válida (negativa)") # Imprime que la edad no es válida
    elif 0 <= edad < 3: # Si la edad está entre 0 y 3
        print(" - Bebé") # Imprime que es un bebé
    elif 3 <= edad < 12: # Si la edad está entre 3 y 12
        print(" - Niño") # Imprime que es un niño
    elif 12 <= edad < 18: # Si la edad está entre 12 y 18
        print(" - Adolescente") # Imprime que es un adolescente
    elif 18 <= edad < 65: # Si la edad está entre 18 y 65
        print(" - Adulto") # Imprime que es un adulto
    else: # En caso contrario
        print(" - Adulto mayor") # Imprime que es un adulto mayor

# ============ ITERACIÓN ============
def demostrar_iteracion() -> None:
    """
    DEMOSTRACIÓN DE ITERACIÓN
    ------------------------
    Ejecución repetida de código mientras se cumpla una condición.
    """
    print("\n=== ITERACIÓN ===")
    
    # Bucle while - Ejecución condicional
    print("\n1. Bucle WHILE (condicional):")
    contador = 3 # Inicializa un contador en 3
    while contador > 0: # Mientras el contador sea mayor que 0
        print(f"  Contador: {contador}") # Imprime el valor del contador
        contador -= 1  # Decrementa el contador en 1
    
    # Bucle for - Iteración sobre secuencia
    print("\n2. Bucle FOR (sobre secuencia):")
    frutas = ["manzana", "banana", "cereza"] # Define una lista de frutas
    for i, fruta in enumerate(frutas, 1): # Itera sobre la lista de frutas, obteniendo el índice y el valor
        print(f"  Fruta {i}: {fruta}") # Imprime el índice y la fruta
    
    # Bucle con break/continue
    print("\n3. Bucle con CONTROL (break/continue):")
    for num in range(1, 6): # Itera sobre el rango de 1 a 5
        if num == 3: # Si el número es 3
            print("  Saltando el 3 con continue") # Imprime que se salta el 3
            continue # Salta a la siguiente iteración
        if num == 5: # Si el número es 5
            print("  Rompiendo en 5 con break") # Imprime que se rompe el bucle en 5
            break # Sale del bucle
        print(f"  Número actual: {num}") # Imprime el número actual

# ============ EJEMPLO INTEGRADO ============
def juego_adivinanza() -> None:
    """
    JUEGO DE ADIVINANZAS - COMBINANDO LAS 3 ESTRUCTURAS
    --------------------------------------------------
    Demuestra cómo interactúan secuencia, selección e iteración
    en un programa completo.
    """
    print("\n=== JUEGO: ADIVINA EL NÚMERO ===")
    
    # SECUENCIA: Configuración inicial
    numero_secreto = random.randint(1, 10) # Genera un número aleatorio entre 1 y 10
    intentos = 3 # Establece el número de intentos
    adivinado = False # Inicializa la variable para indicar si se ha adivinado
    
    print("Adivina un número entre 1 y 10. Tienes 3 intentos.")
    
    # ITERACIÓN: Bucle principal del juego
    while intentos > 0 and not adivinado: # Mientras queden intentos y no se haya adivinado
        # SECUENCIA: Dentro de cada iteración
        try:
            intento = int(input("\nTu suposición: ")) # Pide al usuario que ingrese un número
        except ValueError: # Si el usuario no ingresa un número válido
            print("¡Debes ingresar un número!") # Imprime un mensaje de error
            continue # Salta a la siguiente iteración del bucle
        
        # SELECCIÓN: Evaluar el intento
        if intento == numero_secreto: # Si el intento es igual al número secreto
            print("¡Correcto! ¡Has adivinado!") # Imprime que ha adivinado correctamente
            adivinado = True # Establece la variable adivinado en True
        else: # En caso contrario
            intentos -= 1 # Decrementa los intentos
            if intento < numero_secreto: # Si el intento es menor que el número secreto
                print(f"El número es mayor. Intentos restantes: {intentos}") # Imprime que el número es mayor
            else: # En caso contrario
                print(f"El número es menor. Intentos restantes: {intentos}") # Imprime que el número es menor
    
    # SELECCIÓN: Mensaje final
    if not adivinado: # Si no se adivinó el número
        print(f"\n¡Agotaste tus intentos! El número era {numero_secreto}") # Imprime el número secreto

# ============ FUNCIÓN PRINCIPAL ============
def main():
    """Función principal que ejecuta todas las demostraciones"""
    print("DEMOSTRACIÓN DE ESTRUCTURAS DE CONTROL")
    print("-------------------------------------")
    
    # 1. Demostrar secuencia
    demostrar_secuencia()
    
    # 2. Demostrar selección con diferentes edades
    demostrar_seleccion(15)
    demostrar_seleccion(25)
    demostrar_seleccion(8)
    
    # 3. Demostrar iteración
    demostrar_iteracion()
    
    # 4. Ejemplo integrado
    juego_adivinanza()

if __name__ == "__main__":
    main() # Llama a la función principal si el script se ejecuta directamente
