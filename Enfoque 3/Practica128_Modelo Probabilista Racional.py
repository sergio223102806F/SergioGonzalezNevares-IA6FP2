# -*- coding: utf-8 -*-                                  # Encoding declaration for Python 2 compatibility

# Importaciones necesarias                               # Import section begins
from typing import Dict, List, Optional, Set, Tuple      # Type hints for better code documentation
from dataclasses import dataclass                        # Decorator for creating classes with less boilerplate
from enum import Enum, auto                              # For creating enumerations
import math                                              # Mathematical functions
import random                                            # Random number generation

class TipoVariable(Enum):                                # Enumeration for variable types
    """Tipos de variables en el modelo probabilista"""   # Docstring for the enum
    ALEATORIA = auto()                                   # Observable random variable
    LATENTE = auto()                                     # Unobservable (hidden) variable  
    DECISION = auto()                                    # Decision variable
    UTILIDAD = auto()                                    # Utility/reward variable

class TipoInferencia(Enum):                              # Enumeration for inference methods
    """Métodos de inferencia probabilística"""           # Docstring for the enum
    ENUMERACION = auto()                                 # Exact enumeration method
    MUESTREO = auto()                                    # Approximate sampling method
    MCMC = auto()                                        # Markov Chain Monte Carlo method

@dataclass                                               # Data class for variables
class Variable:
    """Estructura para representar variables en el modelo"""  # Class docstring
    nombre: str                                          # Variable name
    tipo: TipoVariable                                   # Variable type from enum
    dominio: List[str]                                   # Possible values
    padres: List[str]                                    # Parent variables in network
    distribucion: Dict[Tuple, List[float]]               # Conditional probability distribution

@dataclass                                               # Data class for observations
class Observacion:
    """Registro de una observación/evidencia"""          # Class docstring
    variable: str                                        # Observed variable name
    valor: str                                           # Observed value
    certeza: float = 1.0                                 # Confidence level [0,1]

