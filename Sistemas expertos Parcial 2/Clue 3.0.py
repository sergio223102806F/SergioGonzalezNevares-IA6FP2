# Importa la librería principal de Tkinter para crear la GUI.
import tkinter as tk
# Importa widgets temáticos avanzados (como botones y marcos) de Tkinter.
from tkinter import ttk, scrolledtext, messagebox
# Importa la función 'random' para seleccionar aleatoriamente la verdad del caso.
import random
# Importa las definiciones de tipo para mejorar la legibilidad y el tipado estricto.
from typing import Dict, Any, List, Tuple

# --- CONSTANTES DEL JUEGO ---
# Define el tiempo total de la partida en segundos (10 minutos).
TOTAL_GAME_TIME_SECONDS = 10 * 60
# Define la duración del castigo de silencio en segundos (2 minutos).
SILENCE_TIME_SECONDS = 2 * 60
# Define el límite máximo de presión antes de que un sospechoso se calle.
MAX_PRESSURE = 100

# Listas de posibles elementos para el misterio (las variables de la verdad).
CULPRITS = ["Mary", "Lucía", "Charlotte", "Amelia", "Gregory"]
WEAPONS = ["Candelabro", "Daga Ceremonial", "Tubería de plomo", "Revólver .38", "Cuerda de seda"]
LOCATIONS = [
    "Penthouse de Larry (Vegas, Lujoso)",
    "Townhouse de Lucía (Manhattan, Elegante)",
    "Mansión de Amelia (Bosque, Diurno)",
    "Jardín de la Mansión (Nocturno)"
]

