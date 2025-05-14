from abc import ABC, abstractmethod # Importa ABC y abstractmethod del módulo abc para definir clases abstractas y métodos abstractos

# **Clase Abstracta**
class FiguraGeometrica(ABC): # Define una clase abstracta llamada FiguraGeometrica que hereda de ABC
    @abstractmethod
    def area(self): pass # Define un método abstracto llamado area que debe ser implementado por las subclases

# **Herencia Múltiple**
class Animal: # Define una clase llamada Animal
    def comer(self): print("Comiendo...") # Define un método comer que imprime "Comiendo..."

class Mascota: # Define una clase llamada Mascota
    def jugar(self): print("Jugando...") # Define un método jugar que imprime "Jugando..."

class Perro(Animal, Mascota):  # Herencia múltiple # Define una clase llamada Perro que hereda de Animal y Mascota
    def ladrar(self): print("¡Guau!") # Define un método ladrar que imprime "¡Guau!"

# **Polimorfismo**
class Rectangulo(FiguraGeometrica): # Define una clase llamada Rectangulo que hereda de FiguraGeometrica
    def __init__(self, ancho, alto): # Define el constructor de la clase Rectangulo que recibe ancho y alto
        self.ancho = ancho # Inicializa el atributo ancho del rectángulo
        self.alto = alto # Inicializa el atributo alto del rectángulo
    def area(self): return self.ancho * self.alto # Define el método area que calcula y devuelve el área del rectángulo

# Uso
figura = Rectangulo(4, 5) # Crea una instancia de la clase Rectangulo con ancho 4 y alto 5
print("Área:", figura.area()) # Llama al método area del objeto figura e imprime el resultado

perro = Perro() # Crea una instancia de la clase Perro
perro.comer() # Llama al método comer del objeto perro
perro.jugar() # Llama al método jugar del objeto perro

