import numpy as np
from collections import defaultdict

class ListaDecision:
    """Implementación de Listas de Decisión (K-DL y K-TD)"""
    
    def __init__(self, k=1, tipo='dl'):
        """
        Args:
            k (int): Número de atributos en cada regla (1 para 1-DL, 2 para 2-DL, etc.)
            tipo (str): 'dl' para lista de decisión, 'td' para tabla de decisión
        """
        self.k = k
        self.tipo = tipo.lower()
        self.reglas = []  # Almacena las reglas aprendidas
        self.clases = None  # Almacena las clases únicas
        self.atributos = None  # Nombres de atributos (opcional)
        
    def fit(self, X, y, atributos=None):
        """Aprende las reglas a partir de los datos de entrenamiento"""
        self.atributos = atributos if atributos else [f"Attr_{i}" for i in range(X.shape[1])]
        self.clases = np.unique(y)
        n_muestras, n_atributos = X.shape
        
        # Generar todas las posibles combinaciones de k atributos
        from itertools import combinations
        combinaciones = list(combinations(range(n_atributos), self.k))
        
        # Diccionario para contar co-ocurrencias (valor_atributo -> clase -> conteo)
        conteo_reglas = defaultdict(lambda: defaultdict(int))
        
        # 1. Contar frecuencias de co-ocurrencia
        for i in range(n_muestras):
            for comb in combinaciones:
                # Crear clave para la combinación de atributos
                clave = tuple((self.atributos[j], X[i, j]) for j in comb)
                conteo_reglas[clave][y[i]] += 1
        
        # 2. Crear reglas ordenadas por frecuencia
        for clave, conteos_clases in conteo_reglas.items():
            clase_predominante = max(conteos_clases.items(), key=lambda x: x[1])[0]
            soporte = sum(conteos_clases.values())
            confianza = conteos_clases[clase_predominante] / soporte
            
            self.reglas.append({
                'atributos': clave,
                'clase': clase_predominante,
                'soporte': soporte,
                'confianza': confianza
            })
        
        # 3. Ordenar reglas por soporte y confianza (mayor primero)
        self.reglas.sort(key=lambda x: (-x['soporte'], -x['confianza']))
        
        # Para K-TD, organizar como tabla de decisión
        if self.tipo == 'td':
            self._construir_tabla()

    def _construir_tabla(self):
        """Organiza las reglas como tabla de decisión"""
        self.tabla = defaultdict(dict)
        
        for regla in self.reglas:
            clave = regla['atributos']
            self.tabla[clave] = {
                'clase': regla['clase'],
                'soporte': regla['soporte'],
                'confianza': regla['confianza']
            }

    def predict(self, X):
        """Predice la clase para nuevas muestras"""
        predicciones = []
        
        for muestra in X:
            encontrado = False
            # Buscar la primera regla que coincida
            for regla in self.reglas:
                coincide = True
                for attr, valor in regla['atributos']:
                    idx = self.atributos.index(attr)
                    if muestra[idx] != valor:
                        coincide = False
                        break
                
                if coincide:
                    predicciones.append(regla['clase'])
                    encontrado = True
                    break
            
            # Si no coincide con ninguna regla, predecir la clase más frecuente
            if not encontrado:
                predicciones.append(self.clases[0])
        
        return np.array(predicciones)

    def __str__(self):
        """Representación legible del modelo"""
        s = f"Lista de Decisión {self.k}-{self.tipo.upper()} (Reglas: {len(self.reglas)})\n"
        s += "="*50 + "\n"
        
        if self.tipo == 'dl':
            for i, regla in enumerate(self.reglas, 1):
                s += f"Regla {i}:\n"
                for attr, valor in regla['atributos']:
                    s += f"  {attr} = {valor}\n"
                s += f"  → Clase: {regla['clase']} (Soporte: {regla['soporte']}, Conf: {regla['confianza']:.2f})\n\n"
        else:
            s += "Tabla de Decisión:\n"
            for clave, valores in self.tabla.items():
                s += f"{clave} → {valores['clase']} (Sop: {valores['soporte']}, Conf: {valores['confianza']:.2f})\n"
        
        return s

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
    modelo_1dl = ListaDecision(k=1, tipo='dl')
    modelo_1dl.fit(X, y, atributos)
    print(modelo_1dl)
    
    print("\nPredicciones para nuevos casos:")
    X_nuevo = np.array([
        ['Alta', 'Si', 'Joven'],
        ['Baja', 'No', 'Adulto']
    ])
    print(f"Datos: {X_nuevo}")
    print(f"Predicciones: {modelo_1dl.predict(X_nuevo)}")
    
    print("\n=== Ejemplo 2-TD (Tabla de Decisión 2-Atributos) ===")
    modelo_2td = ListaDecision(k=2, tipo='td')
    modelo_2td.fit(X, y, atributos)
    print(modelo_2td)