class ModeloProbabilista:                                # Main probabilistic model class
    """
    Implementación de un modelo probabilista racional    # Class docstring begins
    que incluye:
    - Red bayesiana para relaciones de dependencia
    - Toma de decisiones racionales
    - Múltiples métodos de inferencia
    """
    
    def __init__(self, nombre: str):                     # Constructor method
        """
        Inicializa el modelo probabilista               # Method docstring
        
        Args:
            nombre (str): Nombre identificador del modelo
        """
        self.nombre = nombre                             # Model name
        self.variables: Dict[str, Variable] = {}         # Dictionary of variables
        self.observaciones: Dict[str, Observacion] = {}  # Dictionary of observations
        self.utilidades: Dict[Tuple, float] = {}         # Utility functions
        self.historial: List[str] = []                   # Operation history log
    
    def agregar_variable(self, var: Variable) -> bool:   # Add variable method
        """
        Añade una nueva variable al modelo             # Method docstring
        
        Args:
            var (Variable): Variable a añadir
            
        Returns:
            bool: True si se añadió correctamente
        """
        for padre in var.padres:                        # Check all parents exist
            if padre not in self.variables:             # If parent missing
                return False                           # Return failure
                
        self.variables[var.nombre] = var               # Add variable to dictionary
        self.historial.append(f"Añadida variable {var.nombre}")  # Log operation
        return True                                    # Return success
    
    def agregar_observacion(self, obs: Observacion) -> bool:  # Add observation method
        """
        Registra una nueva observación/evidencia       # Method docstring
        
        Args:
            obs (Observacion): Observación a registrar
            
        Returns:
            bool: True si la variable existe y se registró
        """
        if obs.variable not in self.variables:        # Check variable exists
            return False                              # Return failure if not
            
        self.observaciones[obs.variable] = obs        # Add observation
        self.historial.append(f"Registrada observación {obs.variable}={obs.valor}")  # Log
        return True                                   # Return success
    
    def definir_utilidad(self, variables: List[str], valores: Dict[Tuple, float]) -> bool:  # Define utility
        """
        Define la función de utilidad para un conjunto de variables  # Method docstring
        
        Args:
            variables (List[str]): Variables que afectan la utilidad
            valores (Dict[Tuple, float]): Valores de utilidad para cada combinación
            
        Returns:
            bool: True si todas las variables existen
        """
        for var in variables:                         # Check all variables exist
            if var not in self.variables:             # If any missing
                return False                         # Return failure
                
        self.utilidades[(tuple(variables))] = valores  # Store utility function
        self.historial.append(f"Definida utilidad para {variables}")  # Log
        return True                                   # Return success
    
    def inferencia(self, objetivo: str, metodo: TipoInferencia = TipoInferencia.ENUMERACION, 
                  n_muestras: int = 1000) -> Dict[str, float]:  # Inference method
        """
        Realiza inferencia probabilística sobre una variable objetivo  # Method docstring
        
        Args:
            objetivo (str): Variable objetivo a inferir
            metodo (TipoInferencia): Método de inferencia a usar
            n_muestras (int): Número de muestras para métodos de muestreo
            
        Returns:
            Dict[str, float]: Distribución de probabilidad resultante
        """
        if objetivo not in self.variables:           # Check target exists
            return {}                               # Return empty if not
            
        if metodo == TipoInferencia.ENUMERACION:     # Exact enumeration
            return self._inferencia_enum(objetivo)   # Call exact method
        elif metodo == TipoInferencia.MUESTREO:      # Direct sampling
            return self._muestreo_directo(objetivo, n_muestras)  # Call sampling
        else:                                        # MCMC
            return self._mcmc(objetivo, n_muestras)  # Call MCMC method
    
    def _inferencia_enum(self, objetivo: str) -> Dict[str, float]:  # Exact inference
        """
        Inferencia por enumeración exacta (método exacto pero costoso)  # Method docstring
        
        Args:
            objetivo (str): Variable objetivo
            
        Returns:
            Dict[str, float]: Distribución de probabilidad
        """
        var = self.variables[objetivo]               # Get target variable
        prob = {valor: 0.0 for valor in var.dominio} # Initialize probabilities
        total = 0.0                                  # Normalization factor
        
        vars_ocultas = [v for v in self.variables if v not in self.observaciones and v != objetivo]  # Hidden vars
        
        from itertools import product                # Import for Cartesian product
        for valores_ocultas in product(*[self.variables[v].dominio for v in vars_ocultas]):  # All combinations
            asignacion = {}                         # Current assignment
            for i, v in enumerate(vars_ocultas):    # Build full assignment
                asignacion[v] = valores_ocultas[i]
            for v, obs in self.observaciones.items():  # Add observations
                asignacion[v] = obs.valor
                
            p_conjunta = self._probabilidad_conjunta(asignacion)  # Joint probability
            
            for valor in var.dominio:               # For each target value
                asignacion[objetivo] = valor        # Set target value
                p_cond = self._probabilidad_conjunta(asignacion) / p_conjunta if p_conjunta > 0 else 0  # Conditional
                prob[valor] += p_cond              # Accumulate
                total += p_cond                    # Update total
        
        if total > 0:                              # Normalize if needed
            for valor in prob:
                prob[valor] /= total
                
        return prob                                # Return distribution
    
    def _muestreo_directo(self, objetivo: str, n_muestras: int) -> Dict[str, float]:  # Direct sampling
        """
        Inferencia por muestreo directo (aproximado)  # Method docstring
        
        Args:
            objetivo (str): Variable objetivo
            n_muestras (int): Número de muestras a generar
            
        Returns:
            Dict[str, float]: Distribución de probabilidad aproximada
        """
        conteo = {valor: 0 for valor in self.variables[objetivo].dominio}  # Initialize counts
        
        for _ in range(n_muestras):                 # Generate samples
            muestra = self._generar_muestra()       # Get random sample
            valor_objetivo = muestra[objetivo]      # Get target value
            conteo[valor_objetivo] += 1             # Count occurrences
        
        return {v: c/n_muestras for v, c in conteo.items()}  # Normalize counts
    
    def _mcmc(self, objetivo: str, n_muestras: int) -> Dict[str, float]:  # MCMC method
        """
        Inferencia por MCMC (Gibbs sampling)        # Method docstring
        
        Args:
            objetivo (str): Variable objetivo
            n_muestras (int): Número de muestras a generar
            
        Returns:
            Dict[str, float]: Distribución de probabilidad aproximada
        """
        asignacion = {}                             # Initialize assignment
        vars_ocultas = [v for v in self.variables if v not in self.observaciones]  # Hidden vars
        
        for v in vars_ocultas:                     # Random initialization
            asignacion[v] = random.choice(self.variables[v].dominio)
        for v, obs in self.observaciones.items():   # Set observed values
            asignacion[v] = obs.valor
        
        conteo = {valor: 0 for valor in self.variables[objetivo].dominio}  # Initialize counts
        
        for _ in range(n_muestras):                 # Generate samples
            for v in vars_ocultas:                  # Sample each hidden var
                if v == objetivo:                   # Skip target for now
                    continue
                    
                dist = self._distribucion_condicional(v, asignacion)  # Get conditional
                nuevo_valor = random.choices(list(dist.keys()), weights=list(dist.values()))[0]  # Sample
                asignacion[v] = nuevo_valor         # Update assignment
            
            dist = self._distribucion_condicional(objetivo, asignacion)  # Sample target
            valor_objetivo = random.choices(list(dist.keys()), weights=list(dist.values()))[0]
            asignacion[objetivo] = valor_objetivo
            conteo[valor_objetivo] += 1             # Count
        
        return {v: c/n_muestras for v, c in conteo.items()}  # Normalize counts
    
    def _generar_muestra(self) -> Dict[str, str]:   # Generate random sample
        """
        Genera una muestra aleatoria según la distribución conjunta  # Method docstring
        
        Returns:
            Dict[str, str]: Asignación de valores para todas las variables
        """
        muestra = {}                                # Initialize sample
        orden = self._orden_topologico()            # Get topological order
        
        for var in orden:                           # Sample in order
            if var in self.observaciones:           # If observed
                muestra[var] = self.observaciones[var].valor  # Use observed value
            else:                                   # If hidden
                padres_vals = tuple(muestra[p] for p in self.variables[var].padres)  # Get parent values
                dist = self.variables[var].distribucion[padres_vals]  # Get distribution
                muestra[var] = random.choices(self.variables[var].dominio, weights=dist)[0]  # Sample
        
        return muestra                              # Return complete sample
    
    def _orden_topologico(self) -> List[str]:       # Topological sort
        """
        Orden topológico de variables (padres antes que hijos)  # Method docstring
        
        Returns:
            List[str]: Orden de variables
        """
        visitadas = set()                           # Track visited nodes
        orden = []                                  # Result order
        
        def visitar(nodo):                          # Recursive visit function
            if nodo not in visitadas:               # If not visited
                visitadas.add(nodo)                 # Mark visited
                for padre in self.variables[nodo].padres:  # Visit parents first
                    visitar(padre)
                orden.append(nodo)                  # Add to order after parents
        
        for var in self.variables:                  # Visit all variables
            visitar(var)
            
        return orden                                # Return topological order
    
    def _probabilidad_conjunta(self, asignacion: Dict[str, str]) -> float:  # Joint probability
        """
        Calcula la probabilidad conjunta de una asignación completa  # Method docstring
        
        Args:
            asignacion (Dict[str, str]): Asignación de valores a variables
            
        Returns:
            float: Probabilidad conjunta
        """
        p = 1.0                                    # Initialize probability
        for var, valor in asignacion.items():      # For each assignment
            if var not in self.variables:          # Check variable exists
                return 0.0                        # Return 0 if invalid
                
            padres_vals = tuple(asignacion[p] for p in self.variables[var].padres)  # Parent values
            dist = self.variables[var].distribucion.get(padres_vals, [0]*len(self.variables[var].dominio))  # Distribution
            
            try:                                   # Get probability
                idx = self.variables[var].dominio.index(valor)  # Value index
                p *= dist[idx]                    # Multiply probability
            except ValueError:                     # If value not in domain
                return 0.0                        # Return 0 probability
                
        return p                                  # Return joint probability
    
    def _distribucion_condicional(self, var: str, asignacion: Dict[str, str]) -> Dict[str, float]:  # Conditional dist
        """
        Calcula la distribución condicional de una variable dada una asignación parcial  # Method docstring
        
        Args:
            var (str): Variable objetivo
            asignacion (Dict[str, str]): Asignación parcial
            
        Returns:
            Dict[str, float]: Distribución condicional
        """
        if var not in self.variables:              # Check variable exists
            return {}                             # Return empty if not
            
        padres_vals = tuple(asignacion[p] for p in self.variables[var].padres)  # Parent values
        
        dist = self.variables[var].distribucion.get(padres_vals, [0]*len(self.variables[var].dominio))  # Get distribution
        
        return {v: p for v, p in zip(self.variables[var].dominio, dist)}  # Map values to probabilities
    
    def decision_racional(self, variables_decision: List[str]) -> Dict[str, str]:  # Rational decision
        """
        Toma una decisión racional maximizando la utilidad esperada  # Method docstring
        
        Args:
            variables_decision (List[str]): Variables sobre las que decidir
            
        Returns:
            Dict[str, str]: Mejor asignación encontrada
        """
        mejor_asignacion = {}                      # Best assignment
        mejor_utilidad = -float('inf')             # Initialize best utility
        
        from itertools import product              # Import for Cartesian product
        decisiones_posibles = product(*[self.variables[v].dominio for v in variables_decision])  # All combinations
        
        for decision in decisiones_posibles:       # Evaluate each decision
            asignacion = {}                       # Current assignment
            for i, v in enumerate(variables_decision):
                asignacion[v] = decision[i]      # Set decision variables
            
            obs_previas = self.observaciones.copy()  # Save current observations
            for v, val in asignacion.items():     # Set decision as observation
                self.agregar_observacion(Observacion(v, val, 1.0))
            
            utilidad = self._utilidad_esperada(asignacion)  # Compute expected utility
            
            self.observaciones = obs_previas      # Restore observations
            
            if utilidad > mejor_utilidad:         # Update best if better
                mejor_utilidad = utilidad
                mejor_asignacion = asignacion.copy()
        
        return mejor_asignacion                   # Return best decision
    
    def _utilidad_esperada(self, decision: Dict[str, str]) -> float:  # Expected utility
        """
        Calcula la utilidad esperada dada una decisión  # Method docstring
        
        Args:
            decision (Dict[str, str]): Asignación de variables de decisión
            
        Returns:
            float: Utilidad esperada
        """
        utilidad_total = 0.0                      # Initialize total utility
        
        for vars_util, valores_util in self.utilidades.items():  # For each utility function
            vars_inferir = [v for v in vars_util if v not in decision]  # Vars to infer
            
            if not vars_inferir:                  # All utility vars are decided
                key = tuple(decision[v] for v in vars_util)  # Build key
                utilidad_total += valores_util.get(key, 0)  # Add utility
            else:                                 # Need to infer some vars
                prob = self.inferencia(vars_inferir[0])  # Get distribution
                for val, p in prob.items():       # For each possible value
                    temp_asign = decision.copy()  # Temporary assignment
                    temp_asign[vars_inferir[0]] = val  # Set inferred value
                    key = tuple(temp_asign[v] for v in vars_util)  # Build key
                    utilidad_total += p * valores_util.get(key, 0)  # Add weighted utility
        
        return utilidad_total                     # Return total expected utility
    
    def interfaz_consola(self):                   # Console interface
        """Interfaz de consola para interactuar con el modelo"""  # Method docstring
        print(f"\n=== Modelo Probabilista Racional: {self.nombre} ===")
        print("Opciones:")
        print("1. Agregar variable")
        print("2. Agregar observación")
        print("3. Definir utilidad")
        print("4. Realizar inferencia")
        print("5. Tomar decisión racional")
        print("6. Mostrar estado")
        print("7. Salir")
        
        while True:                               # Main loop
            opcion = input("\nSeleccione una opción (1-7): ")
            
            if opcion == "1":                     # Add variable
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
            
            elif opcion == "2":                   # Add observation
                var = input("Variable observada: ")
                valor = input("Valor observado: ")
                certeza = float(input("Certeza [0-1]: "))
                
                obs = Observacion(var, valor, certeza)
                if self.agregar_observacion(obs):
                    print("Observación registrada.")
                else:
                    print("Error: Variable no existe.")
            
            elif opcion == "3":                   # Define utility
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
            
            elif opcion == "4":                   # Perform inference
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
            
            elif opcion == "5":                   # Make rational decision
                vars_dec = input("Variables de decisión (separadas por comas): ").split(',')
                vars_dec = [v.strip() for v in vars_dec if v.strip()]
                
                try:
                    decision = self.decision_racional(vars_dec)
                    print("\nMejor decisión encontrada:")
                    for var, val in decision.items():
                        print(f"{var} = {val}")
                    
                    utilidad = self._utilidad_esperada(decision)
                    print(f"Utilidad esperada: {utilidad:.2f}")
                except KeyError:
                    print("Error: Algunas variables no existen.")
            
            elif opcion == "6":                   # Show model state
                print("\nEstado del modelo:")
                print(f"Variables: {len(self.variables)}")
                print(f"Observaciones: {len(self.observaciones)}")
                print(f"Funciones de utilidad: {len(self.utilidades)}")
                print("\nÚltimas 5 operaciones:")
                for op in self.historial[-5:]:
                    print(f"- {op}")
            
            elif opcion == "7":                   # Exit
                print("Saliendo del modelo...")
                break
            
            else:                                 # Invalid option
                print("Opción no válida. Intente de nuevo.")

