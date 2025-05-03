# -*- coding: utf-8 -*-


# Importaciones necesarias
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum, auto
from dataclasses import dataclass
import sys

class TipoRegla(Enum):
    """Tipos de reglas en el sistema experto"""
    HECHO = auto()        # Regla que define un hecho directo
    INFERENCIA = auto()   # Regla que infiere nuevos hechos
    ACCION = auto()       # Regla que ejecuta una acción

class ModoInferencia(Enum):
    """Modos de inferencia disponibles"""
    HACIA_ADELANTE = auto()  # Encadenamiento hacia adelante
    HACIA_ATRAS = auto()     # Encadenamiento hacia atrás

@dataclass
class ReglaExperta:
    """Estructura para representar reglas expertas"""
    id: str                     # Identificador único de la regla
    tipo: TipoRegla             # Tipo de regla
    antecedentes: List[str]     # Premisas de la regla
    consecuente: str            # Conclusión o acción
    explicacion: str            # Explicación de la regla
    certeza: float = 1.0        # Grado de certeza [0, 1]

@dataclass
class Hecho:
    """Representa un hecho en la base de conocimientos"""
    contenido: str             # Enunciado del hecho
    certeza: float             # Grado de certeza [0, 1]
    fuente: str                # Cómo se obtuvo este hecho
    explicacion: str           # Justificación del hecho

