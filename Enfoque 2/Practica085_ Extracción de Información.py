# -*- coding: utf-8 -*-                                                     # Define la codificación de caracteres del archivo como UTF-8
"""
Created on Sun Apr 27 13:43:57 2025                                         # Indica la fecha y hora de creación del archivo
                                                                           #
@author: elvin                                                              # Define el autor del archivo
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

class InformationExtractor:                                                  # Define una nueva clase llamada InformationExtractor
    def __init__(self):                                                     # Define el constructor de la clase InformationExtractor
        """
        Constructor de la clase InformationExtractor.                       # Documentación del constructor
        Inicializa las conexiones y variables necesarias.                  # Explica el propósito del constructor
        """
        self.session = requests.Session()  # Sesión HTTP para conexiones persistentes # Inicializa una sesión HTTP para mantener conexiones
        self.conn = None  # Conexión a la base de datos (se inicializa luego) # Inicializa la conexión a la base de datos como None
        self.initialize_database()  # Prepara la base de datos local       # Llama al método para inicializar la base de datos

    def initialize_database(self):                                         # Define el método para inicializar la base de datos
        """
        Inicializa la base de datos SQLite y crea la tabla si no existe.   # Documentación del método
        """
        try:                                                                # Inicia un bloque try para manejar posibles errores
            # Establece conexión con la base de datos                       # Comentario explicando la siguiente acción
            self.conn = sqlite3.connect(DB_NAME)                           # Establece la conexión a la base de datos SQLite
            cursor = self.conn.cursor()                                   # Crea un cursor para ejecutar comandos SQL

            # Crea tabla si no existe con campos relevantes                # Comentario explicando la siguiente acción
            cursor.execute(f"""                                          # Ejecuta un comando SQL formateado
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (               # Crea una tabla si no existe con el nombre definido
                    id INTEGER PRIMARY KEY AUTOINCREMENT,               # Define una columna 'id' como entero, clave primaria y autoincremental
                    source TEXT NOT NULL,                               # Define una columna 'source' como texto y no nula
                    extracted_data TEXT NOT NULL,                       # Define una columna 'extracted_data' como texto y no nula
                    category TEXT,                                      # Define una columna 'category' como texto (puede ser nula)
                    confidence REAL,                                    # Define una columna 'confidence' como número real
                    extraction_date TEXT NOT NULL,                      # Define una columna 'extraction_date' como texto y no nula
                    processed BOOLEAN DEFAULT 0                        # Define una columna 'processed' como booleano con valor predeterminado 0
                )
                """)
            self.conn.commit()  # Guarda los cambios                           # Guarda los cambios realizados en la base de datos
        except sqlite3.Error as e:                                         # Captura errores específicos de SQLite
            print(f"Error al inicializar la base de datos: {e}")          # Imprime un mensaje de error si la inicialización falla
            raise                                                           # Propaga la excepción para que se maneje en un nivel superior

    def fetch_data_from_api(self, endpoint, params=None):                  # Define el método para obtener datos de una API
        """
        Obtiene datos de una API REST.                                    # Documentación del método

        Args:                                                             # Documentación de los argumentos
            endpoint (str): URL del endpoint de la API                    # URL del punto final de la API
            params (dict): Parámetros para la consulta (opcional)          # Diccionario de parámetros para la solicitud (si es necesario)

        Returns:                                                          # Documentación del valor de retorno
            dict: Datos en formato JSON o None si falla                   # Datos de la API en formato JSON o None en caso de error
        """
        retries = 0                                                       # Inicializa el contador de reintentos
        while retries < MAX_RETRIES:                                      # Bucle que se ejecuta hasta alcanzar el número máximo de reintentos
            try:                                                          # Inicia un bloque try para manejar posibles errores de conexión
                # Realiza la petición GET a la API                           # Comentario explicando la siguiente acción
                response = self.session.get(                            # Realiza una petición GET a la URL especificada
                    endpoint,                                            # La URL del endpoint de la API
                    params=params,                                       # Los parámetros de la consulta (si se proporcionan)
                    timeout=10                                            # Establece un tiempo de espera de 10 segundos para la respuesta
                )

                # Verifica si la respuesta fue exitosa (código 200)         # Comentario explicando la siguiente acción
                response.raise_for_status()                               # Lanza una excepción para códigos de estado HTTP erróneos (no 200)

                # Retorna los datos parseados como JSON                     # Comentario explicando la siguiente acción
                return response.json()                                   # Parsea la respuesta de la API como JSON y la retorna

            except requests.exceptions.RequestException as e:             # Captura excepciones relacionadas con errores de la petición HTTP
                print(f"Intento {retries + 1} fallido: {e}")              # Imprime un mensaje de error indicando el número de intento y el error
                retries += 1                                              # Incrementa el contador de reintentos
                if retries == MAX_RETRIES:                                # Verifica si se ha alcanzado el número máximo de reintentos
                    print(f"Error: No se pudo conectar a {endpoint} después de {MAX_RETRIES} intentos") # Imprime un mensaje de error final
                    return None                                           # Retorna None si no se pudo conectar después de varios intentos

    def extract_from_html(self, html_content):                            # Define el método para extraer datos de HTML
        """
        Extrae información de contenido HTML usando BeautifulSoup.        # Documentación del método

        Args:                                                             # Documentación de los argumentos
            html_content (str): Contenido HTML a analizar                 # El contenido HTML del que se extraerán los datos

        Returns:                                                          # Documentación del valor de retorno
            dict: Datos estructurados extraídos                            # Un diccionario con los datos extraídos del HTML
        """
        try:                                                                # Inicia un bloque try para manejar posibles errores al parsear HTML
            soup = BeautifulSoup(html_content, 'html.parser')             # Crea un objeto BeautifulSoup para parsear el HTML

            # Diccionario para almacenar los datos extraídos                # Inicializa un diccionario para guardar los datos extraídos
            extracted_data = {
                'titulo': None,
                'fecha': None,
                'autor': None,
                'contenido': []
            }

            # Extrae el título de la página (etiqueta <title> o <h1>)     # Comentario explicando la siguiente acción
            title_tag = soup.find('title')                               # Busca la etiqueta <title> en el HTML
            extracted_data['titulo'] = title_tag.get_text().strip() if title_tag else None # Extrae el texto del título y elimina espacios, o None si no se encuentra

            # Busca el autor usando expresiones regulares                   # Comentario explicando la siguiente acción
            author_pattern = re.compile(r'autor|writer|by', re.IGNORECASE) # Compila una expresión regular para buscar palabras relacionadas con el autor
            author_tag = soup.find(string=author_pattern)                # Busca texto en el HTML que coincida con el patrón de autor
            extracted_data['autor'] = author_tag.strip() if author_tag else None # Extrae el texto del autor y elimina espacios, o None si no se encuentra

            # Extrae el contenido principal (párrafos)                     # Comentario explicando la siguiente acción
            paragraphs = soup.find_all('p')                               # Busca todas las etiquetas <p> (párrafos) en el HTML
            extracted_data['contenido'] = [p.get_text().strip() for p in paragraphs if p.get_text().strip()] # Extrae el texto de cada párrafo, elimina espacios y lo añade a la lista si no está vacío

            return extracted_data                                         # Retorna el diccionario con los datos extraídos

        except Exception as e:                                             # Captura cualquier excepción que ocurra durante la extracción de HTML
            print(f"Error al extraer de HTML: {e}")                      # Imprime un mensaje de error
            return None                                                   # Retorna None en caso de error

    def clean_text(self, text):                                           # Define el método para limpiar texto
        """
        Limpia y normaliza texto eliminando caracteres no deseados.       # Documentación del método

        Args:                                                             # Documentación de los argumentos
            text (str): Texto a limpiar                                   # El texto que se va a limpiar

        Returns:                                                          # Documentación del valor de retorno
            str: Texto limpio o None si el input no es válido             # El texto limpio o None si la entrada no es válida
        """
        if not text or not isinstance(text, str):                         # Verifica si el texto es None o no es una cadena
            return None                                                   # Retorna None si la entrada no es válida

        try:                                                                # Inicia un bloque try para manejar posibles errores al limpiar el texto
            # Elimina espacios extraños, saltos de línea y tabulaciones     # Comentario explicando la siguiente acción
            text = ' '.join(text.split())                                 # Divide el texto por espacios y luego lo une con un solo espacio

            # Elimina caracteres especiales excepto letras, números y signos básicos # Comentario explicando la siguiente acción
            text = re.sub(r'[^\w\s.,;:¿?¡!-]', '', text, flags=re.UNICODE) # Sustituye cualquier carácter que no sea alfanumérico, espacio, o los signos especificados con una cadena vacía

            return text.strip()                                           # Elimina los espacios en blanco al principio y al final del texto limpio
        except Exception as e:                                             # Captura cualquier excepción que ocurra durante la limpieza del texto
            print(f"Error al limpiar texto: {e}")                        # Imprime un mensaje de error
            return None                                                   # Retorna None en caso de error

    def process_and_extract(self, raw_data, source_type='api'):            # Define el método para procesar y extraer datos
        """
        Procesa datos crudos y extrae información estructurada.          # Documentación del método

        Args:                                                             # Documentación de los argumentos
            raw_data: Datos crudos a procesar (dict, str o list)          # Los datos sin procesar que se van a analizar
            source_type (str): Tipo de fuente ('api', 'html', 'db')       # El tipo de la fuente de datos (API, HTML, base de datos)

        Returns:                                                          # Documentación del valor de retorno
            dict: Datos estructurados extraídos o None si falla           # Un diccionario con los datos estructurados o None en caso de error
        """
        if not raw_data:                                                   # Verifica si los datos sin procesar están vacíos
            print("Error: Datos de entrada vacíos")                      # Imprime un mensaje de error si no hay datos
            return None                                                   # Retorna None si no hay datos

        try:                                                                # Inicia un bloque try para manejar posibles errores durante el procesamiento
            extracted = {}                                                # Inicializa un diccionario para almacenar los datos extraídos

            # Procesamiento según el tipo de fuente                       # Comentario explicando la siguiente acción
            if source_type == 'api':                                      # Si la fuente de datos es una API
                # Extrae campos relevantes de datos API                    # Comentario explicando la siguiente acción
                extracted['titulo'] = self.clean_text(raw_data.get('title')) # Obtiene el título, lo limpia y lo guarda
                extracted['descripcion'] = self.clean_text(raw_data.get('description')) # Obtiene la descripción, la limpia y la guarda
                extracted['fecha'] = raw_data.get('date')                   # Obtiene la fecha y la guarda
                extracted['id'] = raw_data.get('id')                       # Obtiene el ID y lo guarda

            elif source_type == 'html':                                   # Si la fuente de datos es HTML
                # Extrae de contenido HTML                                 # Comentario explicando la siguiente acción
                extracted = self.extract_from_html(raw_data)               # Llama al método para extraer datos del HTML

            elif source_type == 'db':                                     # Si la fuente de datos es una base de datos
                # Procesa datos de base de datos                           # Comentario explicando la siguiente acción
                if isinstance(raw_data, dict):                            # Verifica si los datos de la base de datos son un diccionario
                    extracted = {k: self.clean_text(v) for k, v in raw_data.items()} # Limpia cada valor del diccionario
                else:                                                     # Si el formato de los datos de la base de datos no es un diccionario
                    print("Error: Formato no soportado para tipo 'db'")    # Imprime un mensaje de error
                    return None                                           # Retorna None si el formato no es compatible

            else:                                                         # Si el tipo de fuente no es reconocido
                print(f"Error: Tipo de fuente no soportado: {source_type}") # Imprime un mensaje de error
                return None                                               # Retorna None si el tipo de fuente no es válido

            # Añade metadatos de la extracción                            # Comentario explicando la siguiente acción
            extracted['fuente'] = source_type                             # Guarda el tipo de fuente de los datos
            extracted['fecha_procesamiento'] = datetime.now().isoformat() # Guarda la fecha y hora del procesamiento en formato ISO

            return extracted                                                # Retorna el diccionario con los datos extraídos y procesados

        except Exception as e:                                             # Captura cualquier excepción que ocurra durante el procesamiento
            print(f"Error al procesar datos: {e}")                        # Imprime un mensaje de error
            return None                                                   # Retorna None en caso de error

    def store_extracted_data(self, data, category=None, confidence=0.0): # Define el método para almacenar los datos extraídos
        """
        Almacena datos extraídos en la base de datos local.              # Documentación del método

        Args:                                                             # Documentación de los argumentos
            data (dict): Datos a almacenar                                # El diccionario de datos que se va a almacenar
            category (str): Categoría de los datos (opcional)             # La categoría de los datos (puede ser None)
            confidence (float): Nivel de confianza de la extracción (0-1) # El nivel de confianza de la extracción (valor entre 0 y 1)

        Returns:                                                          # Documentación del valor de retorno
            bool: True si se almacenó correctamente, False si falló        # True si los datos se almacenaron correctamente, False en caso de error
        """
        if not data or not isinstance(data, dict):                         # Verifica si los datos son None o no son un diccionario
            print("Error: Datos inválidos para almacenar")                # Imprime un mensaje de error si los datos no son válidos
            return False                                                  # Retorna False si los datos no son válidos

        try:                                                                # Inicia un bloque try para manejar posibles errores al interactuar con la base de datos
            cursor = self.conn.cursor()                                   # Crea un cursor para ejecutar comandos SQL

            # Prepara los datos para inserción                          # Comentario explicando la siguiente acción
            data_json = json.dumps(data, ensure_ascii=False)               # Convierte el diccionario de datos a formato JSON
            current_date = datetime.now().isoformat()                     # Obtiene la fecha y hora actual en formato ISO

            # Inserta los datos en la base de datos                       # Comentario explicando la siguiente acción
            cursor.execute(                                               # Ejecuta un comando SQL para insertar datos
                f"""
                INSERT INTO {TABLE_NAME}
                (source, extracted_data, category, confidence, extraction_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (data.get('fuente', 'unknown'), data_json, category, confidence, current_date) # Los valores a insertar en la tabla
            )

            self.conn.commit()  # Guarda los cambios                           # Guarda los cambios realizados en la base de datos
            return True                                                   # Retorna True si los datos se almacenaron correctamente

        except sqlite3.Error as e:                                         # Captura errores específicos de SQLite
            print(f"Error al almacenar datos: {e}")                      # Imprime un mensaje de error si ocurre un error de SQLite
            self.conn.rollback()  # Revierte cambios en caso de error        # Revierte cualquier cambio pendiente en la base de datos
            return False                                                  # Retorna False si hubo un error al almacenar

        except Exception as e:                                             # Captura cualquier