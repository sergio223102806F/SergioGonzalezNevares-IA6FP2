# -*- coding: utf-8 -*-


# Importaciones necesarias
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import math
import random

class TipoVariable(Enum):
    """Tipos de variables en el modelo probabilista"""
    ALEATORIA = auto()     # Variable aleatoria observable
    LATENTE = auto()       # Variable no observable directamente
    DECISION = auto()      # Variable de decisión del agente
    UTILIDAD = auto()      # Variable de utilidad/recompensa

class TipoInferencia(Enum):
    """Métodos de inferencia probabilística"""
    ENUMERACION = auto()   # Inferencia por enumeración
    MUESTREO = auto()      # Inferencia por muestreo
    MCMC = auto()          # Cadenas de Markov Monte Carlo

@dataclass
class Variable:
    """Estructura para representar variables en el modelo"""
    nombre: str                   # Nombre de la variable
    tipo: TipoVariable            # Tipo de variable
    dominio: List[str]            # Valores posibles
    padres: List[str]             # Variables padre en la red
    distribucion: Dict[Tuple, List[float]]  # Distribución condicional

@dataclass
class Observacion:
    """Registro de una observación/evidencia"""
    variable: str                 # Nombre de la variable
    valor: str                    # Valor observado
    certeza: float = 1.0          # Grado de certeza [0, 1]

