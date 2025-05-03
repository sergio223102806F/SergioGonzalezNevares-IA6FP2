# -*- coding: utf-8 -*-


# Importaciones necesarias
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum, auto
from dataclasses import dataclass
from collections import defaultdict

class EstadoCreencia(Enum):
    """Estados en los que puede estar una creencia"""
    ACTIVA = auto()       # Creencia actualmente aceptada
    DERROTADA = auto()    # Creencia invalidada por nueva información
    INCIERTA = auto()     # Creencia con soporte insuficiente

class TipoRegla(Enum):
    """Tipos de reglas no monotónicas"""
    DEFAULT = auto()      # Regla por defecto (razonamiento por defecto)
    DEFEASIBLE = auto()   # Regla anulable (derrotable)
    ESTRICTA = auto()     # Regla clásica (no anulable)

@dataclass
class Creencia:
    """Estructura para representar creencias con razonamiento no monotónico"""
    contenido: str                # Proposición de la creencia
    estado: EstadoCreencia        # Estado actual de la creencia
    soporte: Set[str]             # Conjunto de premisas que la apoyan
    reglas_afectadas: List[str]   # Reglas que pueden afectar esta creencia

@dataclass
class ReglaNoMonotonica:
    """Representación de reglas con excepciones"""
    nombre: str                   # Identificador de la regla
    tipo: TipoRegla               # Tipo de regla
    antecedente: List[str]        # Premisas requeridas
    consecuente: str              # Conclusión de la regla
    excepciones: List[str]        # Condiciones que invalidan la regla
    prioridad: int = 0            # Nivel de prioridad para resolver conflictos

