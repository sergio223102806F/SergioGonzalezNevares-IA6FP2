"""
DATOS COMPLEJOS, FUNCIONES Y MÓDULOS -
---------------------------------------------------------------
Este código demuestra:
1. Estructuras de datos complejas (listas, diccionarios, objetos)
2. Funciones (definición, parámetros, retorno)
3. Organización en módulos (importación, namespaces)
"""

# ============ IMPORTACIÓN DE MÓDULOS ============
import json # Importa el módulo json para trabajar con datos JSON (no se usa directamente en el código proporcionado, pero es una importación común para datos complejos)
from typing import List, Dict, Tuple, Optional, Union # Importa tipos para anotaciones de tipo
from dataclasses import dataclass # Importa el decorador dataclass para crear clases de datos
from datetime import datetime # Importa la clase datetime del módulo datetime
import math # Importa el módulo math para funciones matemáticas

# ============ DEFINICIÓN DE ESTRUCTURAS DE DATOS ============
@dataclass
class Producto:
    """Clase que representa un producto en un inventario"""
    id: int # Identificador único del producto
    nombre: str # Nombre del producto
    precio: float # Precio del producto
    stock: int = 0 # Cantidad en stock (valor por defecto: 0)
    ultima_actualizacion: Optional[datetime] = None # Fecha y hora de la última actualización (opcional, valor por defecto: None)

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
    productos: List[Producto] = [ # Define una lista de objetos Producto
        Producto(1, "Laptop", 999.99, 10, datetime.now()),
        Producto(2, "Mouse", 19.99, 50),
        Producto(3, "Teclado", 49.99, 30)
    ]
    
    print("\n1. Lista de productos:")
    for p in productos: # Itera sobre la lista de productos
        print(f" - {p.nombre}: ${p.precio} (Stock: {p.stock})") # Imprime el nombre, precio y stock de cada producto
    
    # 2. DICCIONARIO de empleados (acceso por clave)
    empleados: Dict[str, Dict] = { # Define un diccionario donde las claves son IDs de empleados y los valores son diccionarios con información del empleado
        "A101": {"nombre": "Juan", "puesto": "Desarrollador", "salario": 50000},
        "B202": {"nombre": "María", "puesto": "Diseñadora", "salario": 45000}
    }
    
    print("\n2. Diccionario de empleados:")
    for id_emp, info in empleados.items(): # Itera sobre el diccionario de empleados
        print(f" - {id_emp}: {info['nombre']} ({info['puesto']})") # Imprime el ID, nombre y puesto de cada empleado
    
    # 3. SET de categorías únicas
    categorias = {"Electrónica", "Ropa", "Hogar", "Electrónica"}  # Duplicado eliminado # Define un conjunto de categorías (los duplicados se eliminan automáticamente)
    print("\n3. Set de categorías únicas:")
    print(f" - {categorias}") # Imprime el conjunto de categorías
    
    # 4. TUPLA de coordenadas (inmutable)
    coordenadas: Tuple[float, float] = (40.7128, -74.0060)  # Nueva York # Define una tupla con coordenadas de latitud y longitud
    print("\n4. Tupla de coordenadas:")
    print(f" - Latitud: {coordenadas[0]}, Longitud: {coordenadas[1]}") # Imprime las coordenadas

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
        if not numeros: # Si la lista está vacía
            return 0.0, 0.0, 0.0 # Devuelve ceros para suma, promedio y máximo
        
        suma = sum(numeros) # Calcula la suma de los números
        promedio = suma / len(numeros) # Calcula el promedio
        maximo = max(numeros) # Encuentra el valor máximo
        
        return suma, promedio, maximo # Devuelve los tres valores
    
    datos = [12.5, 18.3, 11.7, 9.8, 15.2]
    total, prom, max_val = calcular_stats(datos) # Llama a la función y asigna los resultados a variables
    
    print("\n1. Retorno múltiple:")
    print(f" - Datos: {datos}")
    print(f" - Total: {total}, Promedio: {prom:.2f}, Máximo: {max_val}") # Imprime los resultados formateados
    
    # 2. Función como parámetro (orden superior)
    def aplicar_funcion(func, valores: List[float]) -> List[float]:
        """Aplica una función a cada elemento de la lista"""
        return [func(x) for x in valores] # Aplica la función a cada elemento y devuelve una nueva lista
    
    def cuadrado(x: float) -> float:
        return x ** 2 # Devuelve el cuadrado de un número
    
    def raiz_cuadrada(x: float) -> float:
        return math.sqrt(x) # Devuelve la raíz cuadrada de un número
    
    print("\n2. Funciones como parámetros:")
    print(f" - Cuadrados: {aplicar_funcion(cuadrado, datos)}") # Aplica la función cuadrado a la lista
    print(f" - Raíces: {aplicar_funcion(raiz_cuadrada, datos)}") # Aplica la función raiz_cuadrada a la lista
    
    # 3. Lambda (función anónima)
    print("\n3. Funciones lambda:")
    cubos = aplicar_funcion(lambda x: x**3, datos) # Usa una función lambda para calcular el cubo de cada número
    print(f" - Cubos: {cubos}") # Imprime los cubos

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
    print(f" - π: {math.pi:.5f}") # Imprime el valor de pi con 5 decimales
    print(f" - cos(π/3): {math.cos(math.pi/3):.3f}") # Imprime el coseno de pi/3 con 3 decimales
    
    # 2. Importación con alias
    import datetime as dt # Importa el módulo datetime con el alias dt
    hoy = dt.date.today() # Obtiene la fecha actual usando el alias
    print("\n2. Uso de módulo datetime con alias:")
    print(f" - Hoy: {hoy.strftime('%d/%m/%Y')}") # Imprime la fecha formateada
    
    # 3. Importación selectiva
    from random import randint, choice # Importa funciones específicas del módulo random
    print("\n3. Importación selectiva de random:")
    print(f" - Número aleatorio: {randint(1, 100)}") # Imprime un entero aleatorio entre 1 y 100
    print(f" - Elección aleatoria: {choice(['rojo', 'verde', 'azul'])}") # Imprime una elección aleatoria de una lista
    
    # 4. Módulos personalizados (ejemplo simulado)
    print("\n4. Módulos personalizados (ejemplo):")
    print("  (Normalmente estarían en archivos separados)")
    
    # Simulamos un módulo de utilidades
    class Utils: # Define una clase Utils para simular un módulo personalizado
        @staticmethod
        def formatear_moneda(monto: float) -> str:
            return f"${monto:,.2f}" # Formatea un monto como moneda con 2 decimales
    
    print(f" - Formato monetario: {Utils.formatear_moneda(1250.75)}") # Usa la función del módulo simulado

