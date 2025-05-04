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
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
import math

# ============ CLASE BASE: VEHÍCULO ============
class Vehiculo:
    """
    Clase base que representa un vehículo genérico.
    Demuestra atributos de instancia, métodos y herencia.
    """
    
    # Atributo de clase (compartido por todas las instancias)
    cantidad_total_vehiculos = 0
    
    def __init__(self, marca: str, modelo: str, año: int):
        """
        Constructor - Inicializa los atributos del vehículo
        
        Args:
            marca: Marca del vehículo
            modelo: Modelo específico
            año: Año de fabricación
        """
        # Atributos de instancia (únicos para cada objeto)
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.kilometraje = 0  # Inicializado en 0
        self.encendido = False
        
        # Incrementar contador de vehículos
        Vehiculo.cantidad_total_vehiculos += 1
    
    def encender(self) -> None:
        """Método para encender el vehículo"""
        if not self.encendido:
            self.encendido = True
            print(f"{self.marca} {self.modelo} encendido")
        else:
            print("El vehículo ya está encendido")
    
    def apagar(self) -> None:
        """Método para apagar el vehículo"""
        if self.encendido:
            self.encendido = False
            print(f"{self.marca} {self.modelo} apagado")
        else:
            print("El vehículo ya está apagado")
    
    def conducir(self, distancia: float) -> None:
        """
        Método para simular la conducción del vehículo
        
        Args:
            distancia: Kilómetros a conducir
        """
        if self.encendido:
            self.kilometraje += distancia
            print(f"Conduciendo {distancia} km. Kilometraje total: {self.kilometraje} km")
        else:
            print("Error: El vehículo está apagado")
    
    def obtener_edad(self) -> int:
        """Calcula la edad del vehículo en años"""
        año_actual = datetime.now().year
        return año_actual - self.año
    
    @classmethod
    def get_cantidad_vehiculos(cls) -> int:
        """Método de clase para obtener el total de vehículos creados"""
        return cls.cantidad_total_vehiculos
    
    @staticmethod
    def validar_año(año: int) -> bool:
        """Método estático para validar el año de fabricación"""
        return 1886 <= año <= datetime.now().year  # 1886 = primer auto patentado
    
    def __str__(self) -> str:
        """Representación legible del objeto"""
        return f"{self.marca} {self.modelo} ({self.año}) - {self.kilometraje} km"

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
        super().__init__(marca, modelo, año)  # Llama al constructor de Vehiculo
        self.puertas = puertas
        self.pasajeros: List[str] = []
    
    def agregar_pasajero(self, nombre: str) -> None:
        """Método para agregar pasajeros al automóvil"""
        if len(self.pasajeros) < 4:  # Capacidad máxima de 4 pasajeros
            self.pasajeros.append(nombre)
            print(f"{nombre} ha subido al automóvil")
        else:
            print("El automóvil está lleno")
    
    def quitar_pasajero(self, nombre: str) -> None:
        """Método para quitar pasajeros del automóvil"""
        if nombre in self.pasajeros:
            self.pasajeros.remove(nombre)
            print(f"{nombre} ha bajado del automóvil")
        else:
            print(f"{nombre} no está en el automóvil")
    
    def conducir(self, distancia: float) -> None:
        """Sobrescribe el método conducir de Vehiculo"""
        if not self.pasajeros:
            print("Error: No hay conductor en el automóvil")
        else:
            super().conducir(distancia)  # Llama al método de la clase base
    
    def __str__(self) -> str:
        """Sobrescribe la representación de cadena"""
        base_str = super().__str__()
        return f"{base_str}, {self.puertas} puertas, Pasajeros: {self.pasajeros}"

# ============ CLASE DERIVADA: MOTOCICLETA ============
class Motocicleta(Vehiculo):
    """
    Otra clase derivada que demuestra polimorfismo.
    """
    
    def __init__(self, marca: str, modelo: str, año: int, estilo: str):
        super().__init__(marca, modelo, año)
        self.estilo = estilo  # Ej: deportiva, cruiser, touring
        self.casco_puesto = False
    
    def poner_casco(self) -> None:
        """Método específico para motocicletas"""
        self.casco_puesto = True
        print("Casco puesto correctamente")
    
    def quitar_casco(self) -> None:
        """Método específico para motocicletas"""
        self.casco_puesto = False
        print("Casco quitado")
    
    def conducir(self, distancia: float) -> None:
        """Sobrescribe el método conducir con requisito de casco"""
        if not self.casco_puesto:
            print("Error: Debes ponerte el casco primero")
        else:
            super().conducir(distancia)
    
    def __str__(self) -> str:
        """Representación específica para motocicletas"""
        return f"{super().__str__()} - Estilo: {self.estilo}"

