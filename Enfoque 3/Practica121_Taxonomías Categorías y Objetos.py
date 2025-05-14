# Importación del módulo typing para anotaciones de tipo
from typing import Dict, List  # Dict para diccionarios, List para listas

class Taxonomia:
    """
    Clase principal que representa una estructura taxonómica jerárquica.
    Permite organizar categorías y objetos en una relación padre-hijo.
    """

    def __init__(self):
        """
        Constructor de la clase Taxonomia.
        Inicializa las estructuras de datos para almacenar la jerarquía.
        """
        # Diccionario donde las claves son categorías y los valores son listas de subcategorías
        self.categorias: Dict[str, List[str]] = {}
        # Diccionario donde las claves son objetos y los valores son sus categorías padre
        self.objetos: Dict[str, str] = {}
        # Nombre de la categoría raíz de la taxonomía
        self.raiz = "Todo"
        # Inicializa la categoría raíz con una lista vacía de subcategorías
        self.categorias[self.raiz] = []

    def agregar_categoria(self, categoria: str, padre: str = None) -> bool:
        """
        Añade una nueva categoría a la taxonomía bajo una categoría padre.

        Parámetros:
            categoria (str): Nombre de la nueva categoría a agregar
            padre (str, opcional): Categoría padre. Si es None, se usa la raíz.

        Retorna:
            bool: True si se agregó correctamente, False si ya existía o el padre no existe
        """
        # Si no se especifica padre, usar la categoría raíz
        if padre is None:
            padre = self.raiz
        # Verificar si la categoría ya existe
        if categoria in self.categorias:
            return False
        # Verificar si la categoría padre existe
        if padre not in self.categorias:
            return False
        # Agregar la nueva categoría como hija del padre especificado
        self.categorias[padre].append(categoria)
        # Inicializar la nueva categoría con lista vacía de subcategorías
        self.categorias[categoria] = []
        return True

    def agregar_objeto(self, objeto: str, categoria: str) -> bool:
        """
        Asigna un objeto a una categoría específica en la taxonomía.

        Parámetros:
            objeto (str): Nombre del objeto a clasificar
            categoria (str): Categoría destino para el objeto

        Retorna:
            bool: True si se agregó correctamente, False si la categoría no existe o el objeto ya estaba
        """
        # Verificar si la categoría existe
        if categoria not in self.categorias:
            return False
        # Verificar si el objeto ya está clasificado
        if objeto in self.objetos:
            return False
        # Asignar el objeto a la categoría especificada
        self.objetos[objeto] = categoria
        return True

    def obtener_categorias_hijas(self, categoria: str = None) -> List[str]:
        """
        Obtiene las subcategorías directas de una categoría especificada.

        Parámetros:
            categoria (str, opcional): Categoría padre. Si es None, usa la raíz.

        Retorna:
            List[str]: Lista de subcategorías directas
        """
        # Si no se especifica categoría, usar la raíz
        if categoria is None:
            categoria = self.raiz
        # Devolver las subcategorías o lista vacía si no existen
        return self.categorias.get(categoria, [])

    def obtener_objetos_en_categoria(self, categoria: str) -> List[str]:
        """
        Recupera todos los objetos clasificados directamente en una categoría.

        Parámetros:
            categoria (str): Categoría a consultar

        Retorna:
            List[str]: Lista de nombres de objetos en la categoría
        """
        # Lista por comprensión que filtra los objetos de la categoría especificada
        return [obj for obj, cat in self.objetos.items() if cat == categoria]

    def obtener_ruta_categoria(self, categoria: str) -> List[str]:
        """
        Construye la ruta jerárquica desde la raíz hasta la categoría especificada.

        Parámetros:
            categoria (str): Categoría destino

        Retorna:
            List[str]: Lista ordenada desde la raíz hasta la categoría
        """
        # Si la categoría no existe, retornar lista vacía
        if categoria not in self.categorias:
            return []
        # Inicializar la ruta con la categoría destino
        ruta = [categoria]
        actual = categoria
        # Recorrer hacia arriba hasta llegar a la raíz
        while actual != self.raiz:
            # Buscar en todas las categorías
            for padre, hijos in self.categorias.items():
                if actual in hijos:  # Si encontramos el padre
                    ruta.insert(0, padre)  # Insertar al inicio de la ruta
                    actual = padre  # Continuar con el padre
                    break
            else:
                return []  # Si no encontramos padre, taxonomía inconsistente
        return ruta

    def visualizar_taxonomia(self, categoria: str = None, nivel: int = 0):
        """
        Muestra la taxonomía completa de forma recursiva con formato jerárquico.

        Parámetros:
            categoria (str, opcional): Nodo desde donde empezar. None para raíz.
            nivel (int, opcional): Nivel de indentación (usado en recursión)
        """
        # Si no se especifica categoría, comenzar desde la raíz
        if categoria is None:
            categoria = self.raiz
        # Imprimir la categoría actual con indentación según nivel
        print("  " * nivel + f"- {categoria}")
        # Obtener y mostrar todos los objetos en esta categoría
        objetos = self.obtener_objetos_en_categoria(categoria)
        for obj in objetos:
            print("  " * (nivel + 1) + f"• {obj}")
        # Llamada recursiva para cada subcategoría
        for subcat in self.categorias[categoria]:
            self.visualizar_taxonomia(subcat, nivel + 1)

def ejemplo_uso():
    """
    Función demostrativa que muestra cómo usar la clase Taxonomia.
    Crea una taxonomía de ejemplo y realiza operaciones básicas.
    """
    # 1. Crear instancia de Taxonomia
    taxonomia = Taxonomia()
    # 2. Construir jerarquía de categorías
    taxonomia.agregar_categoria("Animal")
    taxonomia.agregar_categoria("Vertebrado", "Animal")
    taxonomia.agregar_categoria("Invertebrado", "Animal")
    taxonomia.agregar_categoria("Mamífero", "Vertebrado")
    taxonomia.agregar_categoria("Ave", "Vertebrado")
    taxonomia.agregar_categoria("Reptil", "Vertebrado")
    taxonomia.agregar_categoria("Artrópodo", "Invertebrado")
    # 3. Clasificar objetos en las categorías
    taxonomia.agregar_objeto("Perro", "Mamífero")
    taxonomia.agregar_objeto("Gato", "Mamífero")
    taxonomia.agregar_objeto("Águila", "Ave")
    taxonomia.agregar_objeto("Serpiente", "Reptil")
    taxonomia.agregar_objeto("Araña", "Artrópodo")
    taxonomia.agregar_objeto("Mariposa", "Artrópodo")
    # 4. Mostrar la taxonomía completa
    print("\nTaxonomía completa:")
    taxonomia.visualizar_taxonomia()
    # 5. Ejemplos de consultas
    print("\nSubcategorías de Vertebrado:", taxonomia.obtener_categorias_hijas("Vertebrado"))
    print("Objetos en Artrópodo:", taxonomia.obtener_objetos_en_categoria("Artrópodo"))
    print("Ruta de Reptil:", taxonomia.obtener_ruta_categoria("Reptil"))

# Punto de entrada principal
if __name__ == "__main__":
    ejemplo_uso()