def ejemplo_medico():                             # Medical example setup
    """
    Configura y devuelve un modelo probabilista de ejemplo  # Function docstring
    para diagnóstico médico con decisiones de tratamiento.
    """
    modelo = ModeloProbabilista("Diagnóstico Médico")  # Create model
    
    # 1. Definir variables
    # Variables aleatorias
    enfermedad = Variable(                          # Disease variable
        nombre="Enfermedad",
        tipo=TipoVariable.ALEATORIA,
        dominio=["Gripe", "Resfriado", "Ninguna"],
        padres=[],
        distribucion={
            (): [0.1, 0.3, 0.6]  # P(Gripe)=0.1, P(Resfriado)=0.3, P(Ninguna)=0.6
        }
    )
    
    fiebre = Variable(                             # Fever variable
        nombre="Fiebre",
        tipo=TipoVariable.ALEATORIA,
        dominio=["Alta", "Leve", "Ninguna"],
        padres=["Enfermedad"],
        distribucion={
            ("Gripe",): [0.7, 0.2, 0.1],         # Given Flu
            ("Resfriado",): [0.1, 0.4, 0.5],      # Given Cold
            ("Ninguna",): [0.01, 0.09, 0.9]       # Given Nothing
        }
    )
    
    dolor_cabeza = Variable(                       # Headache variable
        nombre="DolorCabeza",
        tipo=TipoVariable.ALEATORIA,
        dominio=["Fuerte", "Leve", "Ninguno"],
        padres=["Enfermedad"],
        distribucion={
            ("Gripe",): [0.6, 0.3, 0.1],         # Given Flu
            ("Resfriado",): [0.2, 0.4, 0.4],      # Given Cold
            ("Ninguna",): [0.05, 0.15, 0.8]       # Given Nothing
        }
    )
    
    # Variable de decisión (tratamiento)
    tratamiento = Variable(                        # Treatment decision variable
        nombre="Tratamiento",
        tipo=TipoVariable.DECISION,
        dominio=["Antibiotico", "Antiviral", "Reposo"],
        padres=[],
        distribucion={}
    )
    
    # Variable de utilidad (resultado del tratamiento)
    resultado = Variable(                          # Treatment outcome variable
        nombre="Resultado",
        tipo=TipoVariable.UTILIDAD,
        dominio=["Bueno", "Regular", "Malo"],
        padres=["Enfermedad", "Tratamiento"],
        distribucion={
            ("Gripe", "Antibiotico"): [0.1, 0.3, 0.6],  # Flu + Antibiotic
            ("Gripe", "Antiviral"): [0.7, 0.2, 0.1],    # Flu + Antiviral
            ("Gripe", "Reposo"): [0.4, 0.4, 0.2],       # Flu + Rest
            ("Resfriado", "Antibiotico"): [0.3, 0.4, 0.3],  # Cold + Antibiotic
            ("Resfriado", "Antiviral"): [0.2, 0.5, 0.3],    # Cold + Antiviral
            ("Resfriado", "Reposo"): [0.6, 0.3, 0.1],       # Cold + Rest
            ("Ninguna", "Antibiotico"): [0.1, 0.2, 0.7],    # Nothing + Antibiotic
            ("Ninguna", "Antiviral"): [0.1, 0.3, 0.6],      # Nothing + Antiviral
            ("Ninguna", "Reposo"): [0.8, 0.15, 0.05]        # Nothing + Rest
        }
    )
    
    # 2. Añadir variables al modelo
    modelo.agregar_variable(enfermedad)            # Add disease
    modelo.agregar_variable(fiebre)                # Add fever
    modelo.agregar_variable(dolor_cabeza)          # Add headache
    modelo.agregar_variable(tratamiento)           # Add treatment
    modelo.agregar_variable(resultado)             # Add outcome
    
    # 3. Definir función de utilidad
    modelo.definir_utilidad(                       # Define utility function
        ["Resultado"],
        {
            ("Bueno",): 100,                      # Good outcome utility
            ("Regular",): 50,                      # Fair outcome utility
            ("Malo",): -100                        # Bad outcome utility
        }
    )
    
    return modelo                                  # Return configured model