# ============ EJEMPLO INTEGRADO ============
class Tienda:
    """Clase que integra datos complejos y funciones para gestionar una tienda"""
    
    def __init__(self):
        self.inventario: Dict[int, Producto] = {} # Diccionario para almacenar productos por ID
        self.ventas: List[Dict] = [] # Lista para almacenar registros de ventas
    
    def agregar_producto(self, producto: Producto) -> None:
        """Agrega un producto al inventario"""
        self.inventario[producto.id] = producto # Agrega el producto al diccionario usando su ID como clave
    
    def vender_producto(self, id_producto: int, cantidad: int) -> bool:
        """Realiza una venta si hay stock suficiente"""
        if id_producto not in self.inventario: # Si el producto no está en el inventario
            print(f"Producto ID {id_producto} no encontrado")
            return False # Devuelve False para indicar que la venta falló
        
        producto = self.inventario[id_producto] # Obtiene el producto del inventario
        
        if producto.stock < cantidad: # Si no hay suficiente stock
            print(f"Stock insuficiente de {producto.nombre}")
            return False # Devuelve False
        
        # Actualizar stock
        producto.stock -= cantidad # Reduce el stock del producto
        producto.ultima_actualizacion = datetime.now() # Actualiza la fecha de última actualización
        
        # Registrar venta
        self.ventas.append({ # Agrega un registro de venta a la lista de ventas
            "id_producto": id_producto,
            "cantidad": cantidad,
            "fecha": datetime.now(),
            "total": producto.precio * cantidad # Calcula el total de la venta
        })
        
        print(f"Venta realizada: {cantidad} x {producto.nombre}") # Imprime un mensaje de éxito
        return True # Devuelve True para indicar que la venta se realizó con éxito
    
    def generar_reporte(self) -> Dict[str, Union[int, float]]:
        """Genera un reporte de ventas"""
        if not self.ventas: # Si no hay ventas
            return {"total_ventas": 0, "monto_total": 0.0} # Devuelve un reporte con ceros
        
        total_ventas = len(self.ventas) # Calcula el número total de ventas
        monto_total = sum(venta["total"] for venta in self.ventas) # Calcula el monto total de las ventas
        
        return { # Devuelve un diccionario con el reporte
            "total_ventas": total_ventas,
            "monto_total": monto_total,
            "promedio_venta": monto_total / total_ventas # Calcula el promedio de venta
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
    main() # Llama a la función principal si el script se ejecuta directamente