class SistemaNoMonotonico:
    """
    Sistema de razonamiento no monotónico que implementa:
    - Razonamiento por defecto
    - Reglas derrotables
    - Actualización de creencias
    """
    
    def __init__(self):
        """Inicializa el sistema con estructuras básicas"""
        self.creencias: Dict[str, Creencia] = {}          # Diccionario de creencias
        self.reglas: Dict[str, ReglaNoMonotonica] = {}    # Reglas del sistema
        self.hechos_observados: Set[str] = set()          # Hechos conocidos
        self.historial: List[Tuple[str, str]] = []        # Historial de cambios
        
    def agregar_regla(self, regla: ReglaNoMonotonica) -> None:
        """
        Añade una nueva regla al sistema
        
        Args:
            regla (ReglaNoMonotonica): Regla a añadir
        """
        self.reglas[regla.nombre] = regla
        
    def observar_hecho(self, hecho: str) -> None:
        """
        Añade un hecho observado al sistema y actualiza las creencias
        
        Args:
            hecho (str): Hecho observado que puede afectar el sistema
        """
        self.hechos_observados.add(hecho)
        self.actualizar_creencias()
        
    def actualizar_creencias(self) -> None:
        """
        Re-evalúa todas las creencias basadas en la información actual
        y aplica el razonamiento no monotónico
        """
        # Primero desactivar todas las creencias derivadas
        for nombre, creencia in self.creencias.items():
            if not creencia.soporte:  # No cambiar hechos observados
                continue
            creencia.estado = EstadoCreencia.INCIERTA
        
        # Aplicar todas las reglas para generar nuevas creencias
        for regla in self.reglas.values():
            self.aplicar_regla(regla)
            
        # Verificar conflictos y derrotar creencias si es necesario
        self.resolver_conflictos()
    
    def aplicar_regla(self, regla: ReglaNoMonotonica) -> bool:
        """
        Intenta aplicar una regla para generar nuevas creencias
        
        Args:
            regla (ReglaNoMonotonica): Regla a aplicar
            
        Returns:
            bool: True si la regla pudo aplicarse, False si no
        """
        # Verificar si todas las premisas se cumplen
        premisas_cumplidas = all(
            prem in self.hechos_observados or 
            (prem in self.creencias and self.creencias[prem].estado == EstadoCreencia.ACTIVA)
            for prem in regla.antecedente
        )
        
        # Verificar si alguna excepción se cumple
        excepcion_cumplida = any(
            exc in self.hechos_observados or 
            (exc in self.creencias and self.creencias[exc].estado == EstadoCreencia.ACTIVA)
            for exc in regla.excepciones
        )
        
        if premisas_cumplidas and not excepcion_cumplida:
            # Crear o actualizar la creencia resultante
            if regla.consecuente not in self.creencias:
                self.creencias[regla.consecuente] = Creencia(
                    contenido=regla.consecuente,
                    estado=EstadoCreencia.ACTIVA,
                    soporte=set(regla.antecedente),
                    reglas_afectadas=[regla.nombre]
                )
            else:
                creencia = self.creencias[regla.consecuente]
                creencia.soporte.update(regla.antecedente)
                creencia.reglas_afectadas.append(regla.nombre)
                creencia.estado = EstadoCreencia.ACTIVA
                
            # Registrar en el historial
            self.historial.append((f"Aplicada regla {regla.nombre}", regla.consecuente))
            return True
            
        return False
    
    def resolver_conflictos(self) -> None:
        """
        Resuelve conflictos entre creencias basadas en prioridades de reglas
        """
        # Buscar creencias conflictivas
        conflictos: Dict[str, List[str]] = defaultdict(list)
        
        for nombre, creencia in self.creencias.items():
            if creencia.estado == EstadoCreencia.ACTIVA:
                for regla_nombre in creencia.reglas_afectadas:
                    regla = self.reglas[regla_nombre]
                    # Verificar si esta regla derrota otras
                    for otra_creencia in self.creencias.values():
                        if otra_creencia.contenido in regla.excepciones:
                            conflictos[nombre].append(otra_creencia.contenido)
        
        # Resolver conflictos basados en prioridad
        for creencia, derrotadas in conflictos.items():
            for derrotada in derrotadas:
                if derrotada in self.creencias:
                    # Comparar prioridades de reglas
                    max_prioridad_creencia = max(
                        self.reglas[r].prioridad 
                        for r in self.creencias[creencia].reglas_afectadas
                    )
                    max_prioridad_derrotada = max(
                        self.reglas[r].prioridad 
                        for r in self.creencias[derrotada].reglas_afectadas
                    )
                    
                    if max_prioridad_creencia > max_prioridad_derrotada:
                        self.creencias[derrotada].estado = EstadoCreencia.DERROTADA
                        self.historial.append((f"Derrotada {derrotada}", f"por {creencia}"))
    
    def consultar_creencia(self, proposicion: str) -> Optional[EstadoCreencia]:
        """
        Consulta el estado actual de una creencia
        
        Args:
            proposicion (str): Proposición a consultar
            
        Returns:
            Optional[EstadoCreencia]: Estado de la creencia o None si no existe
        """
        if proposicion in self.creencias:
            return self.creencias[proposicion].estado
        return None
    
    def generar_informe(self) -> Dict:
        """
        Genera un informe del estado actual del sistema
        
        Returns:
            Dict: Diccionario con estadísticas del sistema
        """
        return {
            "total_creencias": len(self.creencias),
            "creencias_activas": sum(1 for c in self.creencias.values() 
                                   if c.estado == EstadoCreencia.ACTIVA),
            "creencias_derrotadas": sum(1 for c in self.creencias.values() 
                                      if c.estado == EstadoCreencia.DERROTADA),
            "total_reglas": len(self.reglas),
            "hechos_observados": len(self.hechos_observados)
        }

def demostracion_razonamiento_default():
    """
    Demuestra el razonamiento por defecto con el clásico ejemplo de los pájaros
    """
    sistema = SistemaNoMonotonico()
    
    # 1. Definir reglas
    sistema.agregar_regla(ReglaNoMonotonica(
        nombre="default_pajaro_vuela",
        tipo=TipoRegla.DEFAULT,
        antecedente=["Pájaro(x)"],
        consecuente="Vuela(x)",
        excepciones=["Pingüino(x)", "Herido(x)"],
        prioridad=1
    ))
    
    sistema.agregar_regla(ReglaNoMonotonica(
        nombre="pinguino_no_vuela",
        tipo=TipoRegla.DEFEASIBLE,
        antecedente=["Pingüino(x)"],
        consecuente="¬Vuela(x)",
        excepciones=[],
        prioridad=2  # Mayor prioridad que la regla por defecto
    ))
    
    # 2. Observar hechos iniciales
    sistema.observar_hecho("Pájaro(Tweety)")
    
    print("\nEstado inicial:")
    print("Tweety vuela?", sistema.consultar_creencia("Vuela(Tweety)"))
    
    # 3. Añadir nueva información (Tweety es un pingüino)
    sistema.observar_hecho("Pingüino(Tweety)")
    
    print("\nDespués de saber que Tweety es un pingüino:")
    print("Tweety vuela?", sistema.consultar_creencia("Vuela(Tweety)"))
    
    # 4. Mostrar informe final
    print("\nInforme del sistema:")
    for k, v in sistema.generar_informe().items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    demostracion_razonamiento_default()