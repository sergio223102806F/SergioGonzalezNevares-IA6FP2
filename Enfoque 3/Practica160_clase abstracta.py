from abc import ABC, abstractmethod

# **Clase Abstracta**
class FiguraGeometrica(ABC):
    @abstractmethod
    def area(self): pass

# **Herencia Múltiple**
class Animal:
    def comer(self): print("Comiendo...")

class Mascota:
    def jugar(self): print("Jugando...")

class Perro(Animal, Mascota):  # Herencia múltiple
    def ladrar(self): print("¡Guau!")

# **Polimorfismo**
class Rectangulo(FiguraGeometrica):
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
    def area(self): return self.ancho * self.alto

# Uso
figura = Rectangulo(4, 5)
print("Área:", figura.area())

perro = Perro()
perro.comer()
perro.jugar()
