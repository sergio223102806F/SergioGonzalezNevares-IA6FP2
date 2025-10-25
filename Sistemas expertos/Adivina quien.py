# -*- coding: utf-8 -*- # Define la codificación de caracteres a UTF-8 para soportar acentos y caracteres especiales.
""" # Inicia un bloque de documentación multi-línea (docstring).
Simulador de Adivina Quién (Autos) con Interfaz Gráfica (Tkinter). # Describe brevemente el propósito del script.
Implementa IA de máxima entropía y persistencia de conocimiento (catalogo_autos.json). # Menciona las características clave: IA y almacenamiento de datos.
""" # Cierra el bloque de documentación.

import tkinter as tk # Importa la librería Tkinter para crear la interfaz gráfica (GUI).
from tkinter import messagebox, simpledialog # Importa módulos específicos de Tkinter para diálogos.
import random # Importa el módulo 'random' para seleccionar el auto secreto al azar.
import json # Importa el módulo 'json' para manejar la lectura y escritura de datos.
import os # Importa el módulo 'os' para interactuar con el sistema operativo (verificar archivos).
from collections import Counter # Importa 'Counter' para contar frecuencias de elementos (clave para la IA).

# Define la ruta del archivo de conocimiento persistente
FILEPATH = 'catalogo_autos.json' # Define una constante con el nombre del archivo JSON de datos.

