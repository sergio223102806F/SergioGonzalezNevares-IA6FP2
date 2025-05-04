"""
ESTRUCTURAS DE CONTROL FUNDAMENTALES - 
-------------------------------------------------------------
Este código demuestra las tres estructuras básicas de programación estructurada:
1. Secuencia - Ejecución lineal de instrucciones
2. Selección - Toma de decisiones (if/else)
3. Iteración - Bucles (while, for)
"""

# ============ IMPORTACIONES ============
from typing import List, Dict, Optional
import random

# ============ SECUENCIA ============
def demostrar_secuencia() -> None:
    """
    DEMOSTRACIÓN DE SECUENCIA
    -------------------------
    Ejecución lineal de instrucciones, una después de otra.
    """
    print("\n=== SECUENCIA ===")
    
    # Instrucción 1
    resultado_suma = 5 + 3
    print(f"1. Suma: 5 + 3 = {resultado_suma}")
    
    # Instrucción 2
    resultado_resta = 10 - 2
    print(f"2. Resta: 10 - 2 = {resultado_resta}")
    
    # Instrucción 3
    resultado_final = resultado_suma * resultado_resta
    print(f"3. Multiplicación: {resultado_suma} * {resultado_resta} = {resultado_final}")
    
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
    if edad >= 18:
        print(" - Eres mayor de edad")
    
    # If-else
    if edad < 12:
        print(" - Eres un niño")
    else:
        print(" - Ya no eres un niño")
    
    # If-elif-else múltiple
    if edad < 0:
        print(" - Edad no válida (negativa)")
    elif 0 <= edad < 3:
        print(" - Bebé")
    elif 3 <= edad < 12:
        print(" - Niño")
    elif 12 <= edad < 18:
        print(" - Adolescente")
    elif 18 <= edad < 65:
        print(" - Adulto")
    else:
        print(" - Adulto mayor")

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
    contador = 3
    while contador > 0:
        print(f"   Contador: {contador}")
        contador -= 1  # Decremento
    
    # Bucle for - Iteración sobre secuencia
    print("\n2. Bucle FOR (sobre secuencia):")
    frutas = ["manzana", "banana", "cereza"]
    for i, fruta in enumerate(frutas, 1):
        print(f"   Fruta {i}: {fruta}")
    
    # Bucle con break/continue
    print("\n3. Bucle con CONTROL (break/continue):")
    for num in range(1, 6):
        if num == 3:
            print("   Saltando el 3 con continue")
            continue
        if num == 5:
            print("   Rompiendo en 5 con break")
            break
        print(f"   Número actual: {num}")

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
    numero_secreto = random.randint(1, 10)
    intentos = 3
    adivinado = False
    
    print("Adivina un número entre 1 y 10. Tienes 3 intentos.")
    
    # ITERACIÓN: Bucle principal del juego
    while intentos > 0 and not adivinado:
        # SECUENCIA: Dentro de cada iteración
        try:
            intento = int(input("\nTu suposición: "))
        except ValueError:
            print("¡Debes ingresar un número!")
            continue
        
        # SELECCIÓN: Evaluar el intento
        if intento == numero_secreto:
            print("¡Correcto! ¡Has adivinado!")
            adivinado = True
        else:
            intentos -= 1
            if intento < numero_secreto:
                print(f"El número es mayor. Intentos restantes: {intentos}")
            else:
                print(f"El número es menor. Intentos restantes: {intentos}")
    
    # SELECCIÓN: Mensaje final
    if not adivinado:
        print(f"\n¡Agotaste tus intentos! El número era {numero_secreto}")

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
    main()