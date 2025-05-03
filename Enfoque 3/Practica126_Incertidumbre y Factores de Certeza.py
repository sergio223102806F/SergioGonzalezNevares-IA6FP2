# -*- coding: utf-8 -*-


# Importaciones necesarias
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import math

class TipoIncertidumbre(Enum):
    """Tipos de modelos de incertidumbre implementados"""
    FACTOR_CERTEZA = auto()    # Modelo de factores de certeza (MYCIN)
    PROBABILISTICO = auto()    # Modelo probabilístico simple
    LOGICA_DIFUSA = auto()     # Modelo de lógica difusa

@dataclass
class ReglaIncertidumbre:
    """Estructura para reglas con manejo de incertidumbre"""
    nombre: str                # Identificador de la regla
    antecedentes: List[Tuple[str, float]]  # Lista de (premisa, peso)
    consecuente: str           # Conclusión de la regla
    factor_certeza: float      # FC de la regla [0, 1]
    tipo: TipoIncertidumbre    # Tipo de modelo usado

@dataclass
class HechoIncertidumbre:
    """Representa un hecho con su grado de incertidumbre"""
    contenido: str            # Enunciado del hecho
    certeza: float            # Grado de certeza [-1, 1] o [0, 1]
    tipo: TipoIncertidumbre   # Tipo de modelo usado
    fuente: str               # Cómo se obtuvo este hecho

class SistemaIncertidumbre:
    """
    Sistema para manejo de incertidumbre usando:
    - Factores de certeza (MYCIN)
    - Probabilidades simples
    - Lógica difusa básica
    """
    
    def __init__(self):
        """Inicializa las estructuras del sistema"""
        self.hechos: Dict[str, HechoIncertidumbre] = {}     # Hechos conocidos
        self.reglas: Dict[str, ReglaIncertidumbre] = {}     # Reglas de inferencia
        self.historial: List[str] = []                      # Historial de operaciones
    
    def agregar_hecho(self, hecho: HechoIncertidumbre) -> bool:
        """
        Añade un nuevo hecho al sistema, combinando certeza si ya existe
        
        Args:
            hecho (HechoIncertidumbre): Hecho a añadir
            
        Returns:
            bool: True si se añadió o actualizó correctamente
        """
        # Verificar rango de certeza según el tipo
        if hecho.tipo == TipoIncertidumbre.FACTOR_CERTEZA:
            if not -1 <= hecho.certeza <= 1:
                return False
        else:  # Para modelos probabilísticos y difusos
            if not 0 <= hecho.certeza <= 1:
                return False
        
        if hecho.contenido in self.hechos:
            # Combinar factores de certeza si el hecho ya existe
            existente = self.hechos[hecho.contenido]
            if existente.tipo != hecho.tipo:
                return False
                
            if existente.tipo == TipoIncertidumbre.FACTOR_CERTEZA:
                # Combinación MYCIN de factores de certeza
                nueva_certeza = existente.certeza + hecho.certeza * (1 - existente.certeza)
            else:
                # Para otros modelos, tomar el máximo (podría mejorarse)
                nueva_certeza = max(existente.certeza, hecho.certeza)
                
            self.hechos[hecho.contenido].certeza = nueva_certeza
            self.historial.append(f"Actualizado hecho {hecho.contenido} con certeza {nueva_certeza:.2f}")
        else:
            self.hechos[hecho.contenido] = hecho
            self.historial.append(f"Añadido hecho {hecho.contenido} con certeza {hecho.certeza:.2f}")
            
        return True
    
    def agregar_regla(self, regla: ReglaIncertidumbre) -> bool:
        """
        Añade una nueva regla al sistema
        
        Args:
            regla (ReglaIncertidumbre): Regla a añadir
            
        Returns:
            bool: True si se añadió correctamente
        """
        # Validar la regla según su tipo
        if regla.tipo == TipoIncertidumbre.FACTOR_CERTEZA:
            if not -1 <= regla.factor_certeza <= 1:
                return False
        else:
            if not 0 <= regla.factor_certeza <= 1:
                return False
                
        self.reglas[regla.nombre] = regla
        self.historial.append(f"Añadida regla {regla.nombre}")
        return True
    
    def inferir(self, objetivo: str) -> Optional[float]:
        """
        Realiza inferencia con incertidumbre sobre un objetivo específico
        
        Args:
            objetivo (str): Hecho objetivo a inferir
            
        Returns:
            Optional[float]: Certeza del objetivo o None si no se puede inferir
        """
        if objetivo in self.hechos:
            return self.hechos[objetivo].certeza
            
        # Buscar reglas que concluyan el objetivo
        reglas_aplicables = [
            r for r in self.reglas.values() 
            if r.consecuente == objetivo
        ]
        
        if not reglas_aplicables:
            return None
            
        certezas = []
        
        for regla in reglas_aplicables:
            # Calcular certeza de los antecedentes
            certeza_antecedentes = self._calcular_certeza_antecedentes(regla)
            if certeza_antecedentes is not None:
                # Aplicar factor de certeza de la regla
                if regla.tipo == TipoIncertidumbre.FACTOR_CERTEZA:
                    certeza_consecuente = certeza_antecedentes * regla.factor_certeza
                else:
                    certeza_consecuente = certeza_antecedentes * regla.factor_certeza
                certezas.append(certeza_consecuente)
        
        if not certezas:
            return None
            
        # Combinar las certezas de todas las reglas aplicables
        if reglas_aplicables[0].tipo == TipoIncertidumbre.FACTOR_CERTEZA:
            # Combinación MYCIN de factores de certeza
            certeza_final = 0
            for c in certezas:
                if certeza_final >= 0 and c >= 0:
                    certeza_final += c * (1 - certeza_final)
                elif certeza_final < 0 and c < 0:
                    certeza_final += c * (1 + certeza_final)
                else:
                    certeza_final = (certeza_final + c) / (1 - min(abs(certeza_final), abs(c)))
        else:
            # Para otros modelos, tomar el máximo
            certeza_final = max(certezas)
        
        # Guardar el nuevo hecho inferido
        self.agregar_hecho(HechoIncertidumbre(
            contenido=objetivo,
            certeza=certeza_final,
            tipo=reglas_aplicables[0].tipo,
            fuente=f"Inferido por {len(reglas_aplicables)} reglas"
        ))
        
        return certeza_final
    
    def _calcular_certeza_antecedentes(self, regla: ReglaIncertidumbre) -> Optional[float]:
        """
        Calcula la certeza combinada de los antecedentes de una regla
        
        Args:
            regla (ReglaIncertidumbre): Regla a evaluar
            
        Returns:
            Optional[float]: Certeza combinada o None si algún antecedente es desconocido
        """
        certezas = []
        
        for premisa, peso in regla.antecedentes:
            if premisa not in self.hechos:
                return None
                
            hecho = self.hechos[premisa]
            certeza_premisa = hecho.certeza * peso
            
            # Para factores de certeza, ajustar rango
            if hecho.tipo == TipoIncertidumbre.FACTOR_CERTEZA:
                certeza_premisa = max(-1, min(1, certeza_premisa))
            else:
                certeza_premisa = max(0, min(1, certeza_premisa))
                
            certezas.append(certeza_premisa)
        
        # Calcular combinación según tipo de regla
        if regla.tipo == TipoIncertidumbre.FACTOR_CERTEZA:
            # Para MYCIN, tomar el mínimo de los antecedentes
            return min(certezas) if certezas else 0
        else:
            # Para otros modelos, tomar el producto
            return math.prod(certezas) if certezas else 0
    
    def mostrar_estado(self) -> Dict:
        """
        Muestra el estado actual del sistema
        
        Returns:
            Dict: Diccionario con el estado del sistema
        """
        return {
            "total_hechos": len(self.hechos),
            "hechos_positivos": sum(1 for h in self.hechos.values() if h.certeza > 0),
            "hechos_negativos": sum(1 for h in self.hechos.values() if h.certeza < 0),
            "total_reglas": len(self.reglas),
            "ultimas_operaciones": self.historial[-5:] if self.historial else []
        }

