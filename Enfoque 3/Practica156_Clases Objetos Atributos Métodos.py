"""
PROGRAMACIÓN ORIENTADA A OBJETOS -
-----------------------------------------------------------
Este código demuestra los conceptos fundamentales de POO:
1. Clases - Plantillas para crear objetos
2. Objetos - Instancias de clases
3. Atributos - Datos asociados a objetos
4. Métodos - Funciones asociadas a objetos
"""

# ============ IMPORTACIONES ============
from typing import List, Optional # Importa tipos para anotaciones de tipo
from dataclasses import dataclass # Importa el decorador dataclass para crear clases de datos
from datetime import datetime # Importa la clase datetime del módulo datetime
import math # Importa el módulo math (no se usa directamente en el código proporcionado, pero se incluye como parte del contexto general)

# ============ CLASE BASE: VEHÍCULO ============
class Vehiculo:
    """
    Clase base que representa un vehículo genérico.
    Demuestra atributos de instancia, métodos y herencia.
    """
    
    # Atributo de clase (compartido por todas las instancias)
    cantidad_total_vehiculos = 0 # Variable de clase que cuenta el número total de vehículos creados
    
    def __init__(self, marca: str, modelo: str, año: int):
        """
        Constructor - Inicializa los atributos del vehículo
        
        Args:
            marca: Marca del vehículo
            modelo: Modelo específico
            año: Año de fabricación
        """
        # Atributos de instancia (únicos para cada objeto)
        self.marca = marca # Atributo de instancia: marca del vehículo
        self.modelo = modelo # Atributo de instancia: modelo del vehículo
        self.año = año # Atributo de instancia: año de fabricación
        self.kilometraje = 0  # Inicializado en 0 # Atributo de instancia: kilometraje del vehículo, inicializado en 0
        self.encendido = False # Atributo de instancia: estado del vehículo (encendido o apagado), inicializado en False
        
        # Incrementar contador de vehículos
        Vehiculo.cantidad_total_vehiculos += 1 # Incrementa el contador de vehículos cada vez que se crea un nuevo objeto Vehiculo
    
    def encender(self) -> None:
        """Método para encender el vehículo"""
        if not self.encendido: # Si el vehículo no está encendido
            self.encendido = True # Cambia el estado a encendido
            print(f"{self.marca} {self.modelo} encendido") # Imprime un mensaje indicando que el vehículo se ha encendido
        else: # Si el vehículo ya está encendido
            print("El vehículo ya está encendido") # Imprime un mensaje indicando que el vehículo ya estaba encendido
    
    def apagar(self) -> None:
        """Método para apagar el vehículo"""
        if self.encendido: # Si el vehículo está encendido
            self.encendido = False # Cambia el estado a apagado
            print(f"{self.marca} {self.modelo} apagado") # Imprime un mensaje indicando que el vehículo se ha apagado
        else: # Si el vehículo ya está apagado
            print("El vehículo ya está apagado") # Imprime un mensaje indicando que el vehículo ya estaba apagado
    
    def conducir(self, distancia: float) -> None:
        """
        Método para simular la conducción del vehículo
        
        Args:
            distancia: Kilómetros a conducir
        """
        if self.encendido: # Si el vehículo está encendido
            self.kilometraje += distancia # Incrementa el kilometraje
            print(f"Conduciendo {distancia} km. Kilometraje total: {self.kilometraje} km") # Imprime la distancia conducida y el kilometraje total
        else: # Si el vehículo está apagado
            print("Error: El vehículo está apagado") # Imprime un mensaje de error
    
    def obtener_edad(self) -> int:
        """Calcula la edad del vehículo en años"""
        año_actual = datetime.now().year # Obtiene el año actual
        return año_actual - self.año # Calcula la edad restando el año de fabricación al año actual
    
    @classmethod
    def get_cantidad_vehiculos(cls) -> int:
        """Método de clase para obtener el total de vehículos creados"""
        return cls.cantidad_total_vehiculos # Devuelve el valor del atributo de clase cantidad_total_vehiculos
    
    @staticmethod
    def validar_año(año: int) -> bool:
        """Método estático para validar el año de fabricación"""
        return 1886 <= año <= datetime.now().year  # 1886 = primer auto patentado # Devuelve True si el año está dentro del rango válido, False en caso contrario
    
    def __str__(self) -> str:
        """Representación legible del objeto"""
        return f"{self.marca} {self.modelo} ({self.año}) - {self.kilometraje} km" # Devuelve una cadena formateada con la marca, modelo, año y kilometraje del vehículo

