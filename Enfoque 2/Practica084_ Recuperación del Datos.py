# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 18:47:37 2025

@author: elvin
"""

"""
Implementación de una Gramática Probabilística Independiente del Contexto (PCFG)
con capacidad de recuperación de datos desde una base de datos SQLite.

Esta clase permite:
- Almacenar producciones gramaticales en una base de datos
- Recuperar producciones eficientemente
- Generar oraciones basadas en probabilidades
- Registrar estadísticas de uso
- Normalizar automáticamente las probabilidades
"""

# Importaciones necesarias
import sqlite3  # Para interactuar con la base de datos SQLite
import random   # Para selección aleatoria basada en probabilidades
import json     # Para serializar/deserializar las producciones
from collections import defaultdict  # Para el caché en memoria

class PCFG_DataBacked:
    def __init__(self, db_name='grammar.db'):
        """
        Constructor de la clase.
        
        Args:
            db_name (str): Nombre del archivo de base de datos (por defecto 'grammar.db')
        """
        self.db_name = db_name  # Nombre del archivo de base de datos
        self.conn = None        # Conexión a la base de datos (se inicializa más tarde)
        # Caché en memoria para producciones (defaultdict crea listas automáticamente)
        self.productions_cache = defaultdict(list)
        self.start_symbol = None  # Símbolo inicial de la gramática
        self._initialize_database()  # Inicializa la estructura de la base de datos

    def _initialize_database(self):
        """Crea las tablas necesarias en la base de datos si no existen"""
        with self._get_connection() as conn:  # Obtiene una conexión
            # Crea tabla de producciones si no existe
            conn.execute("""
            CREATE TABLE IF NOT EXISTS productions (
                lhs TEXT NOT NULL,         # Símbolo izquierdo (non-terminal)
                rhs TEXT NOT NULL,          # Lado derecho (serializado como JSON)
                probability REAL NOT NULL,  # Probabilidad de la producción
                usage_count INTEGER DEFAULT 0,  # Contador de usos
                PRIMARY KEY (lhs, rhs)      # Clave primaria compuesta
            )""")
            # Crea tabla para metadatos de la gramática
            conn.execute("""
            CREATE TABLE IF NOT EXISTS grammar_metadata (
                key TEXT PRIMARY KEY,  # Clave del metadato
                value TEXT             # Valor del metadato
            )""")

    def _get_connection(self):
        """Obtiene una conexión a la base de datos (la crea si no existe)"""
        if self.conn is None:  # Si no hay conexión establecida
            self.conn = sqlite3.connect(self.db_name)  # Conecta a la base de datos
        return self.conn  # Retorna la conexión

    def add_production(self, lhs, rhs, probability):
        """
        Añade una producción a la gramática y base de datos.
        
        Args:
            lhs (str): Símbolo no terminal del lado izquierdo
            rhs (list): Lista de símbolos del lado derecho
            probability (float): Probabilidad de la producción (0-1)
        """
        # Validación de tipos
        if not isinstance(rhs, list):
            raise ValueError("El lado derecho debe ser una lista")
        # Validación de rango de probabilidad
        if not (0 <= probability <= 1):
            raise ValueError("La probabilidad debe estar entre 0 y 1")

        # Serializa el lado derecho a JSON para almacenar en DB
        rhs_serialized = json.dumps(rhs)
        
        with self._get_connection() as conn:  # Obtiene conexión
            try:
                # Intenta insertar la nueva producción
                conn.execute(
                    "INSERT INTO productions (lhs, rhs, probability) VALUES (?, ?, ?)",
                    (lhs, rhs_serialized, probability)
                )
            except sqlite3.IntegrityError:
                # Si ya existe, actualiza su probabilidad
                conn.execute(
                    "UPDATE productions SET probability = ? WHERE lhs = ? AND rhs = ?",
                    (probability, lhs, rhs_serialized)
                )
        
        # Actualiza el caché en memoria
        self.productions_cache[lhs].append((rhs, probability))
        
        # Si es la primera producción, establece como símbolo inicial
        if self.start_symbol is None:
            self.start_symbol = lhs
            self._set_metadata('start_symbol', lhs)  # Guarda en metadatos

    def _set_metadata(self, key, value):
        """
        Almacena metadatos en la base de datos.
        
        Args:
            key (str): Nombre del metadato
            value (str): Valor a almacenar
        """
        with self._get_connection() as conn:
            # Inserta o reemplaza el metadato
            conn.execute(
                "INSERT OR REPLACE INTO grammar_metadata (key, value) VALUES (?, ?)",
                (key, str(value))
            )

    def load_productions(self, lhs):
        """
        Carga producciones para un símbolo no terminal desde la base de datos.
        
        Args:
            lhs (str): Símbolo no terminal a buscar
            
        Returns:
            list: Lista de tuplas (rhs, probability)
        """
        # Primero verifica el caché en memoria
        if lhs in self.productions_cache:
            return self.productions_cache[lhs]
            
        with self._get_connection() as conn:
            # Consulta las producciones para el símbolo lhs
            cursor = conn.execute(
                "SELECT rhs, probability FROM productions WHERE lhs = ?", 
                (lhs,)
            )
            # Deserializa el JSON y crea lista de producciones
            productions = [
                (json.loads(rhs), prob) 
                for rhs, prob in cursor.fetchall()
            ]
            # Almacena en caché para futuras consultas
            self.productions_cache[lhs] = productions
            return productions

    def normalize_probabilities(self):
        """Normaliza las probabilidades para que sumen 1 para cada símbolo lhs"""
        with self._get_connection() as conn:
            # Obtiene todos los símbolos lhs distintos
            symbols = conn.execute(
                "SELECT DISTINCT lhs FROM productions"
            ).fetchall()
            
            for (lhs,) in symbols:
                # Calcula la suma total de probabilidades para este lhs
                total = conn.execute(
                    "SELECT SUM(probability) FROM productions WHERE lhs = ?",
                    (lhs,)
                ).fetchone()[0] or 0  # Usa 0 si es None
                
                if total > 0:
                    # Actualiza las probabilidades en la base de datos
                    conn.execute(
                        "UPDATE productions SET probability = probability / ? WHERE lhs = ?",
                        (total, lhs)
                    )
                    
                    # Actualiza el caché en memoria si existe
                    if lhs in self.productions_cache:
                        self.productions_cache[lhs] = [
                            (rhs, prob/total)
                            for rhs, prob in self.productions_cache[lhs]
                        ]

    def generate_sentence(self, symbol=None):
        """
        Genera una oración aleatoria según las probabilidades de la gramática.
        
        Args:
            symbol (str): Símbolo desde el que generar (None para símbolo inicial)
            
        Returns:
            str: Oración generada
        """
        if symbol is None:
            symbol = self.start_symbol
            if symbol is None:
                raise ValueError("No se ha definido un símbolo inicial")
        
        # Carga las producciones para este símbolo
        productions = self.load_productions(symbol)
        if not productions:
            return symbol  # Si no hay producciones, es un símbolo terminal
            
        # Selecciona una producción aleatoria basada en probabilidades
        rhs, prob = random.choices(
            productions,
            weights=[p for _, p in productions],  # Pesos basados en probabilidades
            k=1
        )[0]
        
        # Registra el uso de esta producción
        self._record_usage(symbol, rhs)
        
        # Genera recursivamente cada símbolo del lado derecho
        sentence = []
        for s in rhs:
            sentence.append(self.generate_sentence(s))
            
        # Une los componentes con espacios
        return ' '.join(sentence)

    def _record_usage(self, lhs, rhs):
        """
        Incrementa el contador de uso para una producción.
        
        Args:
            lhs (str): Símbolo izquierdo
            rhs (list): Lado derecho de la producción
        """
        rhs_serialized = json.dumps(rhs)
        with self._get_connection() as conn:
            # Incrementa el contador de usos
            conn.execute(
                "UPDATE productions SET usage_count = usage_count + 1 "
                "WHERE lhs = ? AND rhs = ?",
                (lhs, rhs_serialized)
            )

    def get_usage_stats(self):
        """
        Obtiene estadísticas de uso de producciones ordenadas por frecuencia.
        
        Returns:
            list: Lista de diccionarios con lhs, rhs y count
        """
        with self._get_connection() as conn:
            # Consulta las producciones más usadas
            cursor = conn.execute(
                "SELECT lhs, rhs, usage_count FROM productions "
                "ORDER BY usage_count DESC"
            )
            # Retorna lista de diccionarios con la información
            return [
                {'lhs': lhs, 'rhs': json.loads(rhs), 'count': count}
                for lhs, rhs, count in cursor.fetchall()
            ]

    def print_grammar(self):
        """Muestra la gramática con estadísticas de uso"""
        print("Gramática Probabilística con Recuperación de Datos")
        print(f"Símbolo inicial: {self.start_symbol}\n")
        
        # Obtiene y muestra las estadísticas de uso
        stats = self.get_usage_stats()
        for stat in stats:
            rhs_str = ' '.join(stat['rhs'])
            print(f"{stat['lhs']} -> {rhs_str} [usada {stat['count']} veces]")

# Ejemplo de uso principal
if __name__ == "__main__":
    # Crea una instancia de la gramática
    grammar = PCFG_DataBacked()
    
    # Añade producciones de ejemplo (gramática simple en español)
    grammar.add_production('S', ['NP', 'VP'], 1.0)  # Oración -> Frase nominal + verbal
    grammar.add_production('NP', ['Det', 'N'], 0.7)  # Frase nominal -> Det + Sustantivo
    grammar.add_production('NP', ['N'], 0.3)         # Frase nominal -> Solo sustantivo
    grammar.add_production('VP', ['V', 'NP'], 0.8)   # Frase verbal -> Verbo + Frase nominal
    grammar.add_production('VP', ['V'], 0.2)         # Frase verbal -> Solo verbo
    grammar.add_production('Det', ['el'], 0.6)       # Determinante
    grammar.add_production('Det', ['un'], 0.4)       # Determinante
    grammar.add_production('N', ['gato'], 0.4)       # Sustantivo
    grammar.add_production('N', ['perro'], 0.4)      # Sustantivo
    grammar.add_production('N', ['ratón'], 0.2)      # Sustantivo
    grammar.add_production('V', ['persigue'], 0.6)   # Verbo
    grammar.add_production('V', ['muerde'], 0.3)     # Verbo
    grammar.add_production('V', ['duerme'], 0.1)     # Verbo
    
    # Normaliza las probabilidades para que sumen 1
    grammar.normalize_probabilities()
    
    # Genera y muestra algunas oraciones de ejemplo
    print("Oraciones generadas:")
    for i in range(5):
        print(f"{i+1}. {grammar.generate_sentence().capitalize()}.")
    
    # Muestra estadísticas de uso
    print("\nEstadísticas de uso:")
    grammar.print_grammar()