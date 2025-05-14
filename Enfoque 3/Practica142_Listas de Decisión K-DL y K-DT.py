import numpy as np  # Importa la biblioteca NumPy para operaciones numéricas
from collections import defaultdict  # Importa defaultdict para crear diccionarios con valores por defecto

class ListaDecision:
    """Implementación de Listas de Decisión (K-DL y K-TD)"""

    def __init__(self, k=1, tipo='dl'):
        """
        Args:
            k (int): Número de atributos en cada regla (1 para 1-DL, 2 para 2-DL, etc.)
            tipo (str): 'dl' para lista de decisión, 'td' para tabla de decisión
        """
        self.k = k  # Inicializa el número de atributos por regla
        self.tipo = tipo.lower()  # Convierte el tipo a minúsculas para comparación
        self.reglas = []  # Lista para almacenar las reglas aprendidas
        self.clases = None  # Almacena las clases únicas presentes en los datos
        self.atributos = None  # Almacena los nombres de los atributos (opcional)

    def fit(self, X, y, atributos=None):
        """Aprende las reglas a partir de los datos de entrenamiento"""
        self.atributos = atributos if atributos else [f"Attr_{i}" for i in range(X.shape[1])]
        # Si no se proporcionan nombres de atributos, se generan automáticamente
        self.clases = np.unique(y)  # Obtiene las clases únicas del conjunto de datos
        n_muestras, n_atributos = X.shape  # Obtiene el número de muestras y atributos

        # Generar todas las posibles combinaciones de k atributos
        from itertools import combinations  # Importa la función combinations del módulo itertools
        combinaciones = list(combinations(range(n_atributos), self.k))  # Genera todas las combinaciones posibles de k atributos

        # Diccionario para contar co-ocurrencias (valor_atributo -> clase -> conteo)
        conteo_reglas = defaultdict(lambda: defaultdict(int))
        # Crea un diccionario anidado: la clave externa es una tupla de (atributo, valor),
        # la clave interna es la clase, y el valor es el conteo de ocurrencias.

        # 1. Contar frecuencias de co-ocurrencia
        for i in range(n_muestras):  # Itera sobre cada muestra
            for comb in combinaciones:  # Itera sobre cada combinación de atributos
                # Crear clave para la combinación de atributos
                clave = tuple((self.atributos[j], X[i, j]) for j in comb)
                # Crea una tupla donde cada elemento es un par (nombre_atributo, valor_atributo)
                conteo_reglas[clave][y[i]] += 1  # Incrementa el conteo de la clase para esta combinación de atributos

        # 2. Crear reglas ordenadas por frecuencia
        for clave, conteos_clases in conteo_reglas.items():
            # Itera sobre cada combinación de atributos y sus conteos de clase
            clase_predominante = max(conteos_clases.items(), key=lambda x: x[1])[0]
            # Encuentra la clase con mayor frecuencia para esta combinación de atributos
            soporte = sum(conteos_clases.values())  # Calcula el soporte (frecuencia total de la regla)
            confianza = conteos_clases[clase_predominante] / soporte
            # Calcula la confianza (proporción de la clase predominante entre todas las ocurrencias)

            self.reglas.append({  # Agrega la regla a la lista de reglas
                'atributos': clave,
                'clase': clase_predominante,
                'soporte': soporte,
                'confianza': confianza
            })

        # 3. Ordenar reglas por soporte y confianza (mayor primero)
        self.reglas.sort(key=lambda x: (-x['soporte'], -x['confianza']))
        # Ordena las reglas: primero por soporte descendente, luego por confianza descendente

        # Para K-TD, organizar como tabla de decisión
        if self.tipo == 'td':
            self._construir_tabla()  # Si el tipo es 'td', construye la tabla de decisión

    def _construir_tabla(self):
        """Organiza las reglas como tabla de decisión"""
        self.tabla = defaultdict(dict)  # Inicializa un diccionario para la tabla de decisión

        for regla in self.reglas:  # Itera sobre las reglas aprendidas
            clave = regla['atributos']  # La clave de la tabla es la combinación de atributos
            self.tabla[clave] = {  # Almacena la información de la regla en la tabla
                'clase': regla['clase'],
                'soporte': regla['soporte'],
                'confianza': regla['confianza']
            }

    def predict(self, X):
        """Predice la clase para nuevas muestras"""
        predicciones = []  # Lista para almacenar las predicciones

        for muestra in X:  # Itera sobre cada muestra a predecir
            encontrado = False  # Indica si se encontró una regla coincidente
            # Buscar la primera regla que coincida
            for regla in self.reglas:  # Itera sobre las reglas
                coincide = True  # Asume que la regla coincide inicialmente
                for attr, valor in regla['atributos']:  # Itera sobre los atributos de la regla
                    idx = self.atributos.index(attr)  # Obtiene el índice del atributo
                    if muestra[idx] != valor:  # Compara el valor del atributo de la muestra con el valor de la regla
                        coincide = False  # Si no coinciden, la regla no coincide
                        break  # Sale del bucle interno
                
                if coincide:  # Si la regla coincide
                    predicciones.append(regla['clase'])  # Agrega la clase de la regla a las predicciones
                    encontrado = True  # Marca que se encontró una regla
                    break  # Sale del bucle de reglas
            
            # Si no coincide con ninguna regla, predecir la clase más frecuente
            if not encontrado:
                predicciones.append(self.clases[0])  # Usa la primera clase como predicción por defecto
        
        return np.array(predicciones)  # Devuelve las predicciones como un array de NumPy

    def __str__(self):
        """Representación legible del modelo"""
        s = f"Lista de Decisión {self.k}-{self.tipo.upper()} (Reglas: {len(self.reglas)})\n"
        s += "="*50 + "\n"
        
        if self.tipo == 'dl':  # Si es una lista de decisión
            for i, regla in enumerate(self.reglas, 1):  # Itera sobre las reglas
                s += f"Regla {i}:\n"
                for attr, valor in regla['atributos']:  # Itera sobre los atributos de la regla
                    s += f"  {attr} = {valor}\n"  # Imprime la condición del atributo
                s += f"  → Clase: {regla['clase']} (Soporte: {regla['soporte']}, Conf: {regla['confianza']:.2f})\n\n"
        else:  # Si es una tabla de decisión
            s += "Tabla de Decisión:\n"
            for clave, valores in self.tabla.items():  # Itera sobre las entradas de la tabla
                s += f"{clave} → {valores['clase']} (Sop: {valores['soporte']}, Conf: {valores['confianza']:.2f})\n"
        
        return s  # Devuelve la representación en cadena

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":
    # Datos de ejemplo: diagnóstico médico (simplificado)
    # Atributos: Fiebre (Alta, Media, Baja), Dolor (Si, No), Edad (Joven, Adulto, Mayor)
    X = np.array([
        ['Alta', 'Si', 'Joven'],
        ['Alta', 'No', 'Adulto'],
        ['Media', 'Si', 'Mayor'],
        ['Baja', 'No', 'Joven'],
        ['Alta', 'Si', 'Adulto'],
        ['Media', 'No', 'Mayor'],
        ['Baja', 'Si', 'Joven'],
        ['Alta', 'No', 'Mayor']
    ])
    y = np.array(['Gripe', 'Resfriado', 'Gripe', 'Sano', 'Gripe', 'Sano', 'Resfriado', 'Resfriado'])
    
    atributos = ['Fiebre', 'Dolor', 'Edad']
    
    print("=== Ejemplo 1-DL (Lista de Decisión 1-Atributo) ===")
    modelo_1dl = ListaDecision(k=1, tipo='dl')  # Crea un modelo 1-DL
    modelo_1dl.fit(X, y, atributos)  # Entrena el modelo
    print(modelo_1dl)  # Imprime el modelo

    print("\nPredicciones para nuevos casos:")
    X_nuevo = np.array([
        ['Alta', 'Si', 'Joven'],
        ['Baja', 'No', 'Adulto']
    ])
    print(f"Datos: {X_nuevo}")  # Imprime los datos de prueba
    print(f"Predicciones: {modelo_1dl.predict(X_nuevo)}")  # Imprime las predicciones del modelo

    print("\n=== Ejemplo 2-TD (Tabla de Decisión 2-Atributos) ===")
    modelo_2td = ListaDecision(k=2, tipo='td')  # Crea un modelo 2-TD
    modelo_2td.fit(X, y, atributos)  # Entrena el modelo
    print(modelo_2td)  # Imprime el modelo