class AdivinaQuienCarro: # Define la clase principal que contiene toda la lógica del juego.
    """Contiene la lógica del juego, la IA y la gestión del catálogo.""" # Docstring de la clase.

    def __init__(self): # Método constructor de la clase, se ejecuta al crear una instancia.
        # Catálogo base predeterminado de coches
        self.default_catalogo = [ # Lista de diccionarios que representa los autos iniciales (conocimiento base).
            {"nombre": "Tesla Model 3", "color": "rojo", "tipo": "sedán", "pais": "usa", "puertas": 4, "electrico": True}, # Auto 1 con sus atributos.
            {"nombre": "Volkswagen Beetle", "color": "azul", "tipo": "hatchback", "pais": "alemania", "puertas": 2, "electrico": False}, # Auto 2.
            {"nombre": "Ford F-150", "color": "negro", "tipo": "camioneta", "pais": "usa", "puertas": 4, "electrico": False}, # Auto 3.
            {"nombre": "Porsche 911", "color": "amarillo", "tipo": "deportivo", "pais": "alemania", "puertas": 2, "electrico": False}, # Auto 4.
            {"nombre": "Nissan Leaf", "color": "gris", "tipo": "hatchback", "pais": "japón", "puertas": 4, "electrico": True}, # Auto 5.
            {"nombre": "BMW X5", "color": "negro", "tipo": "suv", "pais": "alemania", "puertas": 4, "electrico": False}, # Auto 6.
            {"nombre": "Chevrolet Corvette", "color": "rojo", "tipo": "deportivo", "pais": "usa", "puertas": 2, "electrico": False}, # Auto 7.
            {"nombre": "Honda CR-V", "color": "blanco", "tipo": "suv", "pais": "japón", "puertas": 4, "electrico": False}, # Auto 8.
            {"nombre": "Audi e-tron", "color": "gris", "tipo": "suv", "pais": "alemania", "puertas": 4, "electrico": True}, # Auto 9.
        ] # Fin del catálogo predeterminado.
        
        self.catalogo_autos = [] # Inicializa la lista que contendrá el catálogo de autos cargado (o predeterminado).
        self.claves_atributos = [] # Inicializa la lista que almacenará los nombres de los atributos (color, tipo, etc.).
        
        self.auto_secreto = None # Almacenará el auto seleccionado por el juego para ser adivinado.
        self.candidatos_restantes = [] # Lista de autos que cumplen con las respuestas dadas (filtrado por la IA).
        
        self.cargar_conocimiento() # Llama al método para intentar cargar el catálogo desde el archivo JSON.
        self.actualizar_claves() # Llama al método para obtener los atributos disponibles de los autos.
        
    def cargar_conocimiento(self): # Define el método para cargar datos del archivo persistente.
        """Intenta cargar el catálogo desde el JSON; si falla, usa el predeterminado.""" # Docstring del método.
        if os.path.exists(FILEPATH): # Comprueba si el archivo JSON existe en la ruta definida.
            try: # Inicia un bloque para manejar posibles errores durante la lectura.
                with open(FILEPATH, 'r', encoding='utf-8') as f: # Abre el archivo JSON en modo lectura con codificación UTF-8.
                    data = json.load(f) # Carga el contenido JSON del archivo en la variable 'data'.
                    self.catalogo_autos = data.get("autos", self.default_catalogo) # Obtiene la lista de autos; si falla, usa el catálogo por defecto.
                    return # Si la carga fue exitosa, termina la ejecución del método aquí.
            except (json.JSONDecodeError, FileNotFoundError): # Captura errores si el JSON es inválido o el archivo no se encuentra (aunque ya se verificó).
                pass # Si hay error de decodificación o no se encuentra (raro), ignora el error y continúa.
        
        self.catalogo_autos = self.default_catalogo # Si el archivo no existía o falló la carga, usa el catálogo predeterminado.
        self.guardar_conocimiento() # Guarda inmediatamente el catálogo predeterminado para que exista el archivo JSON.

    def guardar_conocimiento(self): # Define el método para guardar el catálogo actual en el archivo JSON.
        """Guarda el catálogo actual de autos en el archivo JSON.""" # Docstring del método.
        data = {"autos": self.catalogo_autos} # Prepara el diccionario de datos a guardar con la clave "autos".
        try: # Inicia un bloque para manejar posibles errores al escribir en el archivo.
            with open(FILEPATH, 'w', encoding='utf-8') as f: # Abre el archivo JSON en modo escritura ('w') con UTF-8.
                json.dump(data, f, indent=4, ensure_ascii=False) # Escribe el diccionario 'data' en el archivo, con formato legible (indent=4) y soportando acentos.
        except Exception as e: # Captura cualquier otra excepción durante el guardado.
            # En GUI, usamos messagebox o mostramos en la consola para no interrumpir
            print(f"Error al guardar el conocimiento: {e}") # Imprime el error en la consola si ocurre un problema al guardar.

    def actualizar_claves(self): # Define el método para identificar los atributos clave de los autos.
        """Define las claves de atributos basándose en el catálogo cargado.""" # Docstring del método.
        if self.catalogo_autos: # Verifica que el catálogo de autos no esté vacío.
            # Asume que el primer elemento es representativo. Excluye 'nombre'.
            self.claves_atributos = sorted([k for k in self.catalogo_autos[0].keys() if k != 'nombre']) # Obtiene las claves del primer auto, excluye 'nombre', y las ordena.
            
    def reiniciar_juego(self): # Define el método para configurar una nueva partida.
        """Restablece el estado de la partida.""" # Docstring del método.
        if not self.catalogo_autos: # Si el catálogo está vacío, no se puede iniciar el juego.
            return False # Devuelve False indicando que no se pudo reiniciar.
            
        self.auto_secreto = random.choice(self.catalogo_autos) # Elige un auto al azar del catálogo como el auto secreto.
        self.candidatos_restantes = list(self.catalogo_autos) # Inicializa la lista de candidatos con todos los autos del catálogo.
        return True # Devuelve True indicando que el juego se inició correctamente.

    def formatear_pregunta(self, atributo, valor): # Define el método para crear una pregunta legible a partir de un atributo/valor.
        """Crea una pregunta legible.""" # Docstring del método.
        # Traducción para la interfaz
        attr_map = { # Diccionario para mostrar nombres de atributos amigables en la GUI.
            'color': 'Color', 'tipo': 'Tipo', 'pais': 'País', # Mapeo de clave interna a nombre de display.
            'puertas': 'Puertas', 'electrico': 'Eléctrico' # Mapeo de clave interna a nombre de display.
        } # Fin del diccionario de mapeo.
        attr_display = attr_map.get(atributo, atributo.capitalize()) # Obtiene el nombre legible o capitaliza la clave si no está en el mapa.

        if atributo == 'puertas': # Formato especial para la pregunta sobre puertas.
            return f"¿Tiene {valor} puertas?" # Pregunta específica para el número de puertas.
        elif atributo == 'electrico': # Formato especial para la pregunta booleana 'electrico'.
            # Valor True/False se normaliza a 'true'/'false' en la lógica, aquí lo mostramos legible.
            valor_display = 'Sí' if str(valor).lower() == 'true' else 'No' # Convierte el valor booleano en texto 'Sí' o 'No'.
            return f"¿Es un coche eléctrico? (Respuesta esperada: {valor_display})" # Pregunta para el atributo eléctrico.
        else: # Formato genérico para el resto de los atributos (color, tipo, país).
            return f"¿Es de {attr_display} con el valor '{valor}'?" # Pregunta genérica.

    def sugerir_pregunta_optima(self): # Define el método de la IA para sugerir la mejor pregunta.
        """ # Docstring del método.
        [Lógica de la IA] Encuentra el par atributo/valor que maximiza la entropía # Explica el objetivo de la lógica.
        (divide la lista más cerca de 50/50). # Explica el principio de máxima ganancia de información (división 50/50).
        """ # Cierra el docstring.
        N = len(self.candidatos_restantes) # Obtiene el número total de candidatos restantes.
        if N <= 1: # Si solo queda 1 o 0 candidatos, no hay pregunta que hacer.
            return None, None, None # Devuelve None para indicar que no hay sugerencia.
            
        mejor_pregunta = None # Inicializa la variable para almacenar el mejor par (atributo, valor).
        min_desviacion = N  # Inicializa la desviación mínima con el número total de candidatos (el peor caso posible).

        for atributo in self.claves_atributos: # Itera sobre todos los atributos disponibles ('color', 'tipo', etc.).
            # 1. Contar la frecuencia de cada valor para este atributo en el subconjunto
            conteo_valores = Counter(str(auto.get(atributo)).lower() for auto in self.candidatos_restantes) # Cuenta cuántos autos tienen cada valor para el atributo actual.

            for valor, cuenta in conteo_valores.items(): # Itera sobre cada valor único y su conteo para el atributo.
                # 2. Calcular la desviación del punto de división ideal (N / 2)
                desviacion = abs(cuenta - N / 2) # Calcula qué tan lejos está la división de ser 50/50.
                
                # 3. Minimizar la desviación
                if desviacion < min_desviacion: # Si esta desviación es menor que la mínima encontrada hasta ahora...
                    min_desviacion = desviacion # ...actualiza la desviación mínima.
                    mejor_pregunta = (atributo, valor) # ...almacena este par como la mejor pregunta.
                    
        if mejor_pregunta: # Si se encontró una mejor pregunta (siempre que N > 1).
            atributo, valor = mejor_pregunta # Desempaqueta el par atributo/valor.
            pregunta_formateada = self.formatear_pregunta(atributo, valor) # Formatea la pregunta para mostrarla al usuario.
            return atributo, valor, pregunta_formateada # Devuelve el atributo, el valor y la pregunta legible.
            
        return None, None, None # En caso de que algo falle, devuelve None.

    def manejar_pregunta(self, atributo, valor): # Define el método para procesar la pregunta del usuario.
        """Aplica la pregunta del usuario al auto secreto y filtra los candidatos.""" # Docstring del método.
        
        # 1. Normalizar valor
        valor_norm = str(valor).lower().strip() # Convierte el valor ingresado a minúsculas y elimina espacios.
        
        # Manejo especial para el valor booleano 'electrico'
        if atributo == 'electrico': # Si el atributo preguntado es 'electrico' (booleano).
            # Convierte 'si'/'no' a 'true'/'false' para comparar con el secreto
            if valor_norm in ('si', 'sí', 's'): # Si el usuario responde 'sí'.
                valor_norm = 'true' # Normaliza el valor para comparar con el dato True/False en el catálogo.
            elif valor_norm in ('no', 'n'): # Si el usuario responde 'no'.
                valor_norm = 'false' # Normaliza el valor para comparar con el dato True/False en el catálogo.
                
        secreto_valor = str(self.auto_secreto.get(atributo)).lower() # Obtiene el valor del atributo en el auto secreto y lo normaliza.
        
        # Determinar respuesta
        es_cierto = (secreto_valor == valor_norm) # Comprueba si el valor del auto secreto coincide con el valor preguntado.

        # 2. Filtrado
        if es_cierto: # Si la respuesta al usuario es SÍ.
            self.candidatos_restantes = [ # La nueva lista de candidatos son solo los autos que cumplen la condición:
                auto for auto in self.candidatos_restantes # Itera sobre los candidatos actuales.
                if str(auto.get(atributo)).lower() == valor_norm # Si el valor del auto coincide con el valor preguntado.
            ] # Fin de la lista por comprensión.
        else: # Si la respuesta al usuario es NO.
            self.candidatos_restantes = [ # La nueva lista de candidatos son solo los autos que NO cumplen la condición:
                auto for auto in self.candidatos_restantes # Itera sobre los candidatos actuales.
                if str(auto.get(atributo)).lower() != valor_norm # Si el valor del auto NO coincide con el valor preguntado.
            ] # Fin de la lista por comprensión.
        
        return es_cierto, len(self.candidatos_restantes) # Devuelve la respuesta (booleano) y la cantidad de candidatos restantes.

    def guardar_nuevo_auto(self, nuevo_auto_data): # Define el método para agregar un nuevo auto al catálogo.
        """Añade un auto al catálogo y actualiza la persistencia.""" # Docstring del método.
        self.catalogo_autos.append(nuevo_auto_data) # Añade el diccionario del nuevo auto a la lista del catálogo.
        self.guardar_conocimiento() # Llama al método para guardar el catálogo actualizado en el archivo JSON.
        self.actualizar_claves() # Asegura que las nuevas claves se incluyan en el juego (en caso de que el nuevo auto tenga un atributo diferente).
        
        