class SistemaExperto:
    """
    Implementación de un sistema experto con:
    - Base de conocimientos (reglas + hechos)
    - Motor de inferencia
    - Subsistema de explicación
    """
    
    def __init__(self, nombre: str, dominio: str):
        """
        Inicializa el sistema experto
        
        Args:
            nombre (str): Nombre del sistema experto
            dominio (str): Ámbito de conocimiento
        """
        self.nombre = nombre
        self.dominio = dominio
        self.base_reglas: Dict[str, ReglaExperta] = {}  # Todas las reglas
        self.base_hechos: Dict[str, Hecho] = {}        # Hechos conocidos
        self.agenda: List[str] = []                    # Reglas listas para ejecutar
        self.historial: List[Tuple[str, str]] = []     # Historial de inferencias
        self.modo_inferencia = ModoInferencia.HACIA_ADELANTE  # Modo por defecto
    
    def agregar_regla(self, regla: ReglaExperta) -> bool:
        """
        Añade una nueva regla a la base de conocimientos
        
        Args:
            regla (ReglaExperta): Regla a añadir
            
        Returns:
            bool: True si se añadió correctamente
        """
        if regla.id in self.base_reglas:
            return False
            
        self.base_reglas[regla.id] = regla
        return True
    
    def agregar_hecho(self, hecho: Hecho) -> bool:
        """
        Añade un hecho a la base de conocimientos y actualiza la agenda
        
        Args:
            hecho (Hecho): Hecho a añadir
            
        Returns:
            bool: True si se añadió correctamente
        """
        if hecho.contenido in self.base_hechos:
            # Actualizar certeza si el hecho ya existe
            existente = self.base_hechos[hecho.contenido]
            nueva_certeza = max(existente.certeza, hecho.certeza)
            self.base_hechos[hecho.contenido].certeza = nueva_certeza
            self.historial.append(("Actualizado hecho", f"{hecho.contenido} ({nueva_certeza:.2f})"))
        else:
            self.base_hechos[hecho.contenido] = hecho
            self.historial.append(("Añadido hecho", hecho.contenido))
        
        # Actualizar agenda para encadenamiento hacia adelante
        if self.modo_inferencia == ModoInferencia.HACIA_ADELANTE:
            self._actualizar_agenda(hecho.contenido)
            
        return True
    
    def _actualizar_agenda(self, hecho: str):
        """
        Actualiza la agenda de reglas activables basado en un nuevo hecho
        
        Args:
            hecho (str): Hecho que puede activar reglas
        """
        for regla_id, regla in self.base_reglas.items():
            if regla.tipo == TipoRegla.INFERENCIA and hecho in regla.antecedentes:
                if regla_id not in self.agenda:
                    self.agenda.append(regla_id)
    
    def establecer_modo_inferencia(self, modo: ModoInferencia):
        """
        Establece el modo de inferencia del sistema
        
        Args:
            modo (ModoInferencia): Modo de inferencia a usar
        """
        self.modo_inferencia = modo
        self.historial.append(("Cambio modo", modo.name))
    
    def ejecutar(self, objetivo: Optional[str] = None) -> bool:
        """
        Ejecuta el sistema experto según el modo de inferencia
        
        Args:
            objetivo (Optional[str]): Para encadenamiento hacia atrás, el hecho objetivo
            
        Returns:
            bool: True si se alcanzó una conclusión satisfactoria
        """
        if self.modo_inferencia == ModoInferencia.HACIA_ADELANTE:
            return self._encadenamiento_adelante()
        else:
            if objetivo is None:
                return False
            return self._encadenamiento_atras(objetivo)
    
    def _encadenamiento_adelante(self) -> bool:
        """
        Realiza encadenamiento hacia adelante hasta que no hay más reglas activables
        
        Returns:
            bool: True si se infirieron nuevos hechos
        """
        cambios = False
        
        while self.agenda:
            regla_id = self.agenda.pop(0)
            regla = self.base_reglas[regla_id]
            
            # Verificar si todos los antecedentes se cumplen
            if all(ant in self.base_hechos for ant in regla.antecedentes):
                # Calcular certeza mínima de los antecedentes
                certeza = min(
                    self.base_hechos[ant].certeza 
                    for ant in regla.antecedentes
                ) * regla.certeza
                
                # Crear nuevo hecho inferido
                nuevo_hecho = Hecho(
                    contenido=regla.consecuente,
                    certeza=certeza,
                    fuente=f"Inferido por {regla_id}",
                    explicacion=regla.explicacion
                )
                
                self.agregar_hecho(nuevo_hecho)
                cambios = True
                
        return cambios
    
    def _encadenamiento_atras(self, objetivo: str) -> bool:
        """
        Realiza encadenamiento hacia atrás para probar un objetivo específico
        
        Args:
            objetivo (str): Hecho objetivo a probar
            
        Returns:
            bool: True si el objetivo puede ser probado
        """
        # Si el objetivo ya está en los hechos
        if objetivo in self.base_hechos:
            return True
            
        # Buscar reglas que concluyan este objetivo
        reglas_aplicables = [
            r for r in self.base_reglas.values() 
            if r.consecuente == objetivo and r.tipo == TipoRegla.INFERENCIA
        ]
        
        for regla in reglas_aplicables:
            # Intentar probar todos los antecedentes
            if all(self._encadenamiento_atras(ant) for ant in regla.antecedentes):
                # Calcular certeza
                certeza = min(
                    self.base_hechos[ant].certeza 
                    for ant in regla.antecedentes
                ) * regla.certeza
                
                # Añadir nuevo hecho
                self.agregar_hecho(Hecho(
                    contenido=objetivo,
                    certeza=certeza,
                    fuente=f"Probado por {regla.id}",
                    explicacion=regla.explicacion
                ))
                return True
                
        return False
    
    def explicar(self, hecho: str) -> List[str]:
        """
        Genera una explicación de cómo se obtuvo un hecho
        
        Args:
            hecho (str): Hecho a explicar
            
        Returns:
            List[str]: Lista de pasos de la explicación
        """
        explicacion = []
        
        if hecho not in self.base_hechos:
            return ["El hecho no está en la base de conocimientos"]
            
        hecho_obj = self.base_hechos[hecho]
        explicacion.append(f"Hecho: {hecho_obj.contenido}")
        explicacion.append(f"Certeza: {hecho_obj.certeza:.2f}")
        explicacion.append(f"Fuente: {hecho_obj.fuente}")
        explicacion.append(f"Explicación: {hecho_obj.explicacion}")
        
        # Si fue inferido, mostrar la regla y sus antecedentes
        if "Inferido por" in hecho_obj.fuente or "Probado por" in hecho_obj.fuente:
            regla_id = hecho_obj.fuente.split()[-1]
            if regla_id in self.base_reglas:
                regla = self.base_reglas[regla_id]
                explicacion.append("\nRegla aplicada:")
                explicacion.append(f"ID: {regla.id}")
                explicacion.append(f"Tipo: {regla.tipo.name}")
                explicacion.append(f"Antecedentes: {', '.join(regla.antecedentes)}")
                explicacion.append(f"Consecuente: {regla.consecuente}")
                explicacion.append(f"Explicación regla: {regla.explicacion}")
                
                # Explicar antecedentes
                explicacion.append("\nExplicación de antecedentes:")
                for ant in regla.antecedentes:
                    explicacion.extend(self.explicar(ant))
                    explicacion.append("---")
                
        return explicacion
    
    def interfaz_usuario(self):
        """Interfaz de usuario simple para interactuar con el sistema experto"""
        print(f"\n=== Sistema Experto: {self.nombre} ===")
        print(f"Dominio: {self.dominio}")
        print("\nOpciones:")
        print("1. Añadir hecho manualmente")
        print("2. Establecer modo de inferencia")
        print("3. Ejecutar sistema")
        print("4. Consultar hecho")
        print("5. Explicar hecho")
        print("6. Mostrar estado")
        print("7. Salir")
        
        while True:
            opcion = input("\nSeleccione una opción (1-7): ")
            
            if opcion == "1":
                contenido = input("Contenido del hecho: ")
                certeza = float(input("Certeza (0-1): "))
                fuente = input("Fuente del hecho: ")
                explicacion = input("Explicación: ")
                
                self.agregar_hecho(Hecho(
                    contenido=contenido,
                    certeza=certeza,
                    fuente=fuente,
                    explicacion=explicacion
                ))
                print("Hecho añadido correctamente.")
                
            elif opcion == "2":
                print("\nModos de inferencia:")
                print("1. Encadenamiento hacia adelante")
                print("2. Encadenamiento hacia atrás")
                modo = input("Seleccione modo (1-2): ")
                
                if modo == "1":
                    self.establecer_modo_inferencia(ModoInferencia.HACIA_ADELANTE)
                else:
                    self.establecer_modo_inferencia(ModoInferencia.HACIA_ATRAS)
                print(f"Modo establecido a: {self.modo_inferencia.name}")
                
            elif opcion == "3":
                if self.modo_inferencia == ModoInferencia.HACIA_ADELANTE:
                    cambios = self._encadenamiento_adelante()
                    print(f"Encadenamiento completado. {'Se inferieron nuevos hechos.' if cambios else 'Sin cambios.'}")
                else:
                    objetivo = input("Ingrese el hecho objetivo a probar: ")
                    resultado = self._encadenamiento_atras(objetivo)
                    print(f"El objetivo {'se pudo probar' if resultado else 'no se pudo probar'}")
                    
            elif opcion == "4":
                hecho = input("Hecho a consultar: ")
                if hecho in self.base_hechos:
                    print(f"Certeza: {self.base_hechos[hecho].certeza:.2f}")
                else:
                    print("Hecho desconocido.")
                    
            elif opcion == "5":
                hecho = input("Hecho a explicar: ")
                for linea in self.explicar(hecho):
                    print(linea)
                    
            elif opcion == "6":
                print("\nEstado del sistema:")
                print(f"Total reglas: {len(self.base_reglas)}")
                print(f"Total hechos: {len(self.base_hechos)}")
                print(f"Modo inferencia: {self.modo_inferencia.name}")
                print("\nÚltimas 5 acciones:")
                for accion, detalle in self.historial[-5:]:
                    print(f"- {accion}: {detalle}")
                    
            elif opcion == "7":
                print("Saliendo del sistema experto...")
                sys.exit()
                
            else:
                print("Opción no válida. Intente de nuevo.")