class ModeloProbabilista:
    """
    Implementación de un modelo probabilista racional que incluye:
    - Red bayesiana para relaciones de dependencia
    - Toma de decisiones racionales
    - Múltiples métodos de inferencia
    """
    
    def __init__(self, nombre: str):
        """
        Inicializa el modelo probabilista
        
        Args:
            nombre (str): Nombre identificador del modelo
        """
        self.nombre = nombre
        self.variables: Dict[str, Variable] = {}      # Diccionario de variables
        self.observaciones: Dict[str, Observacion] = {}  # Evidencia observada
        self.utilidades: Dict[Tuple, float] = {}     # Función de utilidad
        self.historial: List[str] = []               # Historial de operaciones
    
    def agregar_variable(self, var: Variable) -> bool:
        """
        Añade una nueva variable al modelo
        
        Args:
            var (Variable): Variable a añadir
            
        Returns:
            bool: True si se añadió correctamente
        """
        # Validar que los padres existan
        for padre in var.padres:
            if padre not in self.variables:
                return False
                
        self.variables[var.nombre] = var
        self.historial.append(f"Añadida variable {var.nombre}")
        return True
    
    def agregar_observacion(self, obs: Observacion) -> bool:
        """
        Registra una nueva observación/evidencia
        
        Args:
            obs (Observacion): Observación a registrar
            
        Returns:
            bool: True si la variable existe y se registró
        """
        if obs.variable not in self.variables:
            return False
            
        self.observaciones[obs.variable] = obs
        self.historial.append(f"Registrada observación {obs.variable}={obs.valor}")
        return True
    
    def definir_utilidad(self, variables: List[str], valores: Dict[Tuple, float]) -> bool:
        """
        Define la función de utilidad para un conjunto de variables
        
        Args:
            variables (List[str]): Variables que afectan la utilidad
            valores (Dict[Tuple, float]): Valores de utilidad para cada combinación
            
        Returns:
            bool: True si todas las variables existen
        """
        for var in variables:
            if var not in self.variables:
                return False
                
        self.utilidades[(tuple(variables))] = valores
        self.historial.append(f"Definida utilidad para {variables}")
        return True
    
    def inferencia(self, objetivo: str, metodo: TipoInferencia = TipoInferencia.ENUMERACION, 
                  n_muestras: int = 1000) -> Dict[str, float]:
        """
        Realiza inferencia probabilística sobre una variable objetivo
        
        Args:
            objetivo (str): Variable objetivo a inferir
            metodo (TipoInferencia): Método de inferencia a usar
            n_muestras (int): Número de muestras para métodos de muestreo
            
        Returns:
            Dict[str, float]: Distribución de probabilidad resultante
        """
        if objetivo not in self.variables:
            return {}
            
        if metodo == TipoInferencia.ENUMERACION:
            return self._inferencia_enum(objetivo)
        elif metodo == TipoInferencia.MUESTREO:
            return self._muestreo_directo(objetivo, n_muestras)
        else:
            return self._mcmc(objetivo, n_muestras)
    
    def _inferencia_enum(self, objetivo: str) -> Dict[str, float]:
        """
        Inferencia por enumeración exacta (método exacto pero costoso)
        
        Args:
            objetivo (str): Variable objetivo
            
        Returns:
            Dict[str, float]: Distribución de probabilidad
        """
        var = self.variables[objetivo]
        prob = {valor: 0.0 for valor in var.dominio}
        total = 0.0
        
        # Generar todas las posibles combinaciones de variables
        vars_ocultas = [v for v in self.variables if v not in self.observaciones and v != objetivo]
        
        from itertools import product
        # Producto cartesiano de todos los valores posibles
        for valores_ocultas in product(*[self.variables[v].dominio for v in vars_ocultas]):
            # Crear asignación completa
            asignacion = {}
            for i, v in enumerate(vars_ocultas):
                asignacion[v] = valores_ocultas[i]
            for v, obs in self.observaciones.items():
                asignacion[v] = obs.valor
                
            # Calcular probabilidad conjunta
            p_conjunta = self._probabilidad_conjunta(asignacion)
            
            # Acumular para cada valor del objetivo
            for valor in var.dominio:
                asignacion[objetivo] = valor
                p_cond = self._probabilidad_conjunta(asignacion) / p_conjunta if p_conjunta > 0 else 0
                prob[valor] += p_cond
                total += p_cond
        
        # Normalizar
        if total > 0:
            for valor in prob:
                prob[valor] /= total
                
        return prob
    
    def _muestreo_directo(self, objetivo: str, n_muestras: int) -> Dict[str, float]:
        """
        Inferencia por muestreo directo (aproximado)
        
        Args:
            objetivo (str): Variable objetivo
            n_muestras (int): Número de muestras a generar
            
        Returns:
            Dict[str, float]: Distribución de probabilidad aproximada
        """
        conteo = {valor: 0 for valor in self.variables[objetivo].dominio}
        
        for _ in range(n_muestras):
            muestra = self._generar_muestra()
            valor_objetivo = muestra[objetivo]
            conteo[valor_objetivo] += 1
        
        # Convertir a probabilidades
        return {v: c/n_muestras for v, c in conteo.items()}
    
    def _mcmc(self, objetivo: str, n_muestras: int) -> Dict[str, float]:
        """
        Inferencia por MCMC (Gibbs sampling)
        
        Args:
            objetivo (str): Variable objetivo
            n_muestras (int): Número de muestras a generar
            
        Returns:
            Dict[str, float]: Distribución de probabilidad aproximada
        """
        # Inicializar asignación aleatoria
        asignacion = {}
        vars_ocultas = [v for v in self.variables if v not in self.observaciones]
        
        for v in vars_ocultas:
            asignacion[v] = random.choice(self.variables[v].dominio)
        for v, obs in self.observaciones.items():
            asignacion[v] = obs.valor
        
        conteo = {valor: 0 for valor in self.variables[objetivo].dominio}
        
        for _ in range(n_muestras):
            # Muestrear cada variable oculta
            for v in vars_ocultas:
                if v == objetivo:  # Muestrear objetivo al final
                    continue
                    
                # Calcular distribución condicional
                dist = self._distribucion_condicional(v, asignacion)
                nuevo_valor = random.choices(list(dist.keys()), weights=list(dist.values()))[0]
                asignacion[v] = nuevo_valor
            
            # Muestrear variable objetivo
            dist = self._distribucion_condicional(objetivo, asignacion)
            valor_objetivo = random.choices(list(dist.keys()), weights=list(dist.values()))[0]
            asignacion[objetivo] = valor_objetivo
            conteo[valor_objetivo] += 1
        
        return {v: c/n_muestras for v, c in conteo.items()}
    
    def _generar_muestra(self) -> Dict[str, str]:
        """
        Genera una muestra aleatoria según la distribución conjunta
        
        Returns:
            Dict[str, str]: Asignación de valores para todas las variables
        """
        muestra = {}
        # Orden topológico (padres antes que hijos)
        orden = self._orden_topologico()
        
        for var in orden:
            if var in self.observaciones:
                muestra[var] = self.observaciones[var].valor
            else:
                padres_vals = tuple(muestra[p] for p in self.variables[var].padres)
                dist = self.variables[var].distribucion[padres_vals]
                muestra[var] = random.choices(self.variables[var].dominio, weights=dist)[0]
        
        return muestra
    
    def _orden_topologico(self) -> List[str]:
        """
        Orden topológico de variables (padres antes que hijos)
        
        Returns:
            List[str]: Orden de variables
        """
        visitadas = set()
        orden = []
        
        def visitar(nodo):
            if nodo not in visitadas:
                visitadas.add(nodo)
                for padre in self.variables[nodo].padres:
                    visitar(padre)
                orden.append(nodo)
        
        for var in self.variables:
            visitar(var)
            
        return orden
    
    def _probabilidad_conjunta(self, asignacion: Dict[str, str]) -> float:
        """
        Calcula la probabilidad conjunta de una asignación completa
        
        Args:
            asignacion (Dict[str, str]): Asignación de valores a variables
            
        Returns:
            float: Probabilidad conjunta
        """
        p = 1.0
        for var, valor in asignacion.items():
            if var not in self.variables:
                return 0.0
                
            padres_vals = tuple(asignacion[p] for p in self.variables[var].padres)
            dist = self.variables[var].distribucion.get(padres_vals, [0]*len(self.variables[var].dominio))
            
            try:
                idx = self.variables[var].dominio.index(valor)
                p *= dist[idx]
            except ValueError:
                return 0.0
                
        return p
    
    def _distribucion_condicional(self, var: str, asignacion: Dict[str, str]) -> Dict[str, float]:
        """
        Calcula la distribución condicional de una variable dada una asignación parcial
        
        Args:
            var (str): Variable objetivo
            asignacion (Dict[str, str]): Asignación parcial
            
        Returns:
            Dict[str, float]: Distribución condicional
        """
        if var not in self.variables:
            return {}
            
        # Obtener valores de los padres
        padres_vals = tuple(asignacion[p] for p in self.variables[var].padres)
        
        # Obtener distribución condicional
        dist = self.variables[var].distribucion.get(padres_vals, [0]*len(self.variables[var].dominio))
        
        return {v: p for v, p in zip(self.variables[var].dominio, dist)}
    
    def decision_racional(self, variables_decision: List[str]) -> Dict[str, str]:
        """
        Toma una decisión racional maximizando la utilidad esperada
        
        Args:
            variables_decision (List[str]): Variables sobre las que decidir
            
        Returns:
            Dict[str, str]: Mejor asignación encontrada
        """
        mejor_asignacion = {}
        mejor_utilidad = -float('inf')
        
        # Generar todas las posibles combinaciones de decisiones
        from itertools import product
        decisiones_posibles = product(*[self.variables[v].dominio for v in variables_decision])
        
        for decision in decisiones_posibles:
            asignacion = {}
            for i, v in enumerate(variables_decision):
                asignacion[v] = decision[i]
            
            # Fijar la decisión como observación
            obs_previas = self.observaciones.copy()
            for v, val in asignacion.items():
                self.agregar_observacion(Observacion(v, val, 1.0))
            
            # Calcular utilidad esperada
            utilidad = self._utilidad_esperada(asignacion)
            
            # Restaurar observaciones
            self.observaciones = obs_previas
            
            # Actualizar mejor decisión
            if utilidad > mejor_utilidad:
                mejor_utilidad = utilidad
                mejor_asignacion = asignacion.copy()
        
        return mejor_asignacion
    
    def _utilidad_esperada(self, decision: Dict[str, str]) -> float:
        """
        Calcula la utilidad esperada dada una decisión
        
        Args:
            decision (Dict[str, str]): Asignación de variables de decisión
            
        Returns:
            float: Utilidad esperada
        """
        utilidad_total = 0.0
        
        # Para cada combinación de variables de utilidad
        for vars_util, valores_util in self.utilidades.items():
            # Variables no fijadas por la decisión
            vars_inferir = [v for v in vars_util if v not in decision]
            
            if not vars_inferir:
                # Todas las variables de utilidad están fijadas
                key = tuple(decision[v] for v in vars_util)
                utilidad_total += valores_util.get(key, 0)
            else:
                # Inferir distribución para variables no fijadas
                prob = self.inferencia(vars_inferir[0])
                for val, p in prob.items():
                    temp_asign = decision.copy()
                    temp_asign[vars_inferir[0]] = val
                    key = tuple(temp_asign[v] for v in vars_util)
                    utilidad_total += p * valores_util.get(key, 0)
        
        return utilidad_total
    
    def interfaz_consola(self):
        """Interfaz de consola para interactuar con el modelo"""
        print(f"\n=== Modelo Probabilista Racional: {self.nombre} ===")
        print("Opciones:")
        print("1. Agregar variable")
        print("2. Agregar observación")
        print("3. Definir utilidad")
        print("4. Realizar inferencia")
        print("5. Tomar decisión racional")
        print("6. Mostrar estado")
        print("7. Salir")
        
        while True:
            opcion = input("\nSeleccione una opción (1-7): ")
            
            if opcion == "1":
                nombre = input("Nombre de la variable: ")
                tipo = input("Tipo (ALEATORIA, LATENTE, DECISION, UTILIDAD): ").upper()
                dominio = input("Dominio (valores separados por comas): ").split(',')
                padres = input("Padres (separados por comas, enter si no tiene): ").split(',')
                padres = [p.strip() for p in padres if p.strip()]
                
                print("\nDefinir distribución condicional:")
                dist = {}
                if padres:
                    from itertools import product
                    for vals_padres in product(*[self.variables[p].dominio for p in padres]):
                        print(f"\nPara {vals_padres}:")
                        probs = input(f"Probabilidades para {dominio} (separadas por comas): ").split(',')
                        probs = [float(p.strip()) for p in probs]
                        dist[vals_padres] = probs
                else:
                    probs = input(f"Probabilidades para {dominio} (separadas por comas): ").split(',')
                    probs = [float(p.strip()) for p in probs]
                    dist[()] = probs
                
                var = Variable(
                    nombre=nombre,
                    tipo=TipoVariable[tipo],
                    dominio=dominio,
                    padres=padres,
                    distribucion=dist
                )
                
                if self.agregar_variable(var):
                    print("Variable añadida correctamente.")
                else:
                    print("Error: Algunos padres no existen.")
            
            elif opcion == "2":
                var = input("Variable observada: ")
                valor = input("Valor observado: ")
                certeza = float(input("Certeza [0-1]: "))
                
                obs = Observacion(var, valor, certeza)
                if self.agregar_observacion(obs):
                    print("Observación registrada.")
                else:
                    print("Error: Variable no existe.")
            
            elif opcion == "3":
                vars_util = input("Variables de utilidad (separadas por comas): ").split(',')
                vars_util = [v.strip() for v in vars_util if v.strip()]
                
                print("\nDefinir valores de utilidad:")
                valores = {}
                from itertools import product
                dominio_util = product(*[self.variables[v].dominio for v in vars_util])
                for combo in dominio_util:
                    valor = float(input(f"Utilidad para {combo}: "))
                    valores[combo] = valor
                
                if self.definir_utilidad(vars_util, valores):
                    print("Utilidad definida.")
                else:
                    print("Error: Algunas variables no existen.")
            
            elif opcion == "4":
                objetivo = input("Variable objetivo: ")
                metodo = input("Método (ENUMERACION, MUESTREO, MCMC): ").upper()
                muestras = int(input("Número de muestras (si aplica): ") or 1000)
                
                try:
                    resultado = self.inferencia(objetivo, TipoInferencia[metodo], muestras)
                    print("\nResultado de inferencia:")
                    for val, prob in resultado.items():
                        print(f"{val}: {prob:.4f}")
                except KeyError:
                    print("Error: Variable o método no válido.")
            
            elif opcion == "5":
                vars_dec = input("Variables de decisión (separadas por comas): ").split(',')
                vars_dec = [v.strip() for v in vars_dec if v.strip()]
                
                try:
                    decision = self.decision_racional(vars_dec)
                    print("\nMejor decisión encontrada:")
                    for var, val in decision.items():
                        print(f"{var} = {val}")
                    
                    # Calcular utilidad esperada
                    utilidad = self._utilidad_esperada(decision)
                    print(f"Utilidad esperada: {utilidad:.2f}")
                except KeyError:
                    print("Error: Algunas variables no existen.")
            
            elif opcion == "6":
                print("\nEstado del modelo:")
                print(f"Variables: {len(self.variables)}")
                print(f"Observaciones: {len(self.observaciones)}")
                print(f"Funciones de utilidad: {len(self.utilidades)}")
                print("\nÚltimas 5 operaciones:")
                for op in self.historial[-5:]:
                    print(f"- {op}")
            
            elif opcion == "7":
                print("Saliendo del modelo...")
                break
            
            else:
                print("Opción no válida. Intente de nuevo.")

