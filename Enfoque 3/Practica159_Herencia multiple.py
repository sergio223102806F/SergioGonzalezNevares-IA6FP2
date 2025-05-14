# Importamos el módulo abc (Abstract Base Classes) para crear clases abstractas
from abc import ABC, abstractmethod # Importa las clases ABC y abstractmethod del módulo abc

"""
HERENCIA MÚLTIPLE:
Python permite que una clase herede de múltiples clases padres.
Esto se conoce como herencia múltiple.
"""

# Definimos una clase base para animales
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre # Inicializa el atributo nombre del animal
    
    def hacer_sonido(self):
        print("Sonido genérico de animal") # Imprime un sonido genérico para los animales

# Definimos una clase para habilidades de mascota
class Mascota:
    def __init__(self, dueno):
        self.dueno = dueno # Inicializa el atributo dueno de la mascota
    
    def jugar(self):
        print(f"{self.nombre} está jugando con {self.dueno}") # Imprime un mensaje indicando que la mascota está jugando

# Clase que hereda de ambas (herencia múltiple)
class Perro(Animal, Mascota):
    def __init__(self, nombre, dueno):
        # Llamamos a los constructores de ambas clases padres
        Animal.__init__(self, nombre) # Llama al constructor de la clase Animal
        Mascota.__init__(self, dueno) # Llama al constructor de la clase Mascota
    
    # Sobreescribimos el método de Animal
    def hacer_sonido(self):
        print("¡Guau guau!") # Imprime el sonido específico de un perro

"""
POLIMORFISMO:
Capacidad de diferentes clases para responder al mismo mensaje/método
de manera diferente.
"""

# Otra clase que hereda de Animal
class Gato(Animal):
    def hacer_sonido(self):
        print("¡Miau miau!") # Imprime el sonido específico de un gato

# Función que demuestra polimorfismo
def hacer_sonido_animal(animal):
    animal.hacer_sonido() # Llama al método hacer_sonido del objeto animal

"""
CLASE ABSTRACTA:
Una clase que no puede ser instanciada y que puede contener métodos abstractos
que deben ser implementados por las clases hijas.
"""

# Definimos una clase abstracta usando el módulo abc
class FiguraGeometrica(ABC):
    @abstractmethod
    def area(self):
        pass  # Las clases hijas deben implementar este método # Método abstracto para calcular el área
    
    @abstractmethod
    def perimetro(self):
        pass  # Las clases hijas deben implementar este método # Método abstracto para calcular el perímetro
    
    # Método concreto (no abstracto) que pueden heredar todas las subclases
    def descripcion(self):
        return "Esta es una figura geométrica" # Devuelve una descripción de la figura geométrica

# Clase concreta que implementa la clase abstracta
class Rectangulo(FiguraGeometrica):
    def __init__(self, ancho, alto):
        self.ancho = ancho # Inicializa el atributo ancho del rectángulo
        self.alto = alto # Inicializa el atributo alto del rectángulo
    
    def area(self):
        return self.ancho * self.alto # Calcula el área del rectángulo
    
    def perimetro(self):
        return 2 * (self.ancho + self.alto) # Calcula el perímetro del rectángulo

# Otra clase concreta que implementa la clase abstracta
class Circulo(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = radio # Inicializa el atributo radio del círculo
    
    def area(self):
        return 3.1416 * (self.radio ** 2) # Calcula el área del círculo
    
    def perimetro(self):
        return 2 * 3.1416 * self.radio # Calcula el perímetro del círculo

# Ejemplo de uso
if __name__ == "__main__":
    print("\n--- HERENCIA MÚLTIPLE ---")
    mi_perro = Perro("Fido", "Juan") # Crea un objeto Perro
    mi_perro.hacer_sonido()  # Método de Animal # Llama al método hacer_sonido de la clase Animal (sobreescrito en Perro)
    mi_perro.jugar()        # Método de Mascota # Llama al método jugar de la clase Mascota
    
    print("\n--- POLIMORFISMO ---")
    animales = [Perro("Rex", "Ana"), Gato("Misi")] # Crea una lista de objetos Animal (Perro y Gato)
    for animal in animales:
        hacer_sonido_animal(animal)  # Mismo método, comportamientos diferentes # Llama a la función hacer_sonido_animal con diferentes objetos Animal
    
    print("\n--- CLASE ABSTRACTA ---")
    figuras = [Rectangulo(4, 5), Circulo(3)] # Crea una lista de objetos FiguraGeometrica (Rectangulo y Circulo)
    for figura in figuras:
        print(f"Área: {figura.area()}, Perímetro: {figura.perimetro()}") # Imprime el área y el perímetro de cada figura
        print(figura.descripcion()) # Llama al método descripcion de la clase FiguraGeometrica
    
    # Esto daría error porque no se puede instanciar una clase abstracta
    # figura = FiguraGeometrica() # Intenta crear una instancia de la clase abstracta FiguraGeometrica (generará un error)