# ============ EJEMPLO DE USO ============
def demo_poo():
    """Función que demuestra todos los conceptos de POO"""
    print("\n=== DEMOSTRACIÓN DE PROGRAMACIÓN ORIENTADA A OBJETOS ===")
    
    # 1. Creación de objetos
    print("\n1. Creación de objetos:")
    auto1 = Automovil("Toyota", "Corolla", 2020, 4)
    moto1 = Motocicleta("Harley-Davidson", "Sportster", 2019, "cruiser")
    
    print(f" - Automóvil creado: {auto1}")
    print(f" - Motocicleta creada: {moto1}")
    
    # 2. Uso de métodos
    print("\n2. Interacción con métodos:")
    auto1.encender()
    auto1.conducir(50)  # No debería funcionar sin conductor
    
    auto1.agregar_pasajero("Juan")
    auto1.conducir(50)
    auto1.conducir(30)
    auto1.agregar_pasajero("María")
    print(f" - Estado actual: {auto1}")
    
    moto1.encender()
    moto1.conducir(100)  # Debería fallar sin casco
    moto1.poner_casco()
    moto1.conducir(100)
    
    # 3. Atributos y métodos especiales
    print("\n3. Atributos y métodos especiales:")
    print(f" - Edad del automóvil: {auto1.obtener_edad()} años")
    print(f" - Estilo de la moto: {moto1.estilo}")
    
    # 4. Métodos de clase y estáticos
    print("\n4. Métodos de clase y estáticos:")
    print(f" - Total de vehículos creados: {Vehiculo.get_cantidad_vehiculos()}")
    print(f" - ¿Año 3000 válido?: {Vehiculo.validar_año(3000)}")
    
    # 5. Polimorfismo
    print("\n5. Demostración de polimorfismo:")
    vehiculos: List[Vehiculo] = [
        auto1,
        moto1,
        Automovil("Ford", "Mustang", 2022, 2),
        Motocicleta("Yamaha", "YZF-R1", 2021, "deportiva")
    ]
    
    for vehiculo in vehiculos:
        vehiculo.encender()
        if isinstance(vehiculo, Automovil):
            vehiculo.agregar_pasajero("Conductor")
        elif isinstance(vehiculo, Motocicleta):
            vehiculo.poner_casco()
        vehiculo.conducir(10)
        print(f" - {vehiculo}\n")

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
        self.vehiculos.append(vehiculo)
        print(f"Vehículo agregado a {self.nombre}: {vehiculo.marca} {vehiculo.modelo}")
    
    def mostrar_inventario(self) -> None:
        """Muestra todos los vehículos en el inventario"""
        print(f"\nInventario de {self.nombre}:")
        for i, vehiculo in enumerate(self.vehiculos, 1):
            print(f"{i}. {vehiculo}")
    
    def buscar_por_marca(self, marca: str) -> List[Vehiculo]:
        """Busca vehículos por marca"""
        return [v for v in self.vehiculos if v.marca.lower() == marca.lower()]

def demo_concesionaria():
    """Demuestra el uso de la clase Concesionaria"""
    print("\n=== DEMOSTRACIÓN DE COMPOSICIÓN ===")
    
    # Crear concesionaria
    autocity = Concesionaria("AutoCity", "Av. Principal 1234")
    
    # Agregar vehículos
    autocity.agregar_vehiculo(Automovil("Toyota", "Hilux", 2023, 4))
    autocity.agregar_vehiculo(Motocicleta("Honda", "CBR600", 2022, "deportiva"))
    autocity.agregar_vehiculo(Automovil("Ford", "Fiesta", 2021, 2))
    
    # Mostrar inventario
    autocity.mostrar_inventario()
    
    # Buscar por marca
    print("\nVehículos Toyota en inventario:")
    for vehiculo in autocity.buscar_por_marca("toyota"):
        print(f" - {vehiculo}")

# ============ FUNCIÓN PRINCIPAL ============
if __name__ == "__main__":
    # Demostración de conceptos básicos
    demo_poo()
    
    # Demostración adicional de composición
    demo_concesionaria()