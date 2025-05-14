import numpy as np  # Importa la biblioteca NumPy para operaciones numéricas
from itertools import product  # Importa product para generar el producto cartesiano de iterables
from collections import defaultdict  # Importa defaultdict para crear diccionarios con valores por defecto

class EspacioVersiones:
    """Implementación del espacio de versiones (candidato-eliminación)"""

    def __init__(self, atributos, valores_posibles):
        """
        Args:
            atributos (list): Nombres de los atributos
            valores_posibles (list): Lista de listas con valores posibles por atributo
        """
        self.atributos = atributos  # Almacena los nombres de los atributos
        self.valores_posibles = valores_posibles  # Almacena los valores posibles para cada atributo
        self.S = None  # Conjunto S (hipótesis más específicas)
        self.G = None  # Conjunto G (hipótesis más generales)

    def inicializar(self, clases):
        """Inicializa S y G con las hipótesis más específicas y generales"""
        # Hipótesis más específica: conjunción de TODOS los valores posibles (inicialmente vacío)
        self.S = [{'atributos': [set() for _ in self.atributos], 'clase': clase} for clase in clases]
        # Para cada clase, inicializa los atributos de la hipótesis S como conjuntos vacíos.

        # Hipótesis más general: conjunción que acepta CUALQUIER valor
        self.G = [{'atributos': [set(valores) for valores in self.valores_posibles], 'clase': clase} for clase in clases]
        # Para cada clase, inicializa los atributos de la hipótesis G con todos los valores posibles para cada atributo.

    def actualizar(self, ejemplo, clase):
        """Actualiza S y G con un nuevo ejemplo"""
        # 1. Actualizar S (generalizar hipótesis mínimamente)
        nuevas_S = []
        for h in self.S:  # Itera sobre cada hipótesis en S
            if h['clase'] == clase:  # Si la hipótesis es de la misma clase que el ejemplo
                # Crear nueva hipótesis generalizada
                nueva_h = {'atributos': [], 'clase': clase}
                for i, (valores_h, val_ejemplo) in enumerate(zip(h['atributos'], ejemplo)):
                    # Itera sobre los atributos de la hipótesis y los valores del ejemplo
                    nuevos_valores = set(valores_h)
                    if not nuevos_valores:  # Si el conjunto de valores del atributo está vacío
                        nuevos_valores.add(val_ejemplo)  # Agrega el valor del ejemplo al conjunto
                    else:
                        if val_ejemplo not in nuevos_valores:
                            # Si el valor del ejemplo no está en el conjunto, lo agrega
                            nuevos_valores.add(val_ejemplo)
                    nueva_h['atributos'].append(nuevos_valores)  # Agrega el conjunto actualizado a la nueva hipótesis
                nuevas_S.append(nueva_h)  # Agrega la nueva hipótesis a la lista de nuevas S
            else:
                # Mantener hipótesis que aún cubran ejemplos previos
                if self._cubre(h, ejemplo):
                    nuevas_S.append(h)  # Mantiene las hipótesis de otras clases que cubren el ejemplo actual

        # 2. Actualizar G (especializar hipótesis mínimamente)
        nuevas_G = []
        for h in self.G:  # Itera sobre las hipótesis en G
            if h['clase'] == clase:
                nuevas_G.append(h)  # Mantiene las hipótesis generales de la misma clase
            else:
                # Generar especializaciones que no cubran el ejemplo negativo
                especializaciones = self._especializar(h, ejemplo)  # Genera hipótesis más específicas que no cubran el ejemplo
                nuevas_G.extend(especializaciones)  # Agrega las especializaciones a la lista

        # 3. Eliminar hipótesis inconsistentes
        self.S = [h for h in nuevas_S if any(self._mas_general(h, g) for g in nuevas_G)]
        # Actualiza S, manteniendo solo las hipótesis que son más generales que alguna en G
        self.G = [h for h in nuevas_G if any(self._mas_general(s, h) for s in self.S)]
        # Actualiza G, manteniendo solo las hipótesis que son más generales que alguna en S

    def _cubre(self, hipotesis, ejemplo):
        """Verifica si una hipótesis cubre un ejemplo"""
        for valores_h, val_ejemplo in zip(hipotesis['atributos'], ejemplo):
            # Itera sobre los atributos de la hipótesis y los valores del ejemplo
            if val_ejemplo not in valores_h:  # Si el valor del ejemplo no está en los valores aceptados por la hipótesis
                return False  # La hipótesis no cubre el ejemplo
        return True  # La hipótesis cubre el ejemplo

    def _especializar(self, hipotesis, ejemplo_negativo):
        """Genera especializaciones de G que no cubran el ejemplo negativo"""
        especializaciones = []
        for i, (valores_h, val_neg) in enumerate(zip(hipotesis['atributos'], ejemplo_negativo)):
            # Itera sobre los atributos de la hipótesis y los valores del ejemplo negativo
            if val_neg in valores_h:  # Si el valor del ejemplo negativo está en los valores aceptados por la hipótesis
                nuevos_valores = set(valores_h) - {val_neg}  # Excluye el valor del ejemplo negativo
                if nuevos_valores:  # Evitar conjuntos vacíos
                    nueva_h = {'atributos': hipotesis['atributos'].copy(), 'clase': hipotesis['clase']}
                    nueva_h['atributos'][i] = nuevos_valores  # Crea una nueva hipótesis con el atributo especializado
                    especializaciones.append(nueva_h)  # Agrega la nueva hipótesis a las especializaciones
        return especializaciones

    def _mas_general(self, h1, h2):
        """Verifica si h1 es más general que h2"""
        for v1, v2 in zip(h1['atributos'], h2['atributos']):
            # Itera sobre los atributos de ambas hipótesis
            if not v1.issuperset(v2):  # Si los valores aceptados por h1 no son un superconjunto de los de h2
                return False  # h1 no es más general que h2
        return True  # h1 es más general que h2

    def __str__(self):
        """Representación legible del espacio de versiones"""
        s = "Espacio de Versiones:\n"
        s += "Conjunto S (más específico):\n"
        for h in self.S:
            s += f"  Clase {h['clase']}: " + " ∧ ".join(
                f"{attr}={val}" if len(val) == 1 else f"{attr}∈{val}"
                for attr, val in zip(self.atributos, h['atributos'])
            ) + "\n"
        s += "Conjunto G (más general):\n"
        for h in self.G:
            s += f"  Clase {h['clase']}: " + " ∧ ".join(
                f"{attr}=*" if len(val) == len(posibles) else f"{attr}∈{val}"
                for attr, val, posibles in zip(self.atributos, h['atributos'], self.valores_posibles)
            ) + "\n"
        return s