def sistema_experto_medico():
    """
    Configura y devuelve un sistema experto médico de ejemplo
    para diagnóstico de enfermedades comunes.
    """
    sistema = SistemaExperto(
        nombre="MED-IA Diagnóstico",
        dominio="Diagnóstico médico de enfermedades comunes"
    )
    
    # 1. Añadir reglas de diagnóstico
    sistema.agregar_regla(ReglaExperta(
        id="R1",
        tipo=TipoRegla.INFERENCIA,
        antecedentes=["Fiebre", "Dolor de cabeza", "Dolor muscular"],
        consecuente="Posible gripe",
        explicacion="La combinación de fiebre con dolores de cabeza y musculares sugiere gripe",
        certeza=0.8
    ))
    
    sistema.agregar_regla(ReglaExperta(
        id="R2",
        tipo=TipoRegla.INFERENCIA,
        antecedentes=["Fiebre alta", "Erupción cutánea"],
        consecuente="Posible varicela",
        explicacion="Fiebre alta con erupción es síntoma común de varicela",
        certeza=0.9
    ))
    
    sistema.agregar_regla(ReglaExperta(
        id="R3",
        tipo=TipoRegla.INFERENCIA,
        antecedentes=["Dolor de garganta", "Fiebre", "Inflamación de amígdalas"],
        consecuente="Posible amigdalitis",
        explicacion="Dolor de garganta con fiebre e inflamación sugiere amigdalitis",
        certeza=0.85
    ))
    
    sistema.agregar_regla(ReglaExperta(
        id="R4",
        tipo=TipoRegla.INFERENCIA,
        antecedentes=["Posible gripe", "Duración > 2 semanas"],
        consecuente="Posible neumonía",
        explicacion="Gripe prolongada puede derivar en neumonía",
        certeza=0.7
    ))
    
    # 2. Añadir algunos hechos iniciales
    sistema.agregar_hecho(Hecho(
        contenido="Fiebre",
        certeza=0.9,
        fuente="Termómetro",
        explicacion="Temperatura medida: 38.5°C"
    ))
    
    sistema.agregar_hecho(Hecho(
        contenido="Dolor de cabeza",
        certeza=0.8,
        fuente="Reporte paciente",
        explicacion="Paciente reporta dolor de cabeza intenso"
    ))
    
    return sistema

if __name__ == "__main__":
    # Crear y ejecutar sistema experto médico
    sistema_medico = sistema_experto_medico()
    
    # Ejecutar en modo interactivo
    print("\n=== SISTEMA EXPERTO MÉDICO ===")
    print("Configuración inicial completada.")
    print(f"Reglas cargadas: {len(sistema_medico.base_reglas)}")
    print(f"Hechos iniciales: {len(sistema_medico.base_hechos)}")
    
    # Ejecutar encadenamiento hacia adelante
    sistema_medico.establecer_modo_inferencia(ModoInferencia.HACIA_ADELANTE)
    sistema_medico.ejecutar()
    
    # Mostrar posibles diagnósticos
    print("\nPosibles diagnósticos inferidos:")
    for hecho, obj in sistema_medico.base_hechos.items():
        if hecho.startswith("Posible"):
            print(f"- {hecho} (Certeza: {obj.certeza:.2f})")
    
    # Explicar un diagnóstico
    print("\nExplicación para 'Posible gripe':")
    for linea in sistema_medico.explicar("Posible gripe"):
        print(linea)
    
    # Opcional: Ejecutar interfaz de usuario interactiva
    # sistema_medico.interfaz_usuario()