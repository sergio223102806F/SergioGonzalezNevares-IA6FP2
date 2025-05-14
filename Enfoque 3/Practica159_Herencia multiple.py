# Importamos el m�dulo abc (Abstract Base Classes) para crear clases abstractas
from abc import ABC, abstractmethod # Importa las clases ABC y abstractmethod del m�dulo abc

"""
HERENCIA M�LTIPLE:
Python permite que una clase herede de m�ltiples clases padres.
Esto se conoce como herencia m�ltiple.
"""

# Definimos una clase base para animales
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre # Inicializa el atributo nombre del animal
    
    def hacer_sonido(self):
        print("Sonido gen�rico de animal") # Imprime un sonido gen�rico para los animales

# Definimos una clase para habilidades de mascota
class Mascota:
    def __init__(self, dueno):
        self.dueno = dueno # Inicializa el atributo dueno de la mascota
    
    def jugar(self):
        print(f"{self.nombre} est� jugando con {self.dueno}") # Imprime un mensaje indicando que la mascota est� jugando

# Clase que hereda de ambas (herencia m�ltiple)
class Perro(Animal, Mascota):
    def __init__(self, nombre, dueno):
        # Llamamos a los constructores de ambas clases padres
        Animal.__init__(self, nombre) # Llama al constructor de la clase Animal
        Mascota.__init__(self, dueno) # Llama al constructor de la clase Mascota
    
    # Sobreescribimos el m�todo de Animal
    def hacer_sonido(self):
        print("�Guau guau!") # Imprime el sonido espec�fico de un perro

"""
POLIMORFISMO:
Capacidad de diferentes clases para responder al mismo mensaje/m�todo
de manera diferente.
"""

# Otra clase que hereda de Animal
class Gato(Animal):
    def hacer_sonido(self):
        print("�Miau miau!") # Imprime el sonido espec�fico de un gato

# Funci�n que demuestra polimorfismo
def hacer_sonido_animal(animal):
    animal.hacer_sonido() # Llama al m�todo hacer_sonido del objeto animal

"""
CLASE ABSTRACTA:
Una clase que no puede ser instanciada y que puede contener m�todos abstractos
que deben ser implementados por las clases hijas.
"""

# Definimos una clase abstracta usando el m�dulo abc
class FiguraGeometrica(ABC):
    @abstractmethod
    def area(self):
        pass  # Las clases hijas deben implementar este m�todo # M�todo abstracto para calcular el �rea
    
    @abstractmethod
    def perimetro(self):
        pass  # Las clases hijas deben implementar este m�todo # M�todo abstracto para calcular el per�metro
    
    # M�todo concreto (no abstracto) que pueden heredar todas las subclases
    def descripcion(self):
        return "Esta es una figura geom�trica" # Devuelve una descripci�n de la figura geom�trica

# Clase concreta que implementa la clase abstracta
class Rectangulo(FiguraGeometrica):
    def __init__(self, ancho, alto):
        self.ancho = ancho # Inicializa el atributo ancho del rect�ngulo
        self.alto = alto # Inicializa el atributo alto del rect�ngulo
    
    def area(self):
        return self.ancho * self.alto # Calcula el �rea del rect�ngulo
    
    def perimetro(self):
        return 2 * (self.ancho + self.alto) # Calcula el per�metro del rect�ngulo

# Otra clase concreta que implementa la clase abstracta
class Circulo(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = radio # Inicializa el atributo radio del c�rculo
    
    def area(self):
        return 3.1416 * (self.radio ** 2) # Calcula el �rea del c�rculo
    
    def perimetro(self):
        return 2 * 3.1416 * self.radio # Calcula el per�metro del c�rculo

# Ejemplo de uso
if __name__ == "__main__":
    print("\n--- HERENCIA M�LTIPLE ---")
    mi_perro = Perro("Fido", "Juan") # Crea un objeto Perro
    mi_perro.hacer_sonido()  # M�todo de Animal # Llama al m�todo hacer_sonido de la clase Animal (sobreescrito en Perro)
    mi_perro.jugar()        # M�todo de Mascota # Llama al m�todo jugar de la clase Mascota
    
    print("\n--- POLIMORFISMO ---")
    animales = [Perro("Rex", "Ana"), Gato("Misi")] # Crea una lista de objetos Animal (Perro y Gato)
    for animal in animales:
        hacer_sonido_animal(animal)  # Mismo m�todo, comportamientos diferentes # Llama a la funci�n hacer_sonido_animal con diferentes objetos Animal
    
    print("\n--- CLASE ABSTRACTA ---")
    figuras = [Rectangulo(4, 5), Circulo(3)] # Crea una lista de objetos FiguraGeometrica (Rectangulo y Circulo)
    for figura in figuras:
        print(f"�rea: {figura.area()}, Per�metro: {figura.perimetro()}") # Imprime el �rea y el per�metro de cada figura
        print(figura.descripcion()) # Llama al m�todo descripcion de la clase FiguraGeometrica
    
    # Esto dar�a error porque no se puede instanciar una clase abstracta
    # figura = FiguraGeometrica() # Intenta crear una instancia de la clase abstracta FiguraGeometrica (generar� un error)
