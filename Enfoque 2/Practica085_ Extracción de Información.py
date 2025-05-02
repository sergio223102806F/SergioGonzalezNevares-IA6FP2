# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 13:43:57 2025

@author: elvin
"""

"""
Script de Extracción de Información con Comentarios Línea por Línea

Este código implementa un sistema completo de extracción de información que:
1. Conecta a una fuente de datos (API y base de datos)
2. Procesa y limpia los datos
3. Extrae información relevante
4. Almacena los resultados
5. Genera reportes
"""

# Importación de librerías necesarias
import requests  # Para hacer peticiones HTTP a APIs
import sqlite3  # Para interactuar con bases de datos SQLite
import pandas as pd  # Para manipulación y análisis de datos
from bs4 import BeautifulSoup  # Para parsear HTML (en caso de extraer de páginas web)
import re  # Para expresiones regulares
import json  # Para manejar datos en formato JSON
from datetime import datetime  # Para manejo de fechas

# Configuración de constantes
API_URL = "https://api.example.com/data"  # URL de la API de donde extraeremos datos
DB_NAME = "extracted_data.db"  # Nombre de la base de datos local
TABLE_NAME = "extracted_info"  # Nombre de la tabla donde almacenaremos los datos
MAX_RETRIES = 3  # Número máximo de reintentos para conexiones fallidas

class InformationExtractor:
    def __init__(self):
        """
        Constructor de la clase InformationExtractor.
        Inicializa las conexiones y variables necesarias.
        """
        self.session = requests.Session()  # Sesión HTTP para conexiones persistentes
        self.conn = None  # Conexión a la base de datos (se inicializa luego)
        self.initialize_database()  # Prepara la base de datos local

    def initialize_database(self):
        """
        Inicializa la base de datos SQLite y crea la tabla si no existe.
        """
        try:
            # Establece conexión con la base de datos
            self.conn = sqlite3.connect(DB_NAME)
            cursor = self.conn.cursor()
            
            # Crea tabla si no existe con campos relevantes
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                extracted_data TEXT NOT NULL,
                category TEXT,
                confidence REAL,
                extraction_date TEXT NOT NULL,
                processed BOOLEAN DEFAULT 0
            )
            """)
            self.conn.commit()  # Guarda los cambios
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")
            raise

    def fetch_data_from_api(self, endpoint, params=None):
        """
        Obtiene datos de una API REST.
        
        Args:
            endpoint (str): URL del endpoint de la API
            params (dict): Parámetros para la consulta (opcional)
            
        Returns:
            dict: Datos en formato JSON o None si falla
        """
        retries = 0
        while retries < MAX_RETRIES:
            try:
                # Realiza la petición GET a la API
                response = self.session.get(
                    endpoint,
                    params=params,
                    timeout=10  # Timeout de 10 segundos
                )
                
                # Verifica si la respuesta fue exitosa (código 200)
                response.raise_for_status()
                
                # Retorna los datos parseados como JSON
                return response.json()
                
            except requests.exceptions.RequestException as e:
                print(f"Intento {retries + 1} fallido: {e}")
                retries += 1
                if retries == MAX_RETRIES:
                    print(f"Error: No se pudo conectar a {endpoint} después de {MAX_RETRIES} intentos")
                    return None

    def extract_from_html(self, html_content):
        """
        Extrae información de contenido HTML usando BeautifulSoup.
        
        Args:
            html_content (str): Contenido HTML a analizar
            
        Returns:
            dict: Datos estructurados extraídos
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')  # Parsea el HTML
            
            # Diccionario para almacenar los datos extraídos
            extracted_data = {
                'titulo': None,
                'fecha': None,
                'autor': None,
                'contenido': []
            }
            
            # Extrae el título de la página (etiqueta <title> o <h1>)
            title_tag = soup.find('title')
            extracted_data['titulo'] = title_tag.get_text().strip() if title_tag else None
            
            # Busca el autor usando expresiones regulares
            author_pattern = re.compile(r'autor|writer|by', re.IGNORECASE)
            author_tag = soup.find(string=author_pattern)
            extracted_data['autor'] = author_tag.strip() if author_tag else None
            
            # Extrae el contenido principal (párrafos)
            paragraphs = soup.find_all('p')
            extracted_data['contenido'] = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
            
            return extracted_data
            
        except Exception as e:
            print(f"Error al extraer de HTML: {e}")
            return None

    def clean_text(self, text):
        """
        Limpia y normaliza texto eliminando caracteres no deseados.
        
        Args:
            text (str): Texto a limpiar
            
        Returns:
            str: Texto limpio o None si el input no es válido
        """
        if not text or not isinstance(text, str):
            return None
            
        try:
            # Elimina espacios extraños, saltos de línea y tabulaciones
            text = ' '.join(text.split())
            
            # Elimina caracteres especiales excepto letras, números y signos básicos
            text = re.sub(r'[^\w\s.,;:¿?¡!-]', '', text, flags=re.UNICODE)
            
            return text.strip()
        except Exception as e:
            print(f"Error al limpiar texto: {e}")
            return None

    def process_and_extract(self, raw_data, source_type='api'):
        """
        Procesa datos crudos y extrae información estructurada.
        
        Args:
            raw_data: Datos crudos a procesar (dict, str o list)
            source_type (str): Tipo de fuente ('api', 'html', 'db')
            
        Returns:
            dict: Datos estructurados extraídos o None si falla
        """
        if not raw_data:
            print("Error: Datos de entrada vacíos")
            return None
            
        try:
            extracted = {}
            
            # Procesamiento según el tipo de fuente
            if source_type == 'api':
                # Extrae campos relevantes de datos API
                extracted['titulo'] = self.clean_text(raw_data.get('title'))
                extracted['descripcion'] = self.clean_text(raw_data.get('description'))
                extracted['fecha'] = raw_data.get('date')
                extracted['id'] = raw_data.get('id')
                
            elif source_type == 'html':
                # Extrae de contenido HTML
                extracted = self.extract_from_html(raw_data)
                
            elif source_type == 'db':
                # Procesa datos de base de datos
                if isinstance(raw_data, dict):
                    extracted = {k: self.clean_text(v) for k, v in raw_data.items()}
                else:
                    print("Error: Formato no soportado para tipo 'db'")
                    return None
                    
            else:
                print(f"Error: Tipo de fuente no soportado: {source_type}")
                return None
                
            # Añade metadatos de la extracción
            extracted['fuente'] = source_type
            extracted['fecha_procesamiento'] = datetime.now().isoformat()
            
            return extracted
            
        except Exception as e:
            print(f"Error al procesar datos: {e}")
            return None

    def store_extracted_data(self, data, category=None, confidence=0.0):
        """
        Almacena datos extraídos en la base de datos local.
        
        Args:
            data (dict): Datos a almacenar
            category (str): Categoría de los datos (opcional)
            confidence (float): Nivel de confianza de la extracción (0-1)
            
        Returns:
            bool: True si se almacenó correctamente, False si falló
        """
        if not data or not isinstance(data, dict):
            print("Error: Datos inválidos para almacenar")
            return False
            
        try:
            cursor = self.conn.cursor()
            
            # Prepara los datos para inserción
            data_json = json.dumps(data, ensure_ascii=False)
            current_date = datetime.now().isoformat()
            
            # Inserta los datos en la base de datos
            cursor.execute(
                f"""
                INSERT INTO {TABLE_NAME} 
                (source, extracted_data, category, confidence, extraction_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (data.get('fuente', 'unknown'), data_json, category, confidence, current_date)
            )
            
            self.conn.commit()  # Guarda los cambios
            return True
            
        except sqlite3.Error as e:
            print(f"Error al almacenar datos: {e}")
            self.conn.rollback()  # Revierte cambios en caso de error
            return False
        except Exception as e:
            print(f"Error inesperado al almacenar: {e}")
            return False

    def generate_report(self, output_format='csv', filename='extraction_report'):
        """
        Genera un reporte de los datos extraídos.
        
        Args:
            output_format (str): Formato del reporte ('csv', 'excel', 'json')
            filename (str): Nombre base del archivo de salida
            
        Returns:
            bool: True si se generó correctamente, False si falló
        """
        try:
            # Obtiene todos los datos no procesados de la base de datos
            query = f"SELECT * FROM {TABLE_NAME} WHERE processed = 0"
            df = pd.read_sql(query, self.conn)
            
            if df.empty:
                print("No hay nuevos datos para reportar")
                return False
                
            # Prepara el nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{filename}_{timestamp}.{output_format}"
            
            # Genera el reporte en el formato solicitado
            if output_format == 'csv':
                df.to_csv(output_file, index=False, encoding='utf-8-sig')
            elif output_format == 'excel':
                df.to_excel(output_file, index=False)
            elif output_format == 'json':
                df.to_json(output_file, orient='records', force_ascii=False)
            else:
                print(f"Formato no soportado: {output_format}")
                return False
                
            # Marca los datos como procesados
            ids = df['id'].tolist()
            update_query = f"""
            UPDATE {TABLE_NAME} 
            SET processed = 1 
            WHERE id IN ({','.join(map(str, ids))})
            """
            self.conn.execute(update_query)
            self.conn.commit()
            
            print(f"Reporte generado exitosamente: {output_file}")
            return True
            
        except Exception as e:
            print(f"Error al generar reporte: {e}")
            return False

    def close(self):
        """Cierra todas las conexiones y libera recursos."""
        try:
            if self.conn:
                self.conn.close()
            self.session.close()
        except Exception as e:
            print(f"Error al cerrar conexiones: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    print("Iniciando proceso de extracción de información...")
    
    # 1. Inicializar el extractor
    extractor = InformationExtractor()
    
    try:
        # 2. Extraer datos de API de ejemplo
        print("\nExtrayendo datos de API...")
        api_data = extractor.fetch_data_from_api(API_URL)
        
        if api_data:
            # 3. Procesar datos API
            processed_api = extractor.process_and_extract(api_data, 'api')
            
            if processed_api:
                # 4. Almacenar datos procesados
                extractor.store_extracted_data(
                    processed_api, 
                    category="api_data", 
                    confidence=0.9
                )
                print("Datos de API almacenados correctamente")
        
        # 5. Generar reporte CSV
        print("\nGenerando reporte...")
        extractor.generate_report('csv', 'api_extraction_report')
        
    except Exception as e:
        print(f"Error en el proceso principal: {e}")
    finally:
        # 6. Cerrar conexiones
        extractor.close()
        print("\nProceso completado. Recursos liberados.")