def ejemplo_medico():
    """
    Configura y devuelve un modelo probabilista de ejemplo
    para diagnóstico médico con decisiones de tratamiento.
    """
    modelo = ModeloProbabilista("Diagnóstico Médico")
    
    # 1. Definir variables
    # Variables aleatorias
    enfermedad = Variable(
        nombre="Enfermedad",
        tipo=TipoVariable.ALEATORIA,
        dominio=["Gripe", "Resfriado", "Ninguna"],
        padres=[],
        distribucion={
            (): [0.1, 0.3, 0.6]  # P(Gripe)=0.1, P(Resfriado)=0.3, P(Ninguna)=0.6
        }
    )
    
    fiebre = Variable(
        nombre="Fiebre",
        tipo=TipoVariable.ALEATORIA,
        dominio=["Alta", "Leve", "Ninguna"],
        padres=["Enfermedad"],
        distribucion={
            ("Gripe",): [0.7, 0.2, 0.1],
            ("Resfriado",): [0.1, 0.4, 0.5],
            ("Ninguna",): [0.01, 0.09, 0.9]
        }
    )
    
    dolor_cabeza = Variable(
        nombre="DolorCabeza",
        tipo=TipoVariable.ALEATORIA,
        dominio=["Fuerte", "Leve", "Ninguno"],
        padres=["Enfermedad"],
        distribucion={
            ("Gripe",): [0.6, 0.3, 0.1],
            ("Resfriado",): [0.2, 0.4, 0.4],
            ("Ninguna",): [0.05, 0.15, 0.8]
        }
    )
    
    # Variable de decisión (tratamiento)
    tratamiento = Variable(
        nombre="Tratamiento",
        tipo=TipoVariable.DECISION,
        dominio=["Antibiotico", "Antiviral", "Reposo"],
        padres=[],
        distribucion={}
    )
    
    # Variable de utilidad (resultado del tratamiento)
    resultado = Variable(
        nombre="Resultado",
        tipo=TipoVariable.UTILIDAD,
        dominio=["Bueno", "Regular", "Malo"],
        padres=["Enfermedad", "Tratamiento"],
        distribucion={
            ("Gripe", "Antibiotico"): [0.1, 0.3, 0.6],
            ("Gripe", "Antiviral"): [0.7, 0.2, 0.1],
            ("Gripe", "Reposo"): [0.4, 0.4, 0.2],
            ("Resfriado", "Antibiotico"): [0.3, 0.4, 0.3],
            ("Resfriado", "Antiviral"): [0.2, 0.5, 0.3],
            ("Resfriado", "Reposo"): [0.6, 0.3, 0.1],
            ("Ninguna", "Antibiotico"): [0.1, 0.2, 0.7],
            ("Ninguna", "Antiviral"): [0.1, 0.3, 0.6],
            ("Ninguna", "Reposo"): [0.8, 0.15, 0.05]
        }
    )
    
    # 2. Añadir variables al modelo
    modelo.agregar_variable(enfermedad)
    modelo.agregar_variable(fiebre)
    modelo.agregar_variable(dolor_cabeza)
    modelo.agregar_variable(tratamiento)
    modelo.agregar_variable(resultado)
    
    # 3. Definir función de utilidad
    modelo.definir_utilidad(
        ["Resultado"],
        {
            ("Bueno",): 100,
            ("Regular",): 50,
            ("Malo",): -100
        }
    )
    
    return modelo

