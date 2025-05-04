# Importamos el módulo abc (Abstract Base Classes) para crear clases abstractas
from abc import ABC, abstractmethod

"""
HERENCIA MÚLTIPLE:
Python permite que una clase herede de múltiples clases padres.
Esto se conoce como herencia múltiple.
"""

# Definimos una clase base para animales
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre
    
    def hacer_sonido(self):
        print("Sonido genérico de animal")

# Definimos una clase para habilidades de mascota
class Mascota:
    def __init__(self, dueno):
        self.dueno = dueno
    
    def jugar(self):
        print(f"{self.nombre} está jugando con {self.dueno}")

# Clase que hereda de ambas (herencia múltiple)
class Perro(Animal, Mascota):
    def __init__(self, nombre, dueno):
        # Llamamos a los constructores de ambas clases padres
        Animal.__init__(self, nombre)
        Mascota.__init__(self, dueno)
    
    # Sobreescribimos el método de Animal
    def hacer_sonido(self):
        print("¡Guau guau!")

"""
POLIMORFISMO:
Capacidad de diferentes clases para responder al mismo mensaje/método
de manera diferente.
"""

# Otra clase que hereda de Animal
class Gato(Animal):
    def hacer_sonido(self):
        print("¡Miau miau!")

# Función que demuestra polimorfismo
def hacer_sonido_animal(animal):
    animal.hacer_sonido()

"""
CLASE ABSTRACTA:
Una clase que no puede ser instanciada y que puede contener métodos abstractos
que deben ser implementados por las clases hijas.
"""

# Definimos una clase abstracta usando el módulo abc
class FiguraGeometrica(ABC):
    @abstractmethod
    def area(self):
        pass  # Las clases hijas deben implementar este método
    
    @abstractmethod
    def perimetro(self):
        pass  # Las clases hijas deben implementar este método
    
    # Método concreto (no abstracto) que pueden heredar todas las subclases
    def descripcion(self):
        return "Esta es una figura geométrica"

# Clase concreta que implementa la clase abstracta
class Rectangulo(FiguraGeometrica):
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
    
    def area(self):
        return self.ancho * self.alto
    
    def perimetro(self):
        return 2 * (self.ancho + self.alto)

# Otra clase concreta que implementa la clase abstracta
class Circulo(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = radio
    
    def area(self):
        return 3.1416 * (self.radio ** 2)
    
    def perimetro(self):
        return 2 * 3.1416 * self.radio

# Ejemplo de uso
if __name__ == "__main__":
    print("\n--- HERENCIA MÚLTIPLE ---")
    mi_perro = Perro("Fido", "Juan")
    mi_perro.hacer_sonido()  # Método de Animal
    mi_perro.jugar()         # Método de Mascota
    
    print("\n--- POLIMORFISMO ---")
    animales = [Perro("Rex", "Ana"), Gato("Misi")]
    for animal in animales:
        hacer_sonido_animal(animal)  # Mismo método, comportamientos diferentes
    
    print("\n--- CLASE ABSTRACTA ---")
    figuras = [Rectangulo(4, 5), Circulo(3)]
    for figura in figuras:
        print(f"Área: {figura.area()}, Perímetro: {figura.perimetro()}")
        print(figura.descripcion())
    
    # Esto daría error porque no se puede instanciar una clase abstracta
    # figura = FiguraGeometrica()