class AlgoritmoAQ:
    """Implementación del algoritmo AQ para aprendizaje de reglas"""

    def __init__(self, atributos, valores_posibles):
        """
        Inicializa el algoritmo AQ.

        Args:
            atributos (list): Lista de nombres de atributos.
            valores_posibles (list): Lista de listas, donde cada lista interna contiene los valores posibles para un atributo.
        """
        self.atributos = atributos
        self.valores_posibles = valores_posibles
        self.reglas = []  # Lista para almacenar las reglas aprendidas

    def fit(self, X, y):
        """
        Aprende reglas que cubran ejemplos positivos.

        Args:
            X (np.ndarray): Matriz de características de los ejemplos de entrenamiento.
            y (np.ndarray): Array de etiquetas de clase de los ejemplos de entrenamiento.
        """
        clases = np.unique(y)  # Obtiene las clases únicas presentes en las etiquetas
        clase_positiva = clases[0]  # Asume que la primera clase es la positiva

        # Seleccionar ejemplos positivos
        X_pos = X[y == clase_positiva]  # Filtra los ejemplos que pertenecen a la clase positiva

        while len(X_pos) > 0:
            # 1. Seleccionar un ejemplo positivo no cubierto (semilla)
            semilla = X_pos[0]  # Selecciona el primer ejemplo positivo restante como semilla

            # 2. Encontrar la mejor regla que cubra la semilla
            mejor_regla = self._encontrar_regla(semilla, X, y, clase_positiva)  # Encuentra la mejor regla que cubre la semilla
            self.reglas.append(mejor_regla)  # Agrega la regla aprendida al conjunto de reglas

            # 3. Eliminar ejemplos cubiertos por la nueva regla
            cubiertos = [self._cubre(mejor_regla, x) for x in X_pos]  # Identifica los ejemplos positivos cubiertos por la regla
            X_pos = X_pos[~np.array(cubiertos)]  # Elimina los ejemplos cubiertos de los ejemplos positivos restantes

    def _encontrar_regla(self, semilla, X, y, clase_positiva):
        """
        Encuentra la regla más específica que cubra la semilla y no cubra negativos.

        Args:
            semilla (np.ndarray): El ejemplo positivo que la regla debe cubrir.
            X (np.ndarray): Matriz de características de todos los ejemplos.
            y (np.ndarray): Array de etiquetas de clase.
            clase_positiva (str): La clase considerada como positiva.

        Returns:
            dict: La mejor regla encontrada.
        """
        # Inicializar regla con valores exactos de la semilla
        regla = {'atributos': [{val} for val in semilla], 'clase': clase_positiva}  # Inicializa la regla con los valores de la semilla

        # Generalizar la regla paso a paso
        mejor_regla = regla.copy()  # Inicializa la mejor regla con la regla actual
        mejor_cubiertos = self._contar_cubiertos(regla, X, y)  # Cuenta cuántos ejemplos cubre la regla

        cambiado = True
        while cambiado:
            cambiado = False
            generalizaciones = self._generar_generalizaciones(regla)  # Genera posibles generalizaciones de la regla

            for gen in generalizaciones:  # Itera sobre las generalizaciones
                cubiertos = self._contar_cubiertos(gen, X, y)  # Cuenta cuántos ejemplos cubre la generalización
                if cubiertos['positivos'] > 0 and cubiertos['negativos'] == 0:  # Si cubre positivos y no negativos
                    if cubiertos['positivos'] > mejor_cubiertos['positivos']:  # Si cubre más positivos que la mejor regla
                        mejor_regla = gen.copy()  # Actualiza la mejor regla
                        mejor_cubiertos = cubiertos  # Actualiza el conteo de ejemplos cubiertos
                        cambiado = True  # Indica que se encontró una mejor regla

            regla = mejor_regla  # Actualiza la regla actual con la mejor regla encontrada

        return mejor_regla  # Devuelve la mejor regla encontrada

    def _generar_generalizaciones(self, regla):
        """
        Genera generalizaciones posibles de una regla.

        Args:
            regla (dict): La regla a generalizar.

        Returns:
            list: Una lista de reglas generalizadas.
        """
        generalizaciones = []
        for i in range(len(self.atributos)):
            # Itera sobre los atributos de la regla
            if len(regla['atributos'][i]) < len(self.valores_posibles[i]):
                # Si el atributo no cubre todos los valores posibles
                nueva_regla = {'atributos': [s.copy() for s in regla['atributos']], 'clase': regla['clase']}
                # Crea una copia de la regla
                nueva_regla['atributos'][i].update(self.valores_posibles[i])
                # Generaliza el atributo, agregando todos los valores posibles
                generalizaciones.append(nueva_regla)  # Agrega la regla generalizada a la lista
        return generalizaciones

    def _contar_cubiertos(self, regla, X, y):
        """
        Cuenta ejemplos positivos y negativos cubiertos por una regla.

        Args:
            regla (dict): La regla a evaluar.
            X (np.ndarray): Matriz de características de los ejemplos.
            y (np.ndarray): Array de etiquetas de clase.

        Returns:
            dict: Un diccionario con el conteo de ejemplos positivos y negativos cubiertos.
        """
        positivos = 0
        negativos = 0
        for ejemplo, clase in zip(X, y):
            # Itera sobre los ejemplos y sus clases
            if self._cubre(regla, ejemplo):  # Si la regla cubre el ejemplo
                if clase == regla['clase']:
                    positivos += 1  # Incrementa el conteo de positivos
                else:
                    negativos += 1  # Incrementa el conteo de negativos
        return {'positivos': positivos, 'negativos': negativos}

    def _cubre(self, regla, ejemplo):
        """
        Verifica si una regla cubre un ejemplo.

        Args:
            regla (dict): La regla a evaluar.
            ejemplo (np.ndarray): El ejemplo a verificar.

        Returns:
            bool: True si la regla cubre el ejemplo, False de lo contrario.
        """
        for valores_h, val_ejemplo in zip(regla['atributos'], ejemplo):
            # Itera sobre los atributos de la regla y los valores del ejemplo
            if val_ejemplo not in valores_h:
                # Si el valor del ejemplo no está en los valores permitidos por la regla
                return False  # La regla no cubre el ejemplo
        return True  # La regla cubre el ejemplo

    def predict(self, X):
        """
        Predice la clase para nuevos ejemplos.

        Args:
            X (np.ndarray): Matriz de características de los ejemplos a predecir.

        Returns:
            np.ndarray: Un array con las clases predichas.
        """
        predicciones = []
        for ejemplo in X:
            # Itera sobre los ejemplos a predecir
            pred = None
            for regla in self.reglas:
                # Itera sobre las reglas aprendidas
                if self._cubre(regla, ejemplo):
                    # Si la regla cubre el ejemplo
                    pred = regla['clase']  # Asigna la clase de la regla como predicción
                    break  # Detiene la búsqueda de reglas
            predicciones.append(pred if pred is not None else 'Desconocido')  # Agrega la predicción a la lista
            # Si no se encontró ninguna regla que cubra el ejemplo, la predicción es 'Desconocido'
        return np.array(predicciones)  # Devuelve las predicciones como un array de NumPy

    def __str__(self):
        """Representación legible de las reglas aprendidas"""
        s = "Reglas AQ aprendidas:\n"
        for i, regla in enumerate(self.reglas, 1):
            s += f"Regla {i}: " + " ∧ ".join(
                f"{attr}={val}" if len(val) == 1 else f"{attr}∈{val}"
                for attr, val in zip(self.atributos, regla['atributos'])
            ) + f" → {regla['clase']}\n"
        return s

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":
    # Datos de ejemplo: diagnóstico de enfermedad (Enfermo/Sano)
    # Atributos: Fiebre (Alta, Media, Baja), Tos (Si, No), DolorCabeza (Si, No)
    X = np.array([
        ['Alta', 'Si', 'Si'],
        ['Alta', 'Si', 'No'],
        ['Media', 'No', 'Si'],
        ['Baja', 'No', 'No'],
        ['Alta', 'No', 'Si']
    ])
    y = np.array(['Enfermo', 'Enfermo', 'Sano', 'Sano', 'Enfermo'])
    atributos = ['Fiebre', 'Tos', 'DolorCabeza']
    valores_posibles = [['Alta', 'Media', 'Baja'], ['Si', 'No'], ['Si', 'No']]

    print("=== Algoritmo AQ ===")
    aq = AlgoritmoAQ(atributos, valores_posibles)  # Crea una instancia del algoritmo AQ
    aq.fit(X, y)  # Entrena el algoritmo con los datos de entrenamiento
    print(aq)  # Imprime las reglas aprendidas por el algoritmo

    print("\nPredicciones:")
    X_test = np.array([['Alta', 'Si', 'Si'], ['Baja', 'No', 'Si']])  # Datos de prueba
    print(f"Datos: {X_test}")
    print(f"Predicciones: {aq.predict(X_test)}")  # Predice las clases para los datos de prueba

    print("\n=== Espacio de Versiones ===")
    ev = EspacioVersiones(atributos, valores_posibles)  # Crea una instancia del algoritmo Espacio de Versiones
    ev.inicializar(np.unique(y))  # Inicializa el espacio de versiones con las clases únicas

    print("\nEstado inicial:")
    print(ev)  # Imprime el estado inicial del espacio de versiones

    print("\nActualizando con ejemplos:")
    for ejemplo, clase in zip(X, y):
        # Itera sobre los ejemplos de entrenamiento y sus clases
        ev.actualizar(ejemplo, clase)  # Actualiza el espacio de versiones con cada ejemplo
        print(f"\nDespués de ejemplo: {ejemplo} → {clase}")
        print(ev)  # Imprime el estado del espacio de versiones después de cada actualización