if __name__ == "__main__":
    # Crear y ejecutar modelo médico de ejemplo
    modelo_medico = ejemplo_medico()
    
    # Ejemplo de uso:
    print("\n=== EJEMPLO MÉDICO ===")
    
    # 1. Registrar observaciones (síntomas)
    modelo_medico.agregar_observacion(Observacion("Fiebre", "Alta", 0.9))
    modelo_medico.agregar_observacion(Observacion("DolorCabeza", "Fuerte", 0.8))
    
    # 2. Inferir enfermedad más probable
    print("\nInferencia de enfermedad dado los síntomas:")
    dist_enfermedad = modelo_medico.inferencia("Enfermedad")
    for enf, prob in dist_enfermedad.items():
        print(f"{enf}: {prob:.2f}")
    
    # 3. Tomar decisión óptima de tratamiento
    print("\nDecisión óptima de tratamiento:")
    decision = modelo_medico.decision_racional(["Tratamiento"])
    print(f"Tratamiento recomendado: {decision['Tratamiento']}")
    
    # 4. Calcular resultado esperado del tratamiento recomendado
    modelo_medico.agregar_observacion(Observacion("Tratamiento", decision['Tratamiento'], 1.0))
    dist_resultado = modelo_medico.inferencia("Resultado")
    print("\nResultado esperado del tratamiento:")
    for res, prob in dist_resultado.items():
        print(f"{res}: {prob:.2f}")
    
    # Opcional: Ejecutar interfaz interactiva
    # modelo_medico.interfaz_consola()