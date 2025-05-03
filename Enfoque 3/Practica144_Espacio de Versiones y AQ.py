import numpy as np
from itertools import product
from collections import defaultdict

class EspacioVersiones:
    """Implementación del espacio de versiones (candidato-eliminación)"""
    
    def __init__(self, atributos, valores_posibles):
        """
        Args:
            atributos (list): Nombres de los atributos
            valores_posibles (list): Lista de listas con valores posibles por atributo
        """
        self.atributos = atributos
        self.valores_posibles = valores_posibles
        self.S = None  # Conjunto S (hipótesis más específicas)
        self.G = None  # Conjunto G (hipótesis más generales)
        
    def inicializar(self, clases):
        """Inicializa S y G con las hipótesis más específicas y generales"""
        # Hipótesis más específica: conjunción de TODOS los valores posibles (inicialmente vacío)
        self.S = [{'atributos': [set() for _ in self.atributos], 'clase': clase} for clase in clases]
        
        # Hipótesis más general: conjunción que acepta CUALQUIER valor
        self.G = [{'atributos': [set(valores) for valores in self.valores_posibles], 'clase': clase} for clase in clases]
    
    def actualizar(self, ejemplo, clase):
        """Actualiza S y G con un nuevo ejemplo"""
        # 1. Actualizar S (generalizar hipótesis mínimamente)
        nuevas_S = []
        for h in self.S:
            if h['clase'] == clase:
                # Crear nueva hipótesis generalizada
                nueva_h = {'atributos': [], 'clase': clase}
                for i, (valores_h, val_ejemplo) in enumerate(zip(h['atributos'], ejemplo)):
                    nuevos_valores = set(valores_h)
                    if not nuevos_valores:  # Si estaba vacío (primera generalización)
                        nuevos_valores.add(val_ejemplo)
                    else:
                        if val_ejemplo not in nuevos_valores:
                            nuevos_valores.add(val_ejemplo)
                    nueva_h['atributos'].append(nuevos_valores)
                nuevas_S.append(nueva_h)
            else:
                # Mantener hipótesis que aún cubran ejemplos previos
                if self._cubre(h, ejemplo):
                    nuevas_S.append(h)
        
        # 2. Actualizar G (especializar hipótesis mínimamente)
        nuevas_G = []
        for h in self.G:
            if h['clase'] == clase:
                nuevas_G.append(h)  # Mantener hipótesis generales de la misma clase
            else:
                # Generar especializaciones que no cubran el ejemplo negativo
                especializaciones = self._especializar(h, ejemplo)
                nuevas_G.extend(especializaciones)
        
        # 3. Eliminar hipótesis inconsistentes
        self.S = [h for h in nuevas_S if any(self._mas_general(h, g) for g in nuevas_G)]
        self.G = [h for h in nuevas_G if any(self._mas_general(s, h) for s in self.S)]
    
    def _cubre(self, hipotesis, ejemplo):
        """Verifica si una hipótesis cubre un ejemplo"""
        for valores_h, val_ejemplo in zip(hipotesis['atributos'], ejemplo):
            if val_ejemplo not in valores_h:
                return False
        return True
    
    def _especializar(self, hipotesis, ejemplo_negativo):
        """Genera especializaciones de G que no cubran el ejemplo negativo"""
        especializaciones = []
        
        for i, (valores_h, val_neg) in enumerate(zip(hipotesis['atributos'], ejemplo_negativo)):
            if val_neg in valores_h:
                nuevos_valores = set(valores_h) - {val_neg}
                if nuevos_valores:  # Evitar conjuntos vacíos
                    nueva_h = {'atributos': hipotesis['atributos'].copy(), 'clase': hipotesis['clase']}
                    nueva_h['atributos'][i] = nuevos_valores
                    especializaciones.append(nueva_h)
        
        return especializaciones
    
    def _mas_general(self, h1, h2):
        """Verifica si h1 es más general que h2"""
        for v1, v2 in zip(h1['atributos'], h2['atributos']):
            if not v1.issuperset(v2):
                return False
        return True
    
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
        self.atributos = atributos
        self.valores_posibles = valores_posibles
        self.reglas = []
        
    def fit(self, X, y):
        """Aprende reglas que cubran ejemplos positivos"""
        clases = np.unique(y)
        clase_positiva = clases[0]  # Asumimos que la primera clase es la positiva
        
        # Seleccionar ejemplos positivos
        X_pos = X[y == clase_positiva]
        
        while len(X_pos) > 0:
            # 1. Seleccionar un ejemplo positivo no cubierto (semilla)
            semilla = X_pos[0]
            
            # 2. Encontrar la mejor regla que cubra la semilla
            mejor_regla = self._encontrar_regla(semilla, X, y, clase_positiva)
            self.reglas.append(mejor_regla)
            
            # 3. Eliminar ejemplos cubiertos por la nueva regla
            cubiertos = [self._cubre(mejor_regla, x) for x in X_pos]
            X_pos = X_pos[~np.array(cubiertos)]
    
    def _encontrar_regla(self, semilla, X, y, clase_positiva):
        """Encuentra la regla más específica que cubra la semilla y no cubra negativos"""
        # Inicializar regla con valores exactos de la semilla
        regla = {'atributos': [{val} for val in semilla], 'clase': clase_positiva}
        
        # Generalizar la regla paso a paso
        mejor_regla = regla.copy()
        mejor_cubiertos = self._contar_cubiertos(regla, X, y)
        
        cambiado = True
        while cambiado:
            cambiado = False
            generalizaciones = self._generar_generalizaciones(regla)
            
            for gen in generalizaciones:
                cubiertos = self._contar_cubiertos(gen, X, y)
                if cubiertos['positivos'] > 0 and cubiertos['negativos'] == 0:
                    if cubiertos['positivos'] > mejor_cubiertos['positivos']:
                        mejor_regla = gen.copy()
                        mejor_cubiertos = cubiertos
                        cambiado = True
            
            regla = mejor_regla
        
        return mejor_regla
    
    def _generar_generalizaciones(self, regla):
        """Genera generalizaciones posibles de una regla"""
        generalizaciones = []
        
        for i in range(len(self.atributos)):
            if len(regla['atributos'][i]) < len(self.valores_posibles[i]):
                nueva_regla = {'atributos': [s.copy() for s in regla['atributos']], 'clase': regla['clase']}
                nueva_regla['atributos'][i].update(self.valores_posibles[i])
                generalizaciones.append(nueva_regla)
        
        return generalizaciones
    
    def _contar_cubiertos(self, regla, X, y):
        """Cuenta ejemplos positivos y negativos cubiertos por una regla"""
        positivos = 0
        negativos = 0
        
        for ejemplo, clase in zip(X, y):
            if self._cubre(regla, ejemplo):
                if clase == regla['clase']:
                    positivos += 1
                else:
                    negativos += 1
        
        return {'positivos': positivos, 'negativos': negativos}
    
    def _cubre(self, regla, ejemplo):
        """Verifica si una regla cubre un ejemplo"""
        for valores_h, val_ejemplo in zip(regla['atributos'], ejemplo):
            if val_ejemplo not in valores_h:
                return False
        return True
    
    def predict(self, X):
        """Predice la clase para nuevos ejemplos"""
        predicciones = []
        for ejemplo in X:
            pred = None
            for regla in self.reglas:
                if self._cubre(regla, ejemplo):
                    pred = regla['clase']
                    break
            predicciones.append(pred if pred is not None else 'Desconocido')
        return np.array(predicciones)
    
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
    aq = AlgoritmoAQ(atributos, valores_posibles)
    aq.fit(X, y)
    print(aq)
    
    print("\nPredicciones:")
    X_test = np.array([['Alta', 'Si', 'Si'], ['Baja', 'No', 'Si']])
    print(f"Datos: {X_test}")
    print(f"Predicciones: {aq.predict(X_test)}")
    
    print("\n=== Espacio de Versiones ===")
    ev = EspacioVersiones(atributos, valores_posibles)
    ev.inicializar(np.unique(y))
    
    print("\nEstado inicial:")
    print(ev)
    
    print("\nActualizando con ejemplos:")
    for ejemplo, clase in zip(X, y):
        ev.actualizar(ejemplo, clase)
        print(f"\nDespués de ejemplo: {ejemplo} → {clase}")
        print(ev)