# --- PERFILES DE SOSPECHOSOS Y DIÁLOGOS EXTENDIDOS (Estilo Visual Novel) ---
# Diccionario principal que almacena el estado, perfil y todos los diálogos de cada sospechoso.
SUSPECT_PROFILES: Dict[str, Dict[str, Any]] = {
    # Bloque de datos para el sospechoso "Mary".
    "Mary": {
        "role": "Novia volátil y Deudora",
        "desc": "Temperamento explosivo. Manipulable por afecto y por sus deudas con Larry.",
        "key": "mary", # Clave interna.
        "pressure": 0, # Nivel de presión inicial (se actualiza durante el juego).
        "isSilenced": False, # Estado de silencio (True si está castigada).
        "silencedTimer": 0, # Temporizador de castigo de silencio.
        "questions": { # Diálogos y efectos de presión para cada tipo de pregunta.
            # Pregunta de tipo "Neutral". Baja presión.
            "Neutral": {"label": "¿Cuál es su coartada y por qué Larry le debía dinero?", "pressure_change": -10, "dialogue": [
                # Contiene la respuesta del sospechoso.
                "**Mary:** (Voz nasal, molesta) Estuve sola en casa, por supuesto. ¿Mi coartada? Estaba lamentando mi existencia con una botella de vino barato. Larry me canceló, otra vez, por 'asuntos urgentes' con Lucía, la abogada. Sobre la deuda... él no me debía dinero; *yo* le debía a *él*. Me prestó una cantidad absurda para 'invertir' y me hizo firmar un pagaré con intereses. Me dijo que era un 'contrato de amor'. ¡Qué estúpida! Si Larry fue asesinado, Lucía lo sabrá; ella tiene todos sus papeles legales, no yo."
            ]},
            # Pregunta de tipo "Emotional". Sube moderadamente la presión.
            "Emotional": {"label": "Presione sobre el ciclo de pasión/manipulación y los celos hacia Lucía.", "pressure_change": +35, "dialogue": [
                "**Mary:** (Grita, golpeando la mesa) ¡Es amor! ¡Era la única persona que me hacía sentir importante! ¿Celos? Sí, Lucía me dio asco con ese correo profesional amenazándome. ¡Qué fría! Ella lo veía como un activo. Yo lo veía... como mi droga. Larry me había prometido que, si su divorcio con Charlotte terminaba, yo sería la siguiente. Pero ¿Charlotte? ¡Ella es rica! ¿Qué quería Larry de ella aparte de la custodia? Algo raro hay allí, te lo juro. Él odiaba a Charlotte más que a nadie."
            ]},
            # Pregunta de tipo "Accusatory". Sube mucho la presión.
            "Accusatory": {"label": "Acúsela de que su temperamento y desesperación financiera la hicieron ceder a la rabia.", "pressure_change": +60, "dialogue": [
                "**Mary:** (Cae en el asiento, rota) ¿Ceder a la rabia? La rabia es mejor que la humillación, Detective. ¡No lo hice! Le diré quién estaba demente por amor: Gregory. Lo vi una vez en la Mansión de Amelia, y la forma en que él la mira... es enfermizo. Si alguien mató por la obsesión que Larry tenía con Amelia, fue Gregory, no yo por el estúpido de Larry. ¡Ahora silencio, o llamo a mi abogado!"
            ]},
        }
    },
    # Bloque de datos para el sospechoso "Lucía".
    "Lucía": {
        "role": "Abogada ambiciosa y Socia",
        "desc": "Estratega fría, actual pareja de Larry. Mantiene una fachada legalista perfecta.",
        "key": "lucia", "pressure": 0, "isSilenced": False, "silencedTimer": 0,
        "questions": {
            "Neutral": {"label": "Solicite los registros de su reunión y detalles sobre las 'operaciones' de Larry.", "pressure_change": -5, "dialogue": [
                "**Lucía:** (Profesional, desliza un documento) Mis registros están aquí: 9:17 PM en la oficina, luego cena de negocios con mi socio. Mi coartada es irrefutable. ¿Operaciones de Larry? Él estaba en una crisis de liquidez extrema por su divorcio con Charlotte. Larry estaba desesperado. Le sugirió a **Amelia** que invirtiera en uno de sus proyectos inmobiliarios de dudosa legalidad, y ella se negó. Sé que Larry no estaba acostumbrado a que le dijeran que no, y esa negativa lo enfureció."
            ]},
            "Emotional": {"label": "Cuestione si Larry era solo un activo que se convirtió en un pasivo problemático.", "pressure_change": +20, "dialogue": [
                "**Lucía:** (Frunce el ceño, irritada) ¡Qué tontería! Larry era un socio *brillante*, aunque imprudente. ¿Pasivo? Estábamos a punto de ganar una gran batalla contra **Charlotte** por unas acciones *ocultas* que ella quería reclamar, no solo la custodia. Su muerte arruina mi caso y mi prestigio. ¿Cree que yo, una abogada a punto de ser socia principal, cometería un error tan amateur por 'celos'? No, Detective. Si hay pasión aquí, búscala en Mary. Yo solo manejo hechos."
            ]},
            "Accusatory": {"label": "Insinúe que usted lo eliminó para cobrar seguros o evitar que sus deudas la arrastraran.", "pressure_change": +70, "dialogue": [
                "**Lucía:** (Risa seca, llena de burla) ¿Seguros? Mi carrera vale más que cualquier póliza. ¡Usted es patético! Larry me dijo que **Gregory**, el mayordomo de Amelia, lo había estado espiando. Lo vio una vez en el penthouse, cerca de la hora de su desaparición, revolviendo un cajón. Larry pensó que Gregory estaba buscando un archivo confidencial. ¡Encuentre a Gregory y déjeme en paz! ¡Esta entrevista ha terminado, y mi bufete recibirá una llamada por acoso legal!"
            ]},
        }
    },
    # Bloque de datos para el sospechoso "Charlotte".
    "Charlotte": {
        "role": "Primera ex-esposa Rica y Resentida",
        "desc": "Aristocrática, resentida, odiaba el control de Larry. Lucha por una fortuna oculta.",
        "key": "charlotte", "pressure": 0, "isSilenced": False, "silencedTimer": 0,
        "questions": {
            "Neutral": {"label": "¿Cuál era su paradero y su situación legal con Larry en el momento de su desaparición?", "pressure_change": -5, "dialogue": [
                "**Charlotte:** (Tono de superioridad aburrida) Estaba en la gala de la Ópera, mi coartada es verificable por la alta sociedad. La situación legal era simple: Larry me odiaba por haberle ganado la custodia de los niños, y lo odiaba por su falta de clase. Él me estaba acosando por vender el antiguo **Candelabro** familiar. Larry lo quería para pagar deudas. Si alguien lo mató, fue por la rabia que generaba su insolencia financiera. Pregúntele a Lucía si su 'socio' no estaba al borde de la quiebra."
            ]},
            "Emotional": {"label": "Cuestione si su actitud sarcástica oculta la herida de un divorcio tan catastrófico.", "pressure_change": +30, "dialogue": [
                "**Charlotte:** (Mira al Detective con desprecio) ¿Herida? No soy una de esas chicas emocionales como **Mary**. Yo me recupero con cheques. La única herida era que su ego se interpusiera en mis finanzas. Larry estaba intentando usar una de mis cuentas de fideicomiso *off-shore* como garantía para un préstamo turbio. Me amenazó con arruinar mi reputación social. Le dije que si intentaba algo, haría que su vida legal fuera un infierno. Lucía lo sabía, por cierto. Ella estaba muy nerviosa por ese préstamo."
            ]},
            "Accusatory": {"label": "Insinúe que lo mató para silenciarlo y proteger su fortuna/reputación.", "pressure_change": +70, "dialogue": [
                "**Charlotte:** (Se levanta, golpeando la silla) ¡Yo no me rebajo a eso! Mi dinero vale más que su miserable vida. Si Larry fue asesinado, fue un acto de **Amelia**. Ella es la única persona que tiene la capacidad de hacer desaparecer a alguien sin dejar rastro. Larry la idolatraba, pero ella es fría y política. Él se enamoró, y ella lo usó para obtener acceso a la información que él tenía sobre un político en particular. ¡Mírenla a ella y no a mí, estoy limpia! ¡Traigan a mi abogado!"
            ]},
        }
    },
    # Bloque de datos para el sospechoso "Amelia".
    "Amelia": {
        "role": "Política Influyente y Manipuladora",
        "desc": "Poderosa, fría. Usaba a Larry por su influencia y a Gregory por su lealtad ciega.",
        "key": "amelia", "pressure": 0, "isSilenced": False, "silencedTimer": 0,
        "questions": {
            "Neutral": {"label": "Verifique su agenda y si la relación con Larry le dio acceso a información sensible.", "pressure_change": -10, "dialogue": [
                "**Amelia:** (Compostura total, voz suave) Estaba en Chicago, cerrando un acuerdo de inversión, con testigos y registro de vuelo. Larry me era útil por su red de contactos, sí. Me dio acceso a cierta información sobre licitaciones de la ciudad, pero nada sensible. Él estaba enamorado, yo era... cortés. Larry me habló mucho de su ex-esposa, **Charlotte**. Mencionó que Charlotte estaba ocultando documentos cruciales en un activo físico, no en cuentas. Algo que podría ser una 'Daga Ceremonial' o un objeto de arte."
            ]},
            "Emotional": {"label": "Insinúe que lo eliminó al volverse un riesgo emocional o político.", "pressure_change": +40, "dialogue": [
                "**Amelia:** (Su sonrisa es controlada pero tensa) Detective, un riesgo emocional es algo que se gestiona, no algo que se mata. Larry era predeciblemente imprudente. Si se convirtió en un riesgo, lo habría exiliado a una de mis propiedades en el extranjero. Pero, si vamos a lo emocional, sí, tengo a **Gregory**. Gregory está enamorado de mí desde hace diez años, desde que le di su primer trabajo. Su lealtad es ciega. Larry lo humilló públicamente una vez en mi fiesta. Gregory nunca lo olvidó. Eso es peligro emocional, no yo."
            ]},
            "Accusatory": {"label": "Cuestione si manipuló a Gregory para que hiciera el 'trabajo sucio' por su amor.", "pressure_change": +80, "dialogue": [
                "**Amelia:** (El aire se enfría, su voz se vuelve hielo) ¡Cuidado! La lealtad no es un crimen. Gregory es un hombre de honor, aunque tiene una fe ciega en mí. Larry era un hombre de secretos. Él me confió que pensaba esconder documentos incriminatorios en su caja fuerte del **Penthouse de Vegas**, no de Nueva York. Si alguien lo mató por esos documentos, vaya al Penthouse. Y no voy a tolerar que acuse a mi personal sin pruebas. ¡Mi abogado está en camino, se acabó el juego!"
            ]},
        }
    },
    # Bloque de datos para el sospechoso "Gregory".
    "Gregory": {
        "role": "Mayordomo Enamorado y Ejecutor",
        "desc": "Fiel a Amelia, celoso de Larry. Víctima de la manipulación de Amelia.",
        "key": "gregory", "pressure": 0, "isSilenced": False, "silencedTimer": 0,
        "questions": {
            "Neutral": {"label": "Verifique sus movimientos en la noche del incidente y su relación con Larry.", "pressure_change": -5, "dialogue": [
                "**Gregory:** (Habla en voz baja, nervioso, casi un murmullo) Estuve en Chicago con la Sra. Amelia, en la suite contigua. Mis deberes son sagrados. Larry era... una molestia. Un hombre vulgar. La Sra. Amelia le guardaba cortesía, pero no respeto. Él la usaba para hablar de dinero y política. Él habló mucho de **Mary**, su amante. Dijo que Mary era 'demasiado ruidosa' y que pronto la 'silenciaría' para que Lucía no se enterara de sus tejemanejes en el divorcio. Larry tenía una lengua muy suelta."
            ]},
            "Emotional": {"label": "Presione sobre su amor por Amelia y el resentimiento hacia Larry por su coqueteo.", "pressure_change": +35, "dialogue": [
                "**Gregory:** (Tiembla, sus ojos brillan) ¡Mi amor por la Sra. Amelia es puro! Ella me dio dignidad. ¡Larry la humillaba con su simple presencia! Él era un hombre que tocaba lo que no le pertenecía. Lo detestaba, sí. Recientemente, la Sra. Amelia me pidió un 'favor'. Fue un viaje corto, una entrega de documentos a un lugar... discreto. Ella estaba muy estresada por su reunión de Chicago. Le dije que haría cualquier cosa por ella. Lo que sea."
            ]},
            "Accusatory": {"label": "Acúselo de haber viajado para ejecutar la orden de Amelia en un acto de amor obsesivo.", "pressure_change": +80, "dialogue": [
                "**Gregory:** (Se derrumba en el asiento, tartamudeando) ¡No! Yo... Yo solo hago lo que ella me pide. Ella es mi vida. Ella me pidió que fuera a revisar un paquete que dejó olvidado... en el **Townhouse de Lucía**. ¡No quería que Lucía lo encontrara! Solo hice ese 'favor' para protegerla. ¡No lo maté! Pero sí, la Sra. Amelia me dijo que si alguien me preguntaba, yo estaría en Chicago. ¡No diré una palabra más, llame a mi abogada... si es que la Sra. Amelia me deja tener una!"
            ]},
        }
    }
}