class GuessingGameGUI(tk.Tk): # Define la clase de la interfaz gráfica, que hereda de tk.Tk (la ventana principal).
    """Interfaz Gráfica de Usuario para el juego Adivina Quién.""" # Docstring de la clase GUI.

    def __init__(self, game_logic): # Método constructor de la clase GUI.
        super().__init__() # Llama al constructor de la clase padre (tk.Tk).
        self.game = game_logic # Almacena la instancia de la lógica del juego.
        self.title("🚗 Adivina el Auto Secreto (IA)") # Establece el título de la ventana.
        self.geometry("600x650") # Establece el tamaño inicial de la ventana (ancho x alto).
        self.resizable(False, False) # Deshabilita la posibilidad de redimensionar la ventana.
        
        # Variables de control de la GUI
        self.candidates_count_var = tk.StringVar(value="0") # Variable de Tkinter para mostrar el conteo de candidatos.
        self.message_var = tk.StringVar(value="Presiona 'Iniciar Nuevo Juego' para comenzar.") # Variable para mostrar mensajes principales.
        self.ai_suggestion_var = tk.StringVar(value="Esperando partida...") # Variable para mostrar la sugerencia de la IA.
        self.selected_attribute_var = tk.StringVar(self) # Variable para almacenar el atributo seleccionado en el menú desplegable (Dropdown).
        
        self.build_ui() # Llama al método para construir todos los elementos visuales.
        self.game_started = False # Bandera booleana para indicar si hay una partida en curso.
        
        # Configurar la inicialización del dropdown
        self.update_ui_state() # Llama a la función para inicializar el estado de los elementos de la UI.

    def build_ui(self): # Define el método que crea la estructura y los widgets de la GUI.
        """Construye todos los elementos de la interfaz.""" # Docstring del método.
        
        # Configuración de estilos
        TITLE_FONT = ("Helvetica", 16, "bold") # Define una fuente para títulos.
        HEADER_FONT = ("Helvetica", 12, "bold") # Define una fuente para encabezados.
        BODY_FONT = ("Helvetica", 10) # Define una fuente para texto normal.
        
        # Marco Principal
        main_frame = tk.Frame(self, padx=15, pady=15, bg="#f0f0f0") # Crea el marco principal con padding y fondo gris claro.
        main_frame.pack(fill="both", expand=True) # Empaqueta el marco para que llene la ventana y se expanda.

        # --- 1. Panel de Estado y Control (Top) ---
        status_frame = tk.Frame(main_frame, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="#e8e8ff") # Crea el marco de estado con borde y fondo azul claro.
        status_frame.pack(fill="x", pady=10) # Empaqueta el marco para que ocupe todo el ancho.
        
        tk.Label(status_frame, text="ESTADO DEL JUEGO", font=TITLE_FONT, bg="#e8e8ff", fg="#4a148c").pack(pady=5) # Etiqueta del título del estado del juego.
        
        # Mensajes
        msg_label = tk.Label(status_frame, textvariable=self.message_var, font=("Helvetica", 11, "italic"), bg="#e8e8ff", wraplength=550) # Etiqueta dinámica para mensajes principales.
        msg_label.pack(fill="x", pady=5) # Empaqueta la etiqueta.
        
        # Contador y Sugerencia
        info_frame = tk.Frame(status_frame, bg="#e8e8ff") # Marco para el contador de candidatos.
        info_frame.pack(fill="x", pady=5) # Empaqueta el marco.

        tk.Label(info_frame, text="Candidatos Restantes:", font=HEADER_FONT, bg="#e8e8ff").pack(side=tk.LEFT, padx=5) # Etiqueta fija para el conteo.
        tk.Label(info_frame, textvariable=self.candidates_count_var, font=("Helvetica", 14, "bold"), bg="#e8e8ff", fg="#004d40").pack(side=tk.LEFT, padx=5) # Etiqueta dinámica del conteo.
        
        # Sugerencia de la IA
        tk.Label(status_frame, text="Sugerencia de la IA (Máxima ganancia de información):", font=HEADER_FONT, bg="#e8e8ff", fg="#1b5e20").pack(pady=(10, 0)) # Etiqueta de título para la sugerencia.
        tk.Label(status_frame, textvariable=self.ai_suggestion_var, font=BODY_FONT, bg="#e8e8ff", wraplength=550).pack(pady=(0, 5)) # Etiqueta dinámica para la sugerencia de la IA.
        
        # Botones de Acción Global
        button_frame = tk.Frame(main_frame, bg="#f0f0f0") # Marco para los botones de control global.
        button_frame.pack(fill="x", pady=10) # Empaqueta el marco.
        
        tk.Button(button_frame, text="▶️ Iniciar Nuevo Juego", command=self.start_game, bg="#4CAF50", fg="white", font=HEADER_FONT, relief=tk.RAISED).pack(side=tk.LEFT, expand=True, padx=5) # Botón para iniciar el juego.
        tk.Button(button_frame, text="✍️ Añadir Auto (Aprender)", command=self.open_learning_mode, bg="#FF9800", fg="white", font=HEADER_FONT, relief=tk.RAISED).pack(side=tk.LEFT, expand=True, padx=5) # Botón para abrir el modo de aprendizaje.

        # --- 2. Panel de Interacción (Preguntar y Adivinar) ---
        interaction_frame = tk.Frame(main_frame, bd=2, relief=tk.RAISED, padx=10, pady=10, bg="white") # Marco para la interacción del juego.
        interaction_frame.pack(fill="x", pady=10) # Empaqueta el marco.
        
        # --- Sección Preguntar ---
        tk.Label(interaction_frame, text="1. HAZ TU PREGUNTA", font=HEADER_FONT, bg="white", fg="#4a148c").pack(fill="x", pady=(5, 10)) # Título de la sección de preguntas.
        
        # Dropdown para el atributo
        attr_label = tk.Label(interaction_frame, text="Atributo:", font=BODY_FONT, bg="white").pack(pady=2, anchor='w') # Etiqueta del dropdown.
        # Crear un OptionMenu vacío inicialmente
        self.attr_menu = tk.OptionMenu(interaction_frame, self.selected_attribute_var, "") # Crea el menú desplegable (OptionMenu) en la variable de atributo.
        self.attr_menu.pack(fill="x", pady=5) # Empaqueta el menú.
        
        # Input para el valor
        tk.Label(interaction_frame, text="Valor (ej: SUV, rojo, usa, si/no):", font=BODY_FONT, bg="white").pack(pady=2, anchor='w') # Etiqueta del campo de valor.
        self.value_entry = tk.Entry(interaction_frame, font=BODY_FONT) # Crea el campo de entrada de texto para el valor.
        self.value_entry.pack(fill="x", pady=5) # Empaqueta el campo.
        
        tk.Button(interaction_frame, text="Preguntar al PC", command=self.handle_question, bg="#64b5f6", fg="black", font=HEADER_FONT).pack(fill="x", pady=10) # Botón para enviar la pregunta.

        # Separador
        tk.Frame(interaction_frame, height=1, bg="#ccc").pack(fill="x", pady=10) # Línea separadora.

        # --- Sección Adivinar ---
        tk.Label(interaction_frame, text="2. ADIVINA EL AUTO", font=HEADER_FONT, bg="white", fg="#4a148c").pack(fill="x", pady=(5, 10)) # Título de la sección de adivinanza.
        
        tk.Label(interaction_frame, text="Nombre Completo del Auto:", font=BODY_FONT, bg="white").pack(pady=2, anchor='w') # Etiqueta del campo de adivinanza.
        self.guess_entry = tk.Entry(interaction_frame, font=BODY_FONT) # Crea el campo de entrada de texto para la adivinanza.
        self.guess_entry.pack(fill="x", pady=5) # Empaqueta el campo.
        
        tk.Button(interaction_frame, text="¡ADIVINAR!", command=self.handle_guess, bg="#e57373", fg="white", font=HEADER_FONT).pack(fill="x", pady=10) # Botón para enviar la adivinanza.
        

    def update_ui_state(self): # Define el método para actualizar el estado de los widgets de la interfaz.
        """Actualiza todos los elementos de la UI basados en el estado del juego.""" # Docstring del método.
        self.candidates_count_var.set(str(len(self.game.candidatos_restantes))) # Actualiza el contador de candidatos restantes.
        
        # Actualizar sugerencia de la IA
        if self.game_started and len(self.game.candidatos_restantes) > 1: # Si el juego está activo y quedan más de un candidato.
            _, _, suggestion = self.game.sugerir_pregunta_optima() # Llama a la IA para obtener la mejor pregunta.
            self.ai_suggestion_var.set(suggestion) # Muestra la sugerencia de la IA.
        elif self.game_started and len(self.game.candidatos_restantes) == 1: # Si solo queda un candidato.
            self.ai_suggestion_var.set(f"¡El auto es el {self.game.candidatos_restantes[0]['nombre']}!") # Muestra el nombre del único auto restante.
        else: # Si el juego no ha comenzado o ha terminado.
            self.ai_suggestion_var.set("Presiona Iniciar Juego para que la IA sugiera la primera pregunta.") # Muestra el mensaje de inicio.
            
        # Actualizar opciones del dropdown
        menu = self.attr_menu["menu"] # Obtiene el menú interno del OptionMenu.
        menu.delete(0, "end") # Limpia todas las opciones actuales del menú.
        
        if not self.game.claves_atributos: # Si no hay atributos cargados.
             menu.add_command(label="Cargando...", state="disabled") # Muestra una opción deshabilitada.
        else: # Si hay atributos disponibles.
            # Mapeo para nombres amigables en el Dropdown
            attr_map = { # Diccionario de mapeo de nombres internos a nombres visibles.
                'color': 'Color', 'tipo': 'Tipo', 'pais': 'País', 
                'puertas': 'Puertas', 'electrico': 'Eléctrico'
            } # Fin del diccionario de mapeo.
            
            for attr in self.game.claves_atributos: # Itera sobre los atributos clave.
                display_name = attr_map.get(attr, attr.capitalize()) # Obtiene el nombre legible.
                menu.add_command(label=display_name, # Añade una opción al menú con el nombre legible.
                                 command=tk._setit(self.selected_attribute_var, attr)) # Configura la acción para establecer la variable al seleccionar la opción.
            
            # Asegurar que se selecciona el primer elemento si no hay nada seleccionado
            if self.selected_attribute_var.get() not in self.game.claves_atributos and self.game.claves_atributos: # Si la variable seleccionada no es válida.
                 self.selected_attribute_var.set(self.game.claves_atributos[0]) # Establece el primer atributo como el seleccionado por defecto.
            

    def start_game(self): # Define el método para iniciar un nuevo juego.
        """Inicializa una nueva partida.""" # Docstring del método.
        if self.game.reiniciar_juego(): # Llama a la lógica del juego para reiniciar (selecciona el auto secreto y los candidatos).
            self.game_started = True # Marca la bandera de juego iniciado como True.
            self.message_var.set(f"🎉 ¡Juego iniciado! Auto secreto elegido. Catálogo: {len(self.game.catalogo_autos)} autos.") # Muestra mensaje de éxito.
            self.value_entry.delete(0, tk.END) # Limpia el campo de entrada de valor.
            self.guess_entry.delete(0, tk.END) # Limpia el campo de adivinanza.
        else: # Si `reiniciar_juego` devuelve False (catálogo vacío).
            messagebox.showerror("Error", "El catálogo de autos está vacío. ¡Añade uno en Modo Aprendizaje!") # Muestra una ventana de error.
            
        self.update_ui_state() # Actualiza el estado de la interfaz.

    def handle_question(self): # Define el método para manejar el evento de enviar una pregunta.
        """Gestiona la pregunta del usuario.""" # Docstring del método.
        if not self.game_started or not self.game.auto_secreto: # Verifica si el juego ha sido iniciado.
            messagebox.showinfo("Alerta", "Por favor, inicia un nuevo juego primero.") # Muestra alerta si no ha iniciado.
            return # Sale del método.

        if len(self.game.candidatos_restantes) <= 1: # Si ya solo queda un candidato (o ninguno).
             self.message_var.set("Solo queda un candidato. ¡Es hora de adivinar!") # Muestra un mensaje.
             self.update_ui_state() # Actualiza el estado.
             return # Sale del método.

        atributo = self.selected_attribute_var.get() # Obtiene el atributo seleccionado del dropdown.
        valor = self.value_entry.get() # Obtiene el valor ingresado por el usuario.

        if not valor: # Verifica si el campo de valor está vacío.
            messagebox.showwarning("Advertencia", "Debes ingresar un valor para el atributo seleccionado.") # Muestra una advertencia.
            return # Sale del método.

        es_cierto, restantes = self.game.manejar_pregunta(atributo, valor) # Llama a la lógica del juego para procesar la pregunta y filtrar.
        self.value_entry.delete(0, tk.END) # Limpia el campo de entrada de valor después de usarlo.
        
        respuesta_display = 'SÍ, es cierto.' if es_cierto else 'NO, no lo es.' # Genera el texto de respuesta.

        if restantes == 0: # Si el filtrado eliminó a todos los candidatos (incluyendo el secreto).
            messagebox.showerror("Fin del Juego", f"¡Error! Has eliminado todos los candidatos. El auto secreto era el {self.game.auto_secreto['nombre']}") # Mensaje de error (pérdida).
            self.game_started = False # Finaliza el juego.
        elif restantes == 1: # Si solo queda un candidato.
            self.message_var.set(f"🤖 Respuesta: {respuesta_display}. ¡Solo queda un candidato! Adivina: {self.game.candidatos_restantes[0]['nombre']}") # Mensaje para indicar que es momento de adivinar.
        else: # Si quedan dos o más candidatos.
            self.message_var.set(f"🤖 Respuesta: {respuesta_display}. Quedan {restantes} candidatos.") # Mensaje con el nuevo número de candidatos.
            
        self.update_ui_state() # Actualiza el estado de la interfaz.

    def handle_guess(self): # Define el método para manejar el intento de adivinanza.
        """Gestiona el intento de adivinanza.""" # Docstring del método.
        if not self.game_started or not self.game.auto_secreto: # Verifica si el juego está activo.
            messagebox.showinfo("Alerta", "Por favor, inicia un nuevo juego primero.") # Muestra alerta si no está activo.
            return # Sale del método.
            
        guess = self.guess_entry.get().strip() # Obtiene el texto de la adivinanza y elimina espacios.
        secret_name = self.game.auto_secreto["nombre"].strip() # Obtiene el nombre del auto secreto y elimina espacios.
        
        if not guess: # Si el campo de adivinanza está vacío.
             messagebox.showwarning("Advertencia", "Debes ingresar el nombre del auto para adivinar.") # Muestra una advertencia.
             return # Sale del método.
             
        if guess.lower() == secret_name.lower(): # Compara la adivinanza (en minúsculas) con el auto secreto (en minúsculas).
            messagebox.showinfo("VICTORIA", f"🎉 ¡FELICIDADES! ¡Adivinaste! El auto era el {secret_name}.") # Mensaje de victoria.
            self.message_var.set("Juego terminado. ¡Inicia un nuevo juego!") # Actualiza el mensaje principal.
            self.game_started = False # Finaliza el juego.
        else: # Si la adivinanza es incorrecta.
            messagebox.showwarning("INCORRECTO", f"❌ ¡Incorrecto! El auto secreto no es el {guess}. ¡Sigue preguntando!") # Mensaje de error.
        
        self.update_ui_state() # Actualiza el estado de la interfaz.


    def open_learning_mode(self): # Define el método para abrir el modo de aprendizaje y añadir un nuevo auto.
        """Abre la ventana o modal para el modo aprendizaje.""" # Docstring del método.
        
        atributos = self.game.claves_atributos # Obtiene la lista de atributos existentes.
        nuevo_auto = {} # Inicializa el diccionario para el nuevo auto.

        # 1. Solicitar nombre
        nombre = simpledialog.askstring("Añadir Auto", "Nombre del Auto (ej: Fiat 500):") # Abre un diálogo para pedir el nombre del auto.
        if not nombre: return # Si el usuario cancela, sale del método.
        nuevo_auto['nombre'] = nombre.strip() # Almacena el nombre.

        # 2. Solicitar atributos (adaptado para GUI)
        for attr in atributos: # Itera sobre cada atributo existente (color, tipo, etc.).
            attr_display = {'color': 'Color', 'tipo': 'Tipo', 'pais': 'País', 'puertas': 'Puertas', 'electrico': 'Eléctrico'}.get(attr, attr.capitalize()) # Obtiene el nombre legible.

            if attr == 'electrico': # Manejo especial para el atributo 'electrico'.
                while True: # Bucle para forzar una respuesta válida (sí/no).
                    resp = simpledialog.askstring("Añadir Auto", f"¿Es {attr_display}? (sí/no):").lower() # Pide al usuario si es eléctrico.
                    if resp in ('si', 'sí', 's'): # Si la respuesta es afirmativa.
                        nuevo_auto[attr] = True # Guarda el booleano True.
                        break # Sale del bucle while.
                    elif resp in ('no', 'n'): # Si la respuesta es negativa.
                        nuevo_auto[attr] = False # Guarda el booleano False.
                        break # Sale del bucle while.
                    elif resp is None: # Si el usuario cancela.
                        return # Sale del método. 
                    else: # Si la respuesta no es válida.
                        messagebox.showwarning("Entrada Inválida", "Respuesta no válida. Usa 'sí' o 'no'.") # Muestra advertencia y repite el bucle.
                        
            elif attr == 'puertas': # Manejo especial para el atributo 'puertas'.
                 while True: # Bucle para forzar una respuesta válida (número).
                    try: # Intenta convertir la entrada a número.
                        resp = simpledialog.askinteger("Añadir Auto", f"Número de {attr_display} (2 o 4):", minvalue=2, maxvalue=5) # Pide el número de puertas (entero).
                        if resp in [2, 4]: # Si es 2 o 4.
                            nuevo_auto[attr] = resp # Guarda el número de puertas.
                            break # Sale del bucle while.
                        elif resp is None: # Si el usuario cancela.
                            return # Sale del método.
                        else: # Si es un número diferente a 2 o 4.
                            messagebox.showwarning("Entrada Inválida", "El número de puertas debe ser 2 o 4.") # Muestra advertencia.
                    except (TypeError, ValueError): # Si la entrada no es un número.
                        messagebox.showwarning("Entrada Inválida", "Debes ingresar un número entero válido (2 o 4).") # Muestra advertencia y repite el bucle.
                        
            else: # Manejo genérico para otros atributos (color, tipo, país).
                # Otros atributos (color, tipo, pais, etc.)
                valor = simpledialog.askstring("Añadir Auto", f"Introduce el valor para '{attr_display}':") # Pide el valor del atributo (string).
                if valor is None: return # Si el usuario cancela, sale.
                if not valor.strip(): # Si el valor está vacío.
                     messagebox.showwarning("Entrada Inválida", "No puede estar vacío.") # Muestra advertencia.
                     return # Sale.
                nuevo_auto[attr] = valor.lower().strip() # Almacena el valor en minúsculas y sin espacios.
        
        # 3. Guardar y actualizar
        self.game.guardar_nuevo_auto(nuevo_auto) # Llama a la lógica del juego para añadir el auto y guardar el JSON.
        messagebox.showinfo("Aprendizaje", f"✅ ¡El auto '{nombre}' ha sido añadido al catálogo y la IA ha aprendido! ({len(self.game.catalogo_autos)} autos en total)") # Mensaje de éxito.
        self.update_ui_state() # Actualiza la interfaz para reflejar el nuevo catálogo.
        self.start_game() # Inicia un nuevo juego con el catálogo actualizado.


if __name__ == "__main__": # Bloque principal que se ejecuta solo cuando el script se corre directamente.
    # 1. Crear la lógica del juego (carga el catálogo)
    game_logic = AdivinaQuienCarro() # Crea una instancia de la clase de lógica del juego.
    
    # 2. Crear y ejecutar la interfaz
    app = GuessingGameGUI(game_logic) # Crea una instancia de la clase de interfaz gráfica, pasándole la lógica del juego.
    app.mainloop() # Inicia el bucle principal de Tkinter, que escucha eventos y muestra la ventana.