def ejemplo_mycin():
    """
    Demuestra el sistema con el clásico modelo de factores de certeza de MYCIN
    para diagnóstico médico.
    """
    sistema = SistemaIncertidumbre()
    
    # 1. Añadir hechos iniciales (síntomas y datos del paciente)
    sistema.agregar_hecho(HechoIncertidumbre(
        contenido="Fiebre alta",
        certeza=0.8,
        tipo=TipoIncertidumbre.FACTOR_CERTEZA,
        fuente="Observación médica"
    ))
    
    sistema.agregar_hecho(HechoIncertidumbre(
        contenido="Dolor de cabeza",
        certeza=0.6,
        tipo=TipoIncertidumbre.FACTOR_CERTEZA,
        fuente="Reporte paciente"
    ))
    
    # 2. Añadir reglas de diagnóstico (simplificadas)
    sistema.agregar_regla(ReglaIncertidumbre(
        nombre="R1",
        antecedentes=[("Fiebre alta", 0.9), ("Dolor de cabeza", 0.7)],
        consecuente="Gripe",
        factor_certeza=0.8,
        tipo=TipoIncertidumbre.FACTOR_CERTEZA
    ))
    
    sistema.agregar_regla(ReglaIncertidumbre(
        nombre="R2",
        antecedentes=[("Fiebre alta", 1.0), ("Dolor de cabeza", 0.3)],
        consecuente="Sinusitis",
        factor_certeza=0.6,
        tipo=TipoIncertidumbre.FACTOR_CERTEZA
    ))
    
    # 3. Realizar inferencia
    print("\n=== DIAGNÓSTICO MÉDICO CON FACTORES DE CERTEZA ===")
    print("\nInferiendo diagnóstico de Gripe...")
    certeza_gripe = sistema.inferir("Gripe")
    print(f"Certeza de Gripe: {certeza_gripe:.2f}")
    
    print("\nInferiendo diagnóstico de Sinusitis...")
    certeza_sinusitis = sistema.inferir("Sinusitis")
    print(f"Certeza de Sinusitis: {certeza_sinusitis:.2f}")
    
    # 4. Mostrar estado del sistema
    print("\nEstado del sistema:")
    for k, v in sistema.mostrar_estado().items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    ejemplo_mycin()