# Definición de la clase principal de la aplicación.
class ClueSimulatorApp:
    # Constructor de la clase, se ejecuta al iniciar la aplicación.
    def __init__(self, master):
        # Almacena la ventana principal de Tkinter.
        self.master = master
        # Establece el título de la ventana.
        master.title("Simulador de Interrogatorio - Estilo Novela Visual")
        # Establece el tamaño inicial de la ventana.
        master.geometry("1400x900")
        # Configura el color de fondo de la ventana principal.
        master.configure(bg="#1c1c1c")

        # --- Variables de Configuración del Caso ---
        # Almacenará el culpable real (seleccionado aleatoriamente al inicio).
        self.guilty_culprit = ""
        # Almacenará el arma real.
        self.guilty_weapon = ""
        # Almacenará la locación real.
        self.guilty_location = ""
        # Almacenará el texto de la resolución final del caso.
        self.resolution_text = ""
        # Bandera que indica si el juego ha terminado.
        self.game_over = False
        # El tiempo restante global, inicializado a 10 minutos.
        self.game_time_remaining = TOTAL_GAME_TIME_SECONDS
        # Clave del sospechoso actualmente seleccionado para interrogar.
        self.current_suspect_key = None
        # ID para el `after` del temporizador, usado para cancelar el bucle.
        self.after_id = None

        # Llama al método para configurar los estilos visuales (CSS de Tkinter).
        self._setup_styles()
        # Llama al método para construir la interfaz gráfica.
        self._setup_ui()
        # Inicia una nueva partida inmediatamente al cargar.
        self.start_new_game()

    # Método para configurar los estilos visuales del juego (tema de Novela Visual).
    def _setup_styles(self):
        # Obtiene una instancia del objeto Style.
        style = ttk.Style()
        # Establece el tema base.
        style.theme_use('clam')
        
        # Paleta de Colores VN
        BG_DARK = "#282828" # Fondo oscuro.
        BG_MID = "#3c3c3c" # Fondo medio.
        TEXT_LIGHT = "#f0f0f0" # Texto claro.
        ACCENT_YELLOW = "#f1c40f" # Acento amarillo (títulos).
        ACCENT_BLUE = "#3498db" # Acento azul (detective).
        ACCENT_RED = "#e74c3c" # Acento rojo (peligro, presión).
        
        # Configuración general de etiquetas.
        style.configure("TLabel", background=BG_DARK, foreground=TEXT_LIGHT, font=('Inter', 11))
        # Configuración general de marcos.
        style.configure("TFrame", background=BG_DARK)
        # Configuración de botones principales (acusación, nuevo caso).
        style.configure("TButton", font=('Inter', 11, 'bold'), borderwidth=1, relief="flat", background=ACCENT_BLUE, foreground=BG_DARK, padding=8)
        # Configuración del color de los botones principales al pasar el ratón.
        style.map("TButton", background=[('active', '#5d9cec')])
        
        # Estilo específico para los botones de selección de sospechosos.
        style.configure("Suspect.TButton", font=('Inter', 10, 'bold'), borderwidth=1, relief="raised", background="#7f8c8d", foreground=BG_DARK, padding=6)
        style.map("Suspect.TButton", background=[('active', '#95a5a6')])

        # Estilo para la barra de progreso (barra de presión) en color rojo intenso.
        style.layout('Red.Horizontal.TProgressbar', 
                     [('Red.Horizontal.TProgressbar.trough',
                       {'children': [('Red.Horizontal.TProgressbar.pbar',
                                      {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nswe'})])
        # Configura los colores de la barra de presión.
        style.configure('Red.Horizontal.TProgressbar', troughcolor=BG_MID, background=ACCENT_RED, bordercolor=BG_DARK, thickness=12)

    # Método para construir la interfaz de usuario.
    def _setup_ui(self):
        # Crea el marco principal con padding.
        main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        
        # Usa grid para el frame principal y lo expande para llenar la ventana.
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Configura las columnas para dividir el espacio: Diálogo (3 partes) y Controles (1 parte).
        main_frame.grid_columnconfigure(0, weight=3) # Diálogo
        main_frame.grid_columnconfigure(1, weight=1) # Controles
        # Configura las filas: Fila 0 (Header), Fila 1 (Contenido, toma el espacio restante).
        main_frame.grid_rowconfigure(1, weight=1)

        # --- Fila 0: Estado y Título ---
        # Crea un marco para el encabezado.
        header_frame = ttk.Frame(main_frame)
        # Coloca el encabezado en la primera fila, abarcando ambas columnas.
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        # Etiqueta para el título principal del juego.
        ttk.Label(header_frame, text="EXPEDIENTE DE ASESINATO", font=('Inter', 24, 'bold'), foreground="#f1c40f", background="#1c1c1c").grid(row=0, column=0, sticky="w")
        
        # Etiqueta para el contador de tiempo, crucial para el juego.
        self.timer_label = ttk.Label(header_frame, text="Tiempo: 10:00", font=('Inter', 18, 'bold'), foreground="#e74c3c", background="#1c1c1c")
        self.timer_label.grid(row=0, column=1, sticky="e")

        # --- Columna 0: Panel de Diálogo y Narrativa (Visual Novel Display) ---
        # Marco para el área de diálogo.
        dialogue_frame = ttk.Frame(main_frame, padding="15", relief=tk.GROOVE)
        # Coloca el marco de diálogo y lo expande.
        dialogue_frame.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        dialogue_frame.grid_rowconfigure(0, weight=1)
        dialogue_frame.grid_columnconfigure(0, weight=1)

        # Área de texto con scroll (ScrolledText) para la narrativa del juego.
        self.narrative_text = scrolledtext.ScrolledText(dialogue_frame, wrap=tk.WORD, width=70, height=35, font=('Georgia', 14), bg="#1c1c1c", fg="#f0f0f0", padx=20, pady=20, borderwidth=0, relief="flat")
        self.narrative_text.grid(row=0, column=0, sticky="nsew")
        # Inicialmente deshabilita la edición por parte del usuario.
        self.narrative_text.config(state=tk.DISABLED)

        # --- Columna 1: Controles e Interrogatorio ---
        # Marco para los controles del juego.
        controls_frame = ttk.Frame(main_frame, padding="15", relief=tk.GROOVE)
        # Coloca el marco de controles y lo expande.
        controls_frame.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")
        controls_frame.grid_columnconfigure(0, weight=1)

        # 1. Selección de Sospechoso
        # Título de la sección de interrogatorio.
        ttk.Label(controls_frame, text="1. INTERROGAR SOSPECHOSO", font=('Inter', 16, 'bold', 'underline'), foreground="#3498db").grid(row=0, column=0, pady=(0, 15), sticky="ew")
        
        # Marco para contener los botones de los sospechosos.
        self.suspect_buttons_frame = ttk.Frame(controls_frame)
        self.suspect_buttons_frame.grid(row=1, column=0, pady=10, sticky="ew")
        # Llama al método para crear los 5 botones.
        self._create_suspect_buttons()

        # 2. Detalles del Sospechoso Seleccionado
        # Etiqueta de perfil.
        ttk.Label(controls_frame, text="Perfil:", font=('Inter', 12, 'bold')).grid(row=2, column=0, pady=(15, 0), sticky="w")
        # Etiqueta para mostrar la descripción del sospechoso actual.
        self.suspect_details_label = ttk.Label(controls_frame, text="<Selecciona un sujeto>", font=('Inter', 11, 'italic'), wraplength=400, foreground="#bdc3c7")
        self.suspect_details_label.grid(row=3, column=0, pady=(5, 10), sticky="w")
        
        # Etiqueta para la barra de presión.
        ttk.Label(controls_frame, text="Nivel de Presión (Riesgo de Silencio):", foreground="#e74c3c").grid(row=4, column=0, sticky="w")
        # Barra de progreso que representa la presión del sospechoso actual.
        self.pressure_bar = ttk.Progressbar(controls_frame, orient='horizontal', mode='determinate', style='Red.Horizontal.TProgressbar')
        self.pressure_bar.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        # Etiqueta de advertencia de silencio.
        self.silence_label = ttk.Label(controls_frame, text="¡SILENCIO ACTIVO! Tiempo restante: ", font=('Inter', 12, 'bold'), foreground="#e74c3c")
        self.silence_label.grid(row=6, column=0, pady=5, sticky="ew")
        # La etiqueta de silencio se oculta al inicio.
        self.silence_label.grid_remove() 

        # 3. Preguntas de Interrogatorio
        # Título de la sección de enfoque.
        ttk.Label(controls_frame, text="2. ELEGIR ENFOQUE", font=('Inter', 16, 'bold', 'underline'), foreground="#f1c40f").grid(row=7, column=0, pady=(20, 15), sticky="ew")
        
        # Marco que contendrá los botones de preguntas (Neutral, Emotional, Accusatory).
        self.question_buttons_frame = ttk.Frame(controls_frame)
        self.question_buttons_frame.grid(row=8, column=0, pady=5, sticky="ew")

        # 4. Acusación Final (Una Sola Oportunidad)
        # Título de la acusación con énfasis en la regla de "Una Oportunidad".
        ttk.Label(controls_frame, text="3. ACUSACIÓN FINAL (Una Oportunidad)", font=('Inter', 16, 'bold', 'underline'), foreground="#2ecc71").grid(row=9, column=0, pady=(20, 15), sticky="ew")
        
        # Etiqueta y Combobox para seleccionar al Culpable.
        ttk.Label(controls_frame, text="Culpable:", background="#282828").grid(row=10, column=0, sticky="w", pady=2)
        self.culprit_var = tk.StringVar(controls_frame, value=CULPRITS[0])
        ttk.Combobox(controls_frame, textvariable=self.culprit_var, values=CULPRITS, state="readonly").grid(row=11, column=0, sticky="ew", pady=(0, 5))
        
        # Etiqueta y Combobox para seleccionar el Arma.
        ttk.Label(controls_frame, text="Arma:", background="#282828").grid(row=12, column=0, sticky="w", pady=2)
        self.weapon_var = tk.StringVar(controls_frame, value=WEAPONS[0])
        ttk.Combobox(controls_frame, textvariable=self.weapon_var, values=WEAPONS, state="readonly").grid(row=13, column=0, sticky="ew", pady=(0, 5))
        
        # Etiqueta y Combobox para seleccionar la Locación.
        ttk.Label(controls_frame, text="Locación:", background="#282828").grid(row=14, column=0, sticky="w", pady=2)
        self.location_var = tk.StringVar(controls_frame, value=LOCATIONS[0])
        ttk.Combobox(controls_frame, textvariable=self.location_var, values=LOCATIONS, state="readonly").grid(row=15, column=0, sticky="ew", pady=(0, 15))

        # Botón para la acusación final, que termina el juego.
        ttk.Button(controls_frame, text="HACER ACUSACIÓN FORMAL", command=self.make_accusation, style="TButton").grid(row=16, column=0, sticky="ew", pady=(10, 5))
        # Botón para iniciar un nuevo caso.
        ttk.Button(controls_frame, text="INICIAR NUEVO CASO", command=self.start_new_game, style="TButton").grid(row=17, column=0, sticky="ew")


    # Método para crear dinámicamente los botones de selección de sospechosos.
    def _create_suspect_buttons(self):
        """Crea los botones de selección de sospechosos."""
        for i, name in enumerate(CULPRITS):
            # Convierte el nombre a minúsculas para usarlo como clave interna.
            key = name.lower()
            
            # Crea un botón para cada sospechoso, asignando la función 'select_suspect'.
            button = ttk.Button(self.suspect_buttons_frame, text=name, 
                                command=lambda k=key: self.select_suspect(k), 
                                style="Suspect.TButton")
            
            # Lógica para distribuir los botones en dos filas (3 en la primera, 2 en la segunda).
            row = i // 3
            col = i % 3
            if i >= 3:
                row = 1
                col = i - 3
                
            # Coloca el botón en la cuadrícula del marco de botones.
            button.grid(row=row, column=col, padx=3, pady=5, sticky="ew")
            self.suspect_buttons_frame.grid_columnconfigure(col, weight=1)
            
            # Almacena la referencia del botón en el diccionario de perfiles para manipular su estado.
            SUSPECT_PROFILES[name]["button"] = button


    # Método que selecciona aleatoriamente el culpable, el arma y la locación (la VERDAD del caso).
    def _generate_case(self) -> Tuple[str, str, str, str]:
        """Selecciona el caso y la narrativa. Aquí se define la VERDAD."""
        # Asignación aleatoria del culpable.
        self.guilty_culprit = random.choice(CULPRITS)
        # Asignación aleatoria del arma.
        self.guilty_weapon = random.choice(WEAPONS)
        # Asignación aleatoria de la locación.
        self.guilty_location = random.choice(LOCATIONS)
        
        # Define el título del caso.
        narrative_title = "El Homicidio de Larry: Pasión y Poder"
        # Define la introducción de la narrativa.
        narrative_intro = (
            f"[SISTEMA] El cuerpo de Larry, el magnate, fue encontrado en la escena del crimen. "
            f"La causa de la muerte fue un trauma fatal. Larry tenía enemigos en todos los círculos. "
            f"Los cinco sospechosos (Mary, Lucía, Charlotte, Amelia y Gregory) están listos para ser interrogados. "
            f"\n\n**Detective:** (Abre el expediente) Empecemos. El tiempo corre."
        )
        # Define el texto de resolución (se muestra al ganar).
        resolution_text = (
            f"**¡CASO RESUELTO!**\n\nEl asesino es: {self.guilty_culprit}.\n"
            f"El arma utilizada fue: {self.guilty_weapon}.\n"
            f"La ubicación real fue: {self.guilty_location}.\n\n"
            f"El detective pudo conectar los hilos de celos, finanzas y manipulación política que llevaron a este acto."
        )
        # Retorna los textos para ser utilizados en la UI.
        return narrative_title, narrative_intro, resolution_text


    # Método principal para inicializar o reiniciar el juego.
    def start_new_game(self):
        """Inicia una nueva partida."""
        # Si hay un temporizador activo, lo cancela para evitar múltiples bucles.
        if self.after_id:
            self.master.after_cancel(self.after_id)
        
        # Reinicia las banderas y temporizadores del juego.
        self.game_over = False
        self.game_time_remaining = TOTAL_GAME_TIME_SECONDS
        self.current_suspect_key = None
        # Oculta el mensaje de silencio.
        self.silence_label.grid_remove()

        # Genera una nueva verdad para el caso.
        narrative_title, narrative_intro, self.resolution_text = self._generate_case()
        
        # Reiniciar el estado de los sospechosos (presión, silencio, etc.).
        for name in SUSPECT_PROFILES:
            profile = SUSPECT_PROFILES[name]
            profile["pressure"] = 0
            profile["isSilenced"] = False
            profile["silencedTimer"] = 0
            # Si el botón existe, lo reactiva y le aplica el estilo normal.
            if "button" in profile:
                profile["button"].config(state=tk.NORMAL, style="Suspect.TButton")
        
        # Inicializa la UI de presión a cero.
        self._update_pressure_bar()
        # Actualiza la etiqueta de detalles del sospechoso.
        self.suspect_details_label.config(text="Selecciona un sospechoso para empezar el interrogatorio.")
        
        # Limpia y re-crea los botones de preguntas.
        self._clear_question_buttons()

        # Imprimir la introducción del caso en el área de diálogo.
        self.narrative_text.config(state=tk.NORMAL)
        self.narrative_text.delete(1.0, tk.END) # Borra contenido anterior.
        # Inserta el título con un tag de formato.
        self.narrative_text.insert(tk.INSERT, f"--- INICIO DEL CASO: {narrative_title} ---\n\n", "header")
        # Inserta la introducción.
        self.narrative_text.insert(tk.INSERT, narrative_intro + "\n\n")
        self.narrative_text.config(state=tk.DISABLED) # Deshabilita la edición.
        
        # Configurar tags de color para la Novela Visual.
        self.narrative_text.tag_config("header", foreground="#f1c40f", font=('Inter', 16, 'bold'))
        self.narrative_text.tag_config("detective", foreground="#3498db", font=('Georgia', 14, 'italic'))
        self.narrative_text.tag_config("suspect", foreground="#2ecc71", font=('Georgia', 14, 'bold'))
        self.narrative_text.tag_config("system", foreground="#e74c3c", font=('Inter', 12, 'bold'))
        
        # Iniciar el bucle de temporizadores.
        self._update_timers()


    # Bucle principal del juego: maneja el tiempo global y los castigos de silencio.
    def _update_timers(self):
        """Maneja el temporizador principal y los temporizadores de silencio."""
        # Detiene el bucle si el juego ha terminado.
        if self.game_over:
            return

        # 1. Temporizador Global
        if self.game_time_remaining > 0:
            self.game_time_remaining -= 1
            # Calcula minutos y segundos para el formato MM:SS.
            minutes = self.game_time_remaining // 60
            seconds = self.game_time_remaining % 60
            # Actualiza la etiqueta del temporizador.
            self.timer_label.config(text=f"Tiempo: {minutes:02d}:{seconds:02d}")
        else:
            # Si el tiempo llega a cero, termina el juego por derrota.
            self.end_game("¡Tiempo agotado! El caso no pudo resolverse a tiempo.", "#e74c3c")
            return

        # 2. Temporizadores de Silencio (para cada sospechoso)
        for name in SUSPECT_PROFILES:
            profile = SUSPECT_PROFILES[name]
            # Si el sospechoso está silenciado...
            if profile["isSilenced"]:
                profile["silencedTimer"] -= 1 # Descuenta un segundo.
                if profile["silencedTimer"] <= 0:
                    # Cuando el castigo termina, reinicia su estado.
                    profile["isSilenced"] = False
                    profile["silencedTimer"] = 0
                    profile["pressure"] = 0 # La presión se reinicia al calmarse.
                    # Reactiva el botón del sospechoso.
                    profile["button"].config(state=tk.NORMAL, style="Suspect.TButton")
                    # Registra un mensaje en el diálogo.
                    self.log_dialogue(f"[SISTEMA] {name} ha terminado su periodo de silencio y está dispuesto(a) a hablar.", "system")
                    
                # Actualizar el label de silencio si el sospechoso actual está silenciado.
                if self.current_suspect_key and self.current_suspect_key.capitalize() == name and profile["isSilenced"]:
                    self.silence_label.config(text=f"¡SILENCIO ACTIVO! Tiempo restante: {profile['silencedTimer']} segundos")

        # 3. Re-agendar la llamada
        # Llama a este método de nuevo después de 1000ms (1 segundo).
        self.after_id = self.master.after(1000, self._update_timers)

    # Método para actualizar visualmente la barra de presión.
    def _update_pressure_bar(self):
        """Actualiza la barra de progreso y el estado de los botones."""
        if self.current_suspect_key:
            # Encuentra el perfil del sospechoso actual.
            name = self.current_suspect_key.capitalize()
            profile = SUSPECT_PROFILES.get(name)
            if profile:
                # Establece el valor de la barra de progreso al nivel de presión actual.
                self.pressure_bar['value'] = profile["pressure"]
        else:
            # Si no hay nadie seleccionado, la barra está vacía.
            self.pressure_bar['value'] = 0

    # Método para limpiar dinámicamente el área de botones de pregunta.
    def _clear_question_buttons(self):
        """Destruye los botones de pregunta para recrearlos."""
        # Comprueba si el marco existe.
        if hasattr(self, 'question_buttons_frame'):
            # Destruye el marco anterior.
            self.question_buttons_frame.destroy()
        
        # Recrear el frame de botones de pregunta en su posición original.
        self.question_buttons_frame = ttk.Frame(self.master)
        # Lo coloca en la posición correcta (row=8, col=0) dentro del marco de controles.
        self.question_buttons_frame.grid(row=8, column=0, pady=5, sticky="ew")
        self.question_buttons_frame.grid_columnconfigure(0, weight=1)


    # Método que se ejecuta al hacer clic en un botón de sospechoso.
    def select_suspect(self, key):
        """Selecciona un sospechoso para interrogar."""
        # Establece la clave del sospechoso actual.
        self.current_suspect_key = key
        name = key.capitalize()
        profile = SUSPECT_PROFILES[name]

        # Actualiza la descripción del perfil.
        self.suspect_details_label.config(text=f"Rol: {profile['role']}. Perfil: {profile['desc']}")
        # Actualiza la barra de presión para el nuevo sospechoso.
        self._update_pressure_bar()

        # Ocultar/Mostrar el temporizador de silencio según el estado.
        if profile["isSilenced"]:
            self.silence_label.grid()
            # Muestra el tiempo restante del castigo.
            self.silence_label.config(text=f"¡SILENCIO ACTIVO! Tiempo restante: {profile['silencedTimer']} segundos")
        else:
            self.silence_label.grid_remove() # Lo oculta si no está silenciado.

        # Recrea los botones de preguntas.
        self._clear_question_buttons()
        
        # Si el sospechoso está silenciado, muestra un mensaje y no crea botones de pregunta.
        if profile["isSilenced"]:
             ttk.Label(self.question_buttons_frame, text=f"{name} se niega a hablar.", foreground="#e74c3c", font=('Inter', 12, 'bold')).pack(fill='x', padx=5, pady=10)
             return

        # Crea los 3 botones (Neutral, Emotional, Accusatory) con sus etiquetas y comandos.
        for type_key, q_data in profile["questions"].items():
            button = ttk.Button(self.question_buttons_frame, 
                                 text=f"[{type_key}] {q_data['label']}", 
                                 # El comando llama a 'interrogate_suspect' con la clave y el tipo de pregunta.
                                 command=lambda k=key, t=type_key: self.interrogate_suspect(k, t),
                                 style="TButton")
            
            # Empaqueta el botón para que ocupe todo el ancho.
            button.pack(fill='x', padx=5, pady=5)


    # Método principal de interacción: simula el interrogatorio.
    def interrogate_suspect(self, key: str, question_type: str):
        """Procesa el interrogatorio, actualiza la presión y genera el diálogo."""
        # Comprueba si el juego ha terminado.
        if self.game_over: 
             self.log_dialogue("[SISTEMA] El caso ya ha terminado. Por favor, reinicie.", "system")
             return

        name = key.capitalize()
        profile = SUSPECT_PROFILES[name]
        q_data = profile["questions"][question_type]
        
        # Chequeo doble por si acaso, para evitar interrogar a alguien silenciado.
        if profile["isSilenced"]:
            self.log_dialogue(f"[SISTEMA] {name} está silenciado y no responderá.", "system")
            return

        # 1. Registrar la pregunta del Detective en el diálogo.
        self.log_dialogue(f"[DETECTIVE] {q_data['label']}", "detective")
        
        # 2. Generar Diálogo y Aplicar Presión
        # Selecciona aleatoriamente una respuesta si el diálogo tiene más de una (aunque aquí solo tienen una).
        response_dialogue = random.choice(q_data["dialogue"])
        
        # Aplica el cambio de presión.
        profile["pressure"] += q_data["pressure_change"]
        # Limita la presión al rango [0, 100].
        profile["pressure"] = max(0, min(MAX_PRESSURE, profile["pressure"])) 
        
        # 3. Registrar la respuesta del Sospechoso.
        self.log_dialogue(response_dialogue, "suspect")

        # 4. Chequeo de Silencio (Si la presión llega al máximo)
        if profile["pressure"] >= MAX_PRESSURE:
            # Mensaje de sistema por castigo de silencio.
            self.log_dialogue(f"[SISTEMA] ¡El Detective ha forzado demasiado! {name} invoca su derecho a permanecer en silencio por {SILENCE_TIME_SECONDS} segundos.", "system")
            # Activa el estado de silencio.
            profile["isSilenced"] = True
            # Inicia el temporizador de castigo.
            profile["silencedTimer"] = SILENCE_TIME_SECONDS
            # Asegura que la presión se mantenga en 100.
            profile["pressure"] = MAX_PRESSURE
            # Deshabilita el botón del sospechoso.
            profile["button"].config(state=tk.DISABLED, style="TButton") 
            # Llama a select_suspect de nuevo para actualizar la UI con el temporizador de silencio.
            self.select_suspect(key) 
        else:
            # Si no hay silencio, solo actualiza la barra de presión.
            self._update_pressure_bar()


    # Método para insertar texto en el área de diálogo.
    def log_dialogue(self, text, tag):
        """Inserta texto en la consola de diálogo con formato de Novela Visual."""
        self.narrative_text.config(state=tk.NORMAL) # Habilita la edición temporalmente.
        # Elimina el nombre del sospechoso de la respuesta para que el color se aplique correctamente.
        if tag == "suspect":
            text = text.replace(self.current_suspect_key.capitalize() + ":", "")
            
        # Inserta el texto al final con el tag de formato (color/fuente).
        self.narrative_text.insert(tk.END, text + "\n\n", tag)
        # Hace scroll automáticamente hasta el final del texto.
        self.narrative_text.yview(tk.END)
        self.narrative_text.config(state=tk.DISABLED) # Deshabilita la edición de nuevo.


    # Método que se ejecuta al presionar el botón de acusación final.
    def make_accusation(self):
        """Procesa la acusación final del jugador. UNA SOLA OPORTUNIDAD."""
        if self.game_over:
            # Muestra un mensaje si el juego ya terminó.
            messagebox.showinfo("Juego Terminado", "El caso ya ha sido resuelto. Presione 'Iniciar Nuevo Caso'.")
            return
            
        # Obtiene las selecciones del jugador.
        acc_culprit = self.culprit_var.get()
        acc_weapon = self.weapon_var.get()
        acc_location = self.location_var.get()

        # Una vez hecha la acusación, el juego termina inmediatamente (la única oportunidad).
        self.game_over = True 
        
        # Comprueba si las tres variables seleccionadas coinciden con la verdad generada.
        if (acc_culprit == self.guilty_culprit and 
            acc_weapon == self.guilty_weapon and 
            acc_location == self.guilty_location):
            
            # Mensaje de victoria.
            message = "¡ACUSACIÓN CORRECTA! Ha resuelto el misterio."
            # Muestra el veredicto en la consola.
            self.log_dialogue("\n--- VEREDICTO DE LA CORTE ---", "header")
            self.log_dialogue(self.resolution_text, "suspect")
            # Llama a end_game con el color de victoria.
            self.end_game(message, "#2ecc71")
            
        else:
            # Acusación incorrecta: mensaje de derrota.
            message = (
                f"ACUSACIÓN INCORRECTA. La verdad era:\n"
                f"Culpable: {self.guilty_culprit}\n"
                f"Arma: {self.guilty_weapon}\n"
                f"Locación: {self.guilty_location}\n"
                f"El caso se cierra sin éxito policial."
            )
            # Llama a end_game con el color de derrota.
            self.end_game("¡ACUSACIÓN INCORRECTA! El caso queda sin resolver.", "#e74c3c")
            # Muestra la verdad en una ventana de mensaje.
            messagebox.showinfo("Caso Perdido", message)

    # Método para finalizar la partida.
    def end_game(self, message, color):
        """Detiene el tiempo y muestra el mensaje de fin de juego."""
        self.game_over = True
        # Cancela el temporizador para detener el bucle de actualización.
        if self.after_id:
            self.master.after_cancel(self.after_id)
        
        # Muestra el mensaje final en la etiqueta del temporizador.
        self.timer_label.config(text=message, foreground=color)
        # Deshabilita los botones de pregunta y selección.
        self._clear_question_buttons()
        for name in SUSPECT_PROFILES:
            if "button" in SUSPECT_PROFILES[name]:
                SUSPECT_PROFILES[name]["button"].config(state=tk.DISABLED)

# --- Bloque de ejecución principal ---
if __name__ == "__main__":
    # Crea la ventana principal (root).
    root = tk.Tk()
    # Crea e inicializa la aplicación del simulador dentro de la ventana.
    app = ClueSimulatorApp(root)
    # Inicia el bucle principal de Tkinter, que maneja los eventos y mantiene la ventana abierta.
    root.mainloop()