import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text
from lime.lime_tabular import LimeTabularExplainer
import shap

class SistemaExplicable:
    """Sistema de ML con capacidades explicativas integradas"""
    
    def __init__(self, modelo=None, tipo='arbol'):
        """
        Args:
            modelo: Modelo preentrenado (opcional)
            tipo (str): 'arbol', 'regresion', 'red_neuronal'
        """
        self.modelo = modelo if modelo else DecisionTreeClassifier(max_depth=3)
        self.tipo = tipo
        self.explicador_lime = None
        self.explicador_shap = None
        
    def entrenar(self, X, y, nombres_atributos=None, nombres_clases=None):
        """Entrena el modelo y prepara los explicadores"""
        self.modelo.fit(X, y)
        self.nombres_atributos = nombres_atributos if nombres_atributos else [f"Atributo_{i}" for i in range(X.shape[1])]
        self.nombres_clases = nombres_clases if nombres_clases else [str(cls) for cls in np.unique(y)]
        
        # Preparar LIME (Local Interpretable Model-agnostic Explanations)
        self.explicador_lime = LimeTabularExplainer(
            training_data=X,
            feature_names=self.nombres_atributos,
            class_names=self.nombres_clases,
            mode='classification' if len(np.unique(y)) > 2 else 'regression'
        )
        
        # Preparar SHAP (SHapley Additive exPlanations)
        if self.tipo == 'arbol':
            self.explicador_shap = shap.TreeExplainer(self.modelo)
        else:
            self.explicador_shap = shap.KernelExplainer(self.modelo.predict, X[:100])
    
    def explicar_globalmente(self):
        """Explicación global del modelo"""
        print("\n=== Explicación Global ===")
        
        if self.tipo == 'arbol':
            # Explicación para árboles de decisión
            print("\nEstructura del árbol de decisión:")
            print(export_text(self.modelo, feature_names=self.nombres_atributos))
            
            print("\nImportancia de características:")
            for nombre, importancia in zip(self.nombres_atributos, self.modelo.feature_importances_):
                print(f"{nombre}: {importancia:.4f}")
        
        # Explicación SHAP global
        print("\nImportancia SHAP (valores promedio):")
        shap_values = self.explicador_shap.shap_values(self.explicador_shap.data)
        if isinstance(shap_values, list):  # Para clasificación múltiple
            for i, clase in enumerate(self.nombres_clases):
                print(f"\nClase {clase}:")
                shap_avg = np.abs(shap_values[i]).mean(axis=0)
                for nombre, valor in zip(self.nombres_atributos, shap_avg):
                    print(f"{nombre}: {valor:.4f}")
        else:  # Para regresión o clasificación binaria
            shap_avg = np.abs(shap_values).mean(axis=0)
            for nombre, valor in zip(self.nombres_atributos, shap_avg):
                print(f"{nombre}: {valor:.4f}")
    
    def explicar_instancia(self, instancia, num_features=5):
        """Explicación para una instancia específica"""
        print(f"\n=== Explicación para Instancia: {instancia} ===")
        
        # Explicación LIME (local)
        print("\nExplicación LIME (factores locales):")
        exp_lime = self.explicador_lime.explain_instance(
            instancia, 
            self.modelo.predict_proba, 
            num_features=num_features
        )
        exp_lime.show_in_notebook()
        
        # Explicación SHAP (local)
        print("\nExplicación SHAP (contribución de características):")
        shap_values = self.explicador_shap.shap_values(instancia.reshape(1, -1))
        shap.force_plot(
            self.explicador_shap.expected_value, 
            shap_values[0] if isinstance(shap_values, list) else shap_values,
            instancia,
            feature_names=self.nombres_atributos
        )
    
    def informacion_relevante(self, X, y):
        """Proporciona información estadística relevante sobre los datos"""
        print("\n=== Información Relevante del Dataset ===")
        
        # Estadísticas básicas
        print(f"\nNúmero de muestras: {X.shape[0]}")
        print(f"Número de características: {X.shape[1]}")
        
        # Distribución de clases
        unique, counts = np.unique(y, return_counts=True)
        print("\nDistribución de clases:")
        for cls, cnt in zip(unique, counts):
            print(f"{cls}: {cnt} muestras ({cnt/len(y):.1%})")
        
        # Correlaciones (para características numéricas)
        if np.issubdtype(X.dtype, np.number):
            corr = np.corrcoef(X.T)
            print("\nMatriz de correlación (primeras 5 características):")
            for i in range(min(5, X.shape[1])):
                print(f"{self.nombres_atributos[i]}: {corr[i][:5]}...")

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":
    # 1. Dataset de ejemplo (cáncer de mama)
    from sklearn.datasets import load_breast_cancer
    data = load_breast_cancer()
    X = data.data
    y = data.target
    nombres_atributos = data.feature_names
    nombres_clases = ['maligno', 'benigno']
    
    # 2. Crear y entrenar sistema explicable
    print("Creando sistema explicable...")
    sistema = SistemaExplicable(tipo='arbol')
    sistema.entrenar(X, y, nombres_atributos, nombres_clases)
    
    # 3. Obtener explicaciones
    sistema.explicar_globalmente()
    
    # 4. Explicar instancia específica (ejemplo aleatorio)
    instancia_ejemplo = X[10]  # Seleccionar la 10ª instancia
    sistema.explicar_instancia(instancia_ejemplo)
    
    # 5. Mostrar información relevante del dataset
    sistema.informacion_relevante(X, y)