# ============ CLASE DERIVADA: AUTOMÓVIL ============
class Automovil(Vehiculo):
    """
    Clase derivada que representa un automóvil específico.
    Demuestra herencia y especialización.
    """
    
    def __init__(self, marca: str, modelo: str, año: int, puertas: int):
        """
        Constructor de Automovil
        
        Args:
            puertas: Número de puertas (atributo específico)
        """
        super().__init__(marca, modelo, año)  # Llama al constructor de Vehiculo # Llama al constructor de la clase base (Vehiculo) para inicializar los atributos heredados
        self.puertas = puertas # Atributo de instancia: número de puertas del automóvil
        self.pasajeros: List[str] = [] # Atributo de instancia: lista de pasajeros en el automóvil, inicializada como una lista vacía
    
    def agregar_pasajero(self, nombre: str) -> None:
        """Método para agregar pasajeros al automóvil"""
        if len(self.pasajeros) < 4:  # Capacidad máxima de 4 pasajeros # Si hay menos de 4 pasajeros en el automóvil
            self.pasajeros.append(nombre) # Agrega el nombre del pasajero a la lista
            print(f"{nombre} ha subido al automóvil") # Imprime un mensaje indicando que el pasajero ha subido
        else: # Si el automóvil está lleno
            print("El automóvil está lleno") # Imprime un mensaje indicando que el automóvil está lleno
    
    def quitar_pasajero(self, nombre: str) -> None:
        """Método para quitar pasajeros del automóvil"""
        if nombre in self.pasajeros: # Si el nombre del pasajero está en la lista de pasajeros
            self.pasajeros.remove(nombre) # Elimina el nombre de la lista
            print(f"{nombre} ha bajado del automóvil") # Imprime un mensaje indicando que el pasajero ha bajado
        else: # Si el pasajero no está en el automóvil
            print(f"{nombre} no está en el automóvil") # Imprime un mensaje indicando que el pasajero no está en el automóvil
    
    def conducir(self, distancia: float) -> None:
        """Sobrescribe el método conducir de Vehiculo"""
        if not self.pasajeros: # Si no hay pasajeros en el automóvil
            print("Error: No hay conductor en el automóvil") # Imprime un mensaje de error
        else: # Si hay al menos un pasajero (conductor)
            super().conducir(distancia)  # Llama al método de la clase base # Llama al método conducir de la clase base (Vehiculo) para simular la conducción
    
    def __str__(self) -> str:
        """Sobrescribe la representación de cadena"""
        base_str = super().__str__() # Obtiene la representación de cadena de la clase base
        return f"{base_str}, {self.puertas} puertas, Pasajeros: {self.pasajeros}" # Devuelve una cadena formateada que incluye la información del automóvil y el número de puertas y la lista de pasajeros

# ============ CLASE DERIVADA: MOTOCICLETA ============
class Motocicleta(Vehiculo):
    """
    Otra clase derivada que demuestra polimorfismo.
    """
    
    def __init__(self, marca: str, modelo: str, año: int, estilo: str):
        super().__init__(marca, modelo, año) # Llama al constructor de la clase base (Vehiculo)
        self.estilo = estilo  # Ej: deportiva, cruiser, touring # Atributo de instancia: estilo de la motocicleta
        self.casco_puesto = False # Atributo de instancia: indica si el casco está puesto, inicializado en False
    
    def poner_casco(self) -> None:
        """Método específico para motocicletas"""
        self.casco_puesto = True # Cambia el estado del casco a puesto
        print("Casco puesto correctamente") # Imprime un mensaje
    
    def quitar_casco(self) -> None:
        """Método específico para motocicletas"""
        self.casco_puesto = False # Cambia el estado del casco a quitado
        print("Casco quitado") # Imprime un mensaje
    
    def conducir(self, distancia: float) -> None:
        """Sobrescribe el método conducir con requisito de casco"""
        if not self.casco_puesto: # Si el casco no está puesto
            print("Error: Debes ponerte el casco primero") # Imprime un mensaje de error
        else: # Si el casco está puesto
            super().conducir(distancia) # Llama al método conducir de la clase base
    
    def __str__(self) -> str:
        """Representación específica para motocicletas"""
        return f"{super().__str__()} - Estilo: {self.estilo}" # Devuelve una cadena formateada que incluye la información de la motocicleta y su estilo