if __name__ == "__main__":                        # Main execution block
    # Crear y ejecutar modelo médico de ejemplo
    modelo_medico = ejemplo_medico()              # Create medical model
    
    # Ejemplo de uso:
    print("\n=== EJEMPLO MÉDICO ===")             # Example header
    
    # 1. Registrar observaciones (síntomas)
    modelo_medico.agregar_observacion(Observacion("Fiebre", "Alta", 0.9))  # High fever
    modelo_medico.agregar_observacion(Observacion("DolorCabeza", "Fuerte", 0.8))  # Strong headache
    
    # 2. Inferir enfermedad más probable
    print("\nInferencia de enfermedad dado los síntomas:")
    dist_enfermedad = modelo_medico.inferencia("Enfermedad")  # Infer disease
    for enf, prob in dist_enfermedad.items():     # Print probabilities
        print(f"{enf}: {prob:.2f}")
    
    # 3. Tomar decisión óptima de tratamiento
    print("\nDecisión óptima de tratamiento:")
    decision = modelo_medico.decision_racional(["Tratamiento"])  # Best treatment
    print(f"Tratamiento recomendado: {decision['Tratamiento']}")
    
    # 4. Calcular resultado esperado del tratamiento recomendado
    modelo_medico.agregar_observacion(Observacion("Tratamiento", decision['Tratamiento'], 1.0))  # Set treatment
    dist_resultado = modelo_medico.inferencia("Resultado")  # Infer outcome
    print("\nResultado esperado del tratamiento:")
    for res, prob in dist_resultado.items():       # Print outcome probabilities
        print(f"{res}: {prob:.2f}")
    
    # Opcional: Ejecutar interfaz interactiva
    # modelo_medico.interfaz_consola()             # Uncomment to run interactive console