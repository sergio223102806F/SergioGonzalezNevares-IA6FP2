import numpy as np  # Importa la biblioteca NumPy para operaciones numéricas
from sklearn.tree import DecisionTreeClassifier, export_text  # Importa DecisionTreeClassifier para el modelo y export_text para visualizar el árbol
from lime.lime_tabular import LimeTabularExplainer  # Importa LimeTabularExplainer para explicaciones LIME
import shap  # Importa la biblioteca SHAP para explicaciones SHAP

class SistemaExplicable:
    """Sistema de ML con capacidades explicativas integradas"""

    def __init__(self, modelo=None, tipo='arbol'):
        """
        Args:
            modelo: Modelo preentrenado (opcional)
            tipo (str): 'arbol', 'regresion', 'red_neuronal'
        """
        self.modelo = modelo if modelo else DecisionTreeClassifier(max_depth=3)  # Usa el modelo proporcionado o un árbol de decisión por defecto
        self.tipo = tipo  # Inicializa el tipo de modelo
        self.explicador_lime = None  # Inicializa el explicador LIME
        self.explicador_shap = None  # Inicializa el explicador SHAP

    def entrenar(self, X, y, nombres_atributos=None, nombres_clases=None):
        """Entrena el modelo y prepara los explicadores"""
        self.modelo.fit(X, y)  # Entrena el modelo con los datos de entrenamiento
        self.nombres_atributos = nombres_atributos if nombres_atributos else [f"Atributo_{i}" for i in range(X.shape[1])]
        # Usa los nombres de atributos proporcionados o genera nombres genéricos
        self.nombres_clases = nombres_clases if nombres_clases else [str(cls) for cls in np.unique(y)]
        # Usa los nombres de clases proporcionados o convierte las clases únicas a cadenas

        # Preparar LIME (Local Interpretable Model-agnostic Explanations)
        self.explicador_lime = LimeTabularExplainer(
            training_data=X,  # Datos de entrenamiento para LIME
            feature_names=self.nombres_atributos,  # Nombres de los atributos
            class_names=self.nombres_clases,  # Nombres de las clases
            mode='classification' if len(np.unique(y)) > 2 else 'regression'  # Modo: clasificación o regresión
        )

        # Preparar SHAP (SHapley Additive exPlanations)
        if self.tipo == 'arbol':
            self.explicador_shap = shap.TreeExplainer(self.modelo)  # Explicador SHAP para árboles
        else:
            self.explicador_shap = shap.KernelExplainer(self.modelo.predict, X[:100])  # Explicador SHAP para otros modelos (aproximación)

    def explicar_globalmente(self):
        """Explicación global del modelo"""
        print("\n=== Explicación Global ===")

        if self.tipo == 'arbol':
            # Explicación para árboles de decisión
            print("\nEstructura del árbol de decisión:")
            print(export_text(self.modelo, feature_names=self.nombres_atributos))  # Imprime la estructura del árbol

            print("\nImportancia de características:")
            for nombre, importancia in zip(self.nombres_atributos, self.modelo.feature_importances_):
                print(f"{nombre}: {importancia:.4f}")  # Imprime la importancia de cada característica

        # Explicación SHAP global
        print("\nImportancia SHAP (valores promedio):")
        shap_values = self.explicador_shap.shap_values(self.explicador_shap.data)  # Calcula los valores SHAP
        if isinstance(shap_values, list):  # Para clasificación múltiple
            for i, clase in enumerate(self.nombres_clases):
                print(f"\nClase {clase}:")
                shap_avg = np.abs(shap_values[i]).mean(axis=0)  # Promedio de los valores absolutos de SHAP por característica
                for nombre, valor in zip(self.nombres_atributos, shap_avg):
                    print(f"{nombre}: {valor:.4f}")  # Imprime la importancia SHAP promedio para cada clase
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
            instancia,  # Instancia a explicar
            self.modelo.predict_proba,  # Función para obtener probabilidades de clase
            num_features=num_features  # Número de características a mostrar en la explicación
        )
        exp_lime.show_in_notebook()  # Muestra la explicación LIME en el notebook (si se usa en un notebook)

        # Explicación SHAP (local)
        print("\nExplicación SHAP (contribución de características):")
        shap_values = self.explicador_shap.shap_values(instancia.reshape(1, -1))  # Calcula los valores SHAP para la instancia
        shap.force_plot(  # Crea un gráfico de fuerza para visualizar la explicación SHAP
            self.explicador_shap.expected_value,  # Valor esperado de la salida del modelo
            shap_values[0] if isinstance(shap_values, list) else shap_values,  # Valores SHAP para la instancia
            instancia,  # La instancia a explicar
            feature_names=self.nombres_atributos  # Nombres de las características
        )

    def informacion_relevante(self, X, y):
        """Proporciona información estadística relevante sobre los datos"""
        print("\n=== Información Relevante del Dataset ===")

        # Estadísticas básicas
        print(f"\nNúmero de muestras: {X.shape[0]}")  # Imprime el número de muestras
        print(f"Número de características: {X.shape[1]}")  # Imprime el número de características

        # Distribución de clases
        unique, counts = np.unique(y, return_counts=True)  # Obtiene las clases únicas y sus conteos
        print("\nDistribución de clases:")
        for cls, cnt in zip(unique, counts):
            print(f"{cls}: {cnt} muestras ({cnt/len(y):.1%})")  # Imprime la distribución de cada clase

        # Correlaciones (para características numéricas)
        if np.issubdtype(X.dtype, np.number):  # Verifica si las características son numéricas
            corr = np.corrcoef(X.T)  # Calcula la matriz de correlación
            print("\nMatriz de correlación (primeras 5 características):")
            for i in range(min(5, X.shape[1])):
                print(f"{self.nombres_atributos[i]}: {corr[i][:5]}...")  # Imprime las correlaciones de las primeras 5 características

# ==================== Ejemplo de Uso ====================
if __name__ == "__main__":
    # 1. Dataset de ejemplo (cáncer de mama)
    from sklearn.datasets import load_breast_cancer  # Importa la función para cargar el dataset de cáncer de mama
    data = load_breast_cancer()  # Carga el dataset
    X = data.data  # Obtiene los datos de las características
    y = data.target  # Obtiene las etiquetas de las clases
    nombres_atributos = data.feature_names  # Obtiene los nombres de los atributos
    nombres_clases = ['maligno', 'benigno']  # Define los nombres de las clases

    # 2. Crear y entrenar sistema explicable
    print("Creando sistema explicable...")
    sistema = SistemaExplicable(tipo='arbol')  # Crea una instancia del sistema explicable con un árbol de decisión
    sistema.entrenar(X, y, nombres_atributos, nombres_clases)  # Entrena el sistema con los datos

    # 3. Obtener explicaciones
    sistema.explicar_globalmente()  # Obtiene y muestra explicaciones globales del modelo

    # 4. Explicar instancia específica (ejemplo aleatorio)
    instancia_ejemplo = X[10]  # Selecciona la 10ª instancia como ejemplo
    sistema.explicar_instancia(instancia_ejemplo)  # Obtiene y muestra la explicación para la instancia

    # 5. Mostrar información relevante del dataset
    sistema.informacion_relevante(X, y)  # Muestra información estadística sobre el dataset