# ============ EJEMPLO DE USO ============
def demo_poo():
    """Función que demuestra todos los conceptos de POO"""
    print("\n=== DEMOSTRACIÓN DE PROGRAMACIÓN ORIENTADA A OBJETOS ===")
    
    # 1. Creación de objetos
    print("\n1. Creación de objetos:")
    auto1 = Automovil("Toyota", "Corolla", 2020, 4) # Crea un objeto Automovil
    moto1 = Motocicleta("Harley-Davidson", "Sportster", 2019, "cruiser") # Crea un objeto Motocicleta
    
    print(f" - Automóvil creado: {auto1}") # Imprime la representación del objeto auto1
    print(f" - Motocicleta creada: {moto1}") # Imprime la representación del objeto moto1
    
    # 2. Uso de métodos
    print("\n2. Interacción con métodos:")
    auto1.encender() # Enciende el automóvil
    auto1.conducir(50)  # No debería funcionar sin conductor # Intenta conducir sin conductor
    
    auto1.agregar_pasajero("Juan") # Agrega un pasajero al automóvil
    auto1.conducir(50) # Conduce el automóvil
    auto1.conducir(30)
    auto1.agregar_pasajero("María")
    print(f" - Estado actual: {auto1}")
    
    moto1.encender()
    moto1.conducir(100)  # Debería fallar sin casco
    moto1.poner_casco()
    moto1.conducir(100)
    
    # 3. Atributos y métodos especiales
    print("\n3. Atributos y métodos especiales:")
    print(f" - Edad del automóvil: {auto1.obtener_edad()} años") # Imprime la edad del automóvil
    print(f" - Estilo de la moto: {moto1.estilo}") # Imprime el estilo de la motocicleta
    
    # 4. Métodos de clase y estáticos
    print("\n4. Métodos de clase y estáticos:")
    print(f" - Total de vehículos creados: {Vehiculo.get_cantidad_vehiculos()}") # Imprime el número total de vehículos creados
    print(f" - ¿Año 3000 válido?: {Vehiculo.validar_año(3000)}") # Imprime si el año 3000 es válido
    
    # 5. Polimorfismo
    print("\n5. Demostración de polimorfismo:")
    vehiculos: List[Vehiculo] = [ # Crea una lista de objetos Vehiculo (incluyendo Automovil y Motocicleta)
        auto1,
        moto1,
        Automovil("Ford", "Mustang", 2022, 2),
        Motocicleta("Yamaha", "YZF-R1", 2021, "deportiva")
    ]
    
    for vehiculo in vehiculos: # Itera sobre la lista de vehículos
        vehiculo.encender() # Enciende cada vehículo
        if isinstance(vehiculo, Automovil): # Si el vehículo es un Automovil
            vehiculo.agregar_pasajero("Conductor") # Agrega un conductor
        elif isinstance(vehiculo, Motocicleta): # Si el vehículo es una Motocicleta
            vehiculo.poner_casco() # Pone el casco
        vehiculo.conducir(10) # Conduce 10 km
        print(f" - {vehiculo}\n") # Imprime la representación del vehículo

# ============ CLASE ADICIONAL: CONCESIONARIA ============
@dataclass
class Concesionaria:
    """
    Clase que demuestra composición de objetos.
    Una concesionaria contiene muchos vehículos.
    """
    nombre: str
    direccion: str
    vehiculos: List[Vehiculo] = None
    
    def __post_init__(self):
        """Inicializa la lista de vehículos si es None"""
        if self.vehiculos is None:
            self.vehiculos = []
    
    def agregar_vehiculo(self, vehiculo: Vehiculo) -> None:
        """Agrega un vehículo al inventario"""
        self.vehiculos.append(vehiculo) # Agrega el vehículo a la lista de vehículos de la concesionaria
        print(f"Vehículo agregado a {self.nombre}: {vehiculo.marca} {vehiculo.modelo}") # Imprime un mensaje indicando qué vehículo se agregó
    
    def mostrar_inventario(self) -> None:
        """Muestra todos los vehículos en el inventario"""
        print(f"\nInventario de {self.nombre}:") # Imprime el nombre de la concesionaria
        for i, vehiculo in enumerate(self.vehiculos, 1): # Itera sobre la lista de vehículos con un índice
            print(f"{i}. {vehiculo}") # Imprime el índice y la representación de cada vehículo
    
    def buscar_por_marca(self, marca: str) -> List[Vehiculo]:
        """Busca vehículos por marca"""
        return [v for v in self.vehiculos if v.marca.lower() == marca.lower()] # Devuelve una lista de vehículos cuya marca coincide con la marca buscada (insensible a mayúsculas)

def demo_concesionaria():
    """Demuestra el uso de la clase Concesionaria"""
    print("\n=== DEMOSTRACIÓN DE COMPOSICIÓN ===")
    
    # Crear concesionaria
    autocity = Concesionaria("AutoCity", "Av. Principal 1234") # Crea una instancia de la clase Concesionaria
    
    # Agregar vehículos
    autocity.agregar_vehiculo(Automovil("Toyota", "Hilux", 2023, 4)) # Agrega un automóvil a la concesionaria
    autocity.agregar_vehiculo(Motocicleta("Honda", "CBR600", 2022, "deportiva")) # Agrega una motocicleta a la concesionaria
    autocity.agregar_vehiculo(Automovil("Ford", "Fiesta", 2021, 2)) # Agrega otro automóvil a la concesionaria
    
    # Mostrar inventario
    autocity.mostrar_inventario() # Muestra el inventario de la concesionaria
    
    # Buscar por marca
    print("\nVehículos Toyota en inventario:") # Imprime un encabezado
    for vehiculo in autocity.buscar_por_marca("toyota"): # Busca vehículos de la marca "toyota"
        print(f" - {vehiculo}") # Imprime la representación de cada vehículo encontrado

# ============ FUNCIÓN PRINCIPAL ============
if __name__ == "__main__":
    # Demostración de conceptos básicos
    demo_poo()
    
    # Demostración adicional de composición
    demo_concesionaria()
