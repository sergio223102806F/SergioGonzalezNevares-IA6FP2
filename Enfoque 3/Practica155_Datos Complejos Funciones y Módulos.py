"""
DATOS COMPLEJOS, FUNCIONES Y MÓDULOS - 
---------------------------------------------------------------
Este código demuestra:
1. Estructuras de datos complejas (listas, diccionarios, objetos)
2. Funciones (definición, parámetros, retorno)
3. Organización en módulos (importación, namespaces)
"""

# ============ IMPORTACIÓN DE MÓDULOS ============
import json
from typing import List, Dict, Tuple, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import math

# ============ DEFINICIÓN DE ESTRUCTURAS DE DATOS ============
@dataclass
class Producto:
    """Clase que representa un producto en un inventario"""
    id: int
    nombre: str
    precio: float
    stock: int = 0
    ultima_actualizacion: Optional[datetime] = None

# ============ COLECCIONES COMPLEJAS ============
def demo_colecciones():
    """
    Demuestra el uso de estructuras de datos complejas:
    - Listas: Colecciones ordenadas y mutables
    - Diccionarios: Pares clave-valor
    - Tuplas: Colecciones inmutables
    - Sets: Colecciones no ordenadas y sin duplicados
    """
    print("\n=== COLECCIONES DE DATOS ===")
    
    # 1. LISTA de productos (ordenada, mutable)
    productos: List[Producto] = [
        Producto(1, "Laptop", 999.99, 10, datetime.now()),
        Producto(2, "Mouse", 19.99, 50),
        Producto(3, "Teclado", 49.99, 30)
    ]
    
    print("\n1. Lista de productos:")
    for p in productos:
        print(f" - {p.nombre}: ${p.precio} (Stock: {p.stock})")
    
    # 2. DICCIONARIO de empleados (acceso por clave)
    empleados: Dict[str, Dict] = {
        "A101": {"nombre": "Juan", "puesto": "Desarrollador", "salario": 50000},
        "B202": {"nombre": "María", "puesto": "Diseñadora", "salario": 45000}
    }
    
    print("\n2. Diccionario de empleados:")
    for id_emp, info in empleados.items():
        print(f" - {id_emp}: {info['nombre']} ({info['puesto']})")
    
    # 3. SET de categorías únicas
    categorias = {"Electrónica", "Ropa", "Hogar", "Electrónica"}  # Duplicado eliminado
    print("\n3. Set de categorías únicas:")
    print(f" - {categorias}")
    
    # 4. TUPLA de coordenadas (inmutable)
    coordenadas: Tuple[float, float] = (40.7128, -74.0060)  # Nueva York
    print("\n4. Tupla de coordenadas:")
    print(f" - Latitud: {coordenadas[0]}, Longitud: {coordenadas[1]}")

# ============ FUNCIONES AVANZADAS ============
def demo_funciones():
    """
    Demuestra características avanzadas de funciones:
    - Parámetros posicionales y nombrados
    - Valores por defecto
    - Funciones como parámetros
    - Retorno de múltiples valores
    """
    print("\n=== FUNCIONES AVANZADAS ===")
    
    # 1. Función con parámetros opcionales y retorno múltiple
    def calcular_stats(numeros: List[float]) -> Tuple[float, float, float]:
        """Calcula estadísticas básicas de una lista de números"""
        if not numeros:
            return 0.0, 0.0, 0.0
        
        suma = sum(numeros)
        promedio = suma / len(numeros)
        maximo = max(numeros)
        
        return suma, promedio, maximo
    
    datos = [12.5, 18.3, 11.7, 9.8, 15.2]
    total, prom, max_val = calcular_stats(datos)
    
    print("\n1. Retorno múltiple:")
    print(f" - Datos: {datos}")
    print(f" - Total: {total}, Promedio: {prom:.2f}, Máximo: {max_val}")
    
    # 2. Función como parámetro (orden superior)
    def aplicar_funcion(func, valores: List[float]) -> List[float]:
        """Aplica una función a cada elemento de la lista"""
        return [func(x) for x in valores]
    
    def cuadrado(x: float) -> float:
        return x ** 2
    
    def raiz_cuadrada(x: float) -> float:
        return math.sqrt(x)
    
    print("\n2. Funciones como parámetros:")
    print(f" - Cuadrados: {aplicar_funcion(cuadrado, datos)}")
    print(f" - Raíces: {aplicar_funcion(raiz_cuadrada, datos)}")
    
    # 3. Lambda (función anónima)
    print("\n3. Funciones lambda:")
    cubos = aplicar_funcion(lambda x: x**3, datos)
    print(f" - Cubos: {cubos}")

# ============ ORGANIZACIÓN EN MÓDULOS ============
def demo_modulos():
    """
    Demuestra la organización del código en módulos:
    - Importación de módulos estándar y personalizados
    - Creación de namespaces
    - Uso de __name__ == "__main__"
    """
    print("\n=== ORGANIZACIÓN EN MÓDULOS ===")
    
    # 1. Importación estándar (math)
    print("\n1. Uso de módulo math:")
    print(f" - π: {math.pi:.5f}")
    print(f" - cos(π/3): {math.cos(math.pi/3):.3f}")
    
    # 2. Importación con alias
    import datetime as dt
    hoy = dt.date.today()
    print("\n2. Uso de módulo datetime con alias:")
    print(f" - Hoy: {hoy.strftime('%d/%m/%Y')}")
    
    # 3. Importación selectiva
    from random import randint, choice
    print("\n3. Importación selectiva de random:")
    print(f" - Número aleatorio: {randint(1, 100)}")
    print(f" - Elección aleatoria: {choice(['rojo', 'verde', 'azul'])}")
    
    # 4. Módulos personalizados (ejemplo simulado)
    print("\n4. Módulos personalizados (ejemplo):")
    print("   (Normalmente estarían en archivos separados)")
    
    # Simulamos un módulo de utilidades
    class Utils:
        @staticmethod
        def formatear_moneda(monto: float) -> str:
            return f"${monto:,.2f}"
    
    print(f" - Formato monetario: {Utils.formatear_moneda(1250.75)}")

# ============ EJEMPLO INTEGRADO ============
class Tienda:
    """Clase que integra datos complejos y funciones para gestionar una tienda"""
    
    def __init__(self):
        self.inventario: Dict[int, Producto] = {}
        self.ventas: List[Dict] = []
    
    def agregar_producto(self, producto: Producto) -> None:
        """Agrega un producto al inventario"""
        self.inventario[producto.id] = producto
    
    def vender_producto(self, id_producto: int, cantidad: int) -> bool:
        """Realiza una venta si hay stock suficiente"""
        if id_producto not in self.inventario:
            print(f"Producto ID {id_producto} no encontrado")
            return False
        
        producto = self.inventario[id_producto]
        
        if producto.stock < cantidad:
            print(f"Stock insuficiente de {producto.nombre}")
            return False
        
        # Actualizar stock
        producto.stock -= cantidad
        producto.ultima_actualizacion = datetime.now()
        
        # Registrar venta
        self.ventas.append({
            "id_producto": id_producto,
            "cantidad": cantidad,
            "fecha": datetime.now(),
            "total": producto.precio * cantidad
        })
        
        print(f"Venta realizada: {cantidad} x {producto.nombre}")
        return True
    
    def generar_reporte(self) -> Dict[str, Union[int, float]]:
        """Genera un reporte de ventas"""
        if not self.ventas:
            return {"total_ventas": 0, "monto_total": 0.0}
        
        total_ventas = len(self.ventas)
        monto_total = sum(venta["total"] for venta in self.ventas)
        
        return {
            "total_ventas": total_ventas,
            "monto_total": monto_total,
            "promedio_venta": monto_total / total_ventas
        }

def demo_integrada():
    """Demuestra una integración completa de los conceptos"""
    print("\n=== EJEMPLO INTEGRADO: SISTEMA DE TIENDA ===")
    
    # Crear tienda
    tienda = Tienda()
    
    # Agregar productos (usando dataclass Producto)
    tienda.agregar_producto(Producto(1, "Laptop", 1200.00, 15))
    tienda.agregar_producto(Producto(2, "Teléfono", 599.99, 30))
    tienda.agregar_producto(Producto(3, "Tablet", 349.99, 20))
    
    # Realizar ventas
    tienda.vender_producto(1, 2)  # Vender 2 laptops
    tienda.vender_producto(2, 5)  # Vender 5 teléfonos
    tienda.vender_producto(3, 10) # Vender 10 tablets
    
    # Intentar venta sin stock
    tienda.vender_producto(1, 20)  # Debería fallar
    
    # Generar reporte
    reporte = tienda.generar_reporte()
    print("\nReporte de ventas:")
    print(f" - Total ventas: {reporte['total_ventas']}")
    print(f" - Monto total: ${reporte['monto_total']:,.2f}")
    print(f" - Promedio por venta: ${reporte['promedio_venta']:,.2f}")

# ============ FUNCIÓN PRINCIPAL ============
def main():
    """Función principal que ejecuta todas las demostraciones"""
    print("DEMOSTRACIÓN DE DATOS COMPLEJOS, FUNCIONES Y MÓDULOS")
    print("----------------------------------------------------")
    
    # 1. Demostración de colecciones de datos
    demo_colecciones()
    
    # 2. Demostración de funciones avanzadas
    demo_funciones()
    
    # 3. Demostración de organización en módulos
    demo_modulos()
    
    # 4. Ejemplo integrado
    demo_integrada()

if __name__ == "__main__":
    main()