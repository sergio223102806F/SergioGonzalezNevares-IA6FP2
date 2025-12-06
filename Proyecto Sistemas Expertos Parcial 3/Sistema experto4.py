import tkinter as tk
from tkinter import ttk, messagebox
import sys

# =========================================================================================
# 1. BASE DE CONOCIMIENTO (Knowledge Base) - Dataset de Automóviles
# =========================================================================================

CAR_DATASET = [
    {
        "modelo": "Toyota Corolla", "tipo_carroceria": "Sedán", "segmento": "Familiar",
        "precio_min": 22000, "consumo_ciudad": 7.5, "potencia_cv": 140, "seguridad": 5,
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Media", "hibrido": True,
        "electricidad": False, "tags": ["Confiabilidad", "Eficiencia", "Familiar", "Urbano"]
    },
    {
        "modelo": "Mazda CX-5", "tipo_carroceria": "SUV", "segmento": "Aventura",
        "precio_min": 28000, "consumo_ciudad": 9.0, "potencia_cv": 187, "seguridad": 5,
        "capacidad_max": 5, "estilo": "Deportivo", "tecnologia": "Alta", "hibrido": False,
        "electricidad": False, "tags": ["Diseño", "Lujo", "Espacioso", "Viajes"]
    },
    {
        "modelo": "Hyundai IONIQ 5", "tipo_carroceria": "Crossover", "segmento": "Tecnológico",
        "precio_min": 45000, "consumo_ciudad": 0.0, "potencia_cv": 225, "seguridad": 5,
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Muy Alta", "hibrido": False,
        "electricidad": True, "tags": ["Eléctrico", "Innovación", "Ecología", "Premium"]
    },
    {
        "modelo": "Honda CR-V", "tipo_carroceria": "SUV", "segmento": "Familiar",
        "precio_min": 30000, "consumo_ciudad": 8.5, "potencia_cv": 190, "seguridad": 5,
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Media", "hibrido": True,
        "electricidad": False, "tags": ["Confiabilidad", "Familiar", "Espacioso", "Híbrido"]
    },
    {
        "modelo": "Ford F-150", "tipo_carroceria": "Pick-up", "segmento": "Trabajo",
        "precio_min": 35000, "consumo_ciudad": 13.0, "potencia_cv": 325, "seguridad": 4,
        "capacidad_max": 5, "estilo": "Robusto", "tecnologia": "Media", "hibrido": False,
        "electricidad": False, "tags": ["Potencia", "Carga", "Todoterreno", "Trabajo"]
    },
    {
        "modelo": "Mini Cooper", "tipo_carroceria": "Hatchback", "segmento": "Urbano",
        "precio_min": 25000, "consumo_ciudad": 6.8, "potencia_cv": 134, "seguridad": 4,
        "capacidad_max": 4, "estilo": "Único", "tecnologia": "Alta", "hibrido": False,
        "electricidad": False, "tags": ["Compacto", "Estilo", "Urbano", "Ágil"]
    },
    {
        "modelo": "Porsche 911", "tipo_carroceria": "Coupé", "segmento": "Lujo",
        "precio_min": 100000, "consumo_ciudad": 12.5, "potencia_cv": 379, "seguridad": 5,
        "capacidad_max": 2, "estilo": "Deportivo", "tecnologia": "Muy Alta", "hibrido": False,
        "electricidad": False, "tags": ["Velocidad", "Exclusivo", "Alto-Rendimiento", "Lujo"]
    },
    {
        "modelo": "Dacia Sandero", "tipo_carroceria": "Hatchback", "segmento": "Económico",
        "precio_min": 12000, "consumo_ciudad": 6.0, "potencia_cv": 90, "seguridad": 3,
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Baja", "hibrido": False,
        "electricidad": False, "tags": ["Barato", "Ahorro", "Urbano", "Práctico"]
    },
]

# =========================================================================================
# 2. SISTEMA EXPERTO (Lógica y Motor de Inferencia)
# =========================================================================================

class ExpertSystem:
    """Clase principal para la recomendación de autos del Sistema Experto."""

    def __init__(self, knowledge_base):
        """Inicializa el sistema con la Base de Conocimiento."""
        self.knowledge_base = knowledge_base
        self.facts = {} # Memoria de trabajo (Base de Hechos)

    def _get_price_range(self, budget_level):
        """Mapea el nivel de presupuesto a un rango de precios (Restricción Rígida)."""
        if budget_level == 'Bajo':
            return 0, 25000
        elif budget_level == 'Medio':
            return 25001, 45000
        elif budget_level == 'Alto':
            return 45001, float('inf')
        return 0, float('inf')

    def _get_use_tag(self, use):
        """Mapea el uso principal a una etiqueta clave para la puntuación."""
        if use == "Deportivo": return "Velocidad"
        if use == "Urbano": return "Urbano"
        if use == "Trabajo": return "Trabajo" 
        if use == "Aventura": return "Todoterreno"
        if use == "Familiar": return "Familiar"
        return "Familiar"

    def _format_currency(self, amount):
        """Formatea la cantidad como moneda (estilo de localización español)."""
        if amount == float('inf'):
            return '∞'
        # Formato con separadores de miles y signo de dólar
        return f"${amount:,.0f}".replace(',', '_').replace('.', ',').replace('_', '.')

    def _score_car_detailed(self, car, primary_use_tag, car_reasons):
        """
        Aplica reglas de puntuación (Restricciones Suaves) a un auto, detallando las razones
        con argumentos más elaborados y concisos.
        """
        score = 0
        motor_pref = self.facts.get("motor_preferido", "Gasolina")
        estilo_pref = self.facts.get("estilo_preferido", "Clásico")
        uso_principal = self.facts.get("uso_principal", "Familiar")

        # Rule 3.1: Preferencia de Motor (Eficiencia vs. Potencia)
        if motor_pref == 'Eléctrico' and car['electricidad']:
            score += 7
            # JUSTIFICACIÓN CORTA Y DIRECTA
            car_reasons.append(f"Motor Eléctrico: Cumple su preferencia de cero emisiones, innovación y bajo coste operativo. (+7 Ptos)")
        elif motor_pref == 'Híbrido' and car['hibrido']:
            score += 5
            # JUSTIFICACIÓN CORTA Y DIRECTA
            car_reasons.append(f"Motor Híbrido: Combina motores para máxima eficiencia en ciudad y flexibilidad de autonomía. (+5 Ptos)")
        elif motor_pref == 'Gasolina' and not car['hibrido'] and not car['electricidad']:
            score += 2
            # JUSTIFICACIÓN CORTA Y DIRECTA
            car_reasons.append(f"Motor Gasolina: Ofrece mayor potencia disponible, menor coste de adquisición y mantenimiento simple. (+2 Ptos)")

        # Rule 3.2: Estilo Personal
        if estilo_pref == car['estilo']:
            score += 4
            # JUSTIFICACIÓN CORTA Y DIRECTA
            car_reasons.append(f"Estilo '{car['estilo']}': Se alinea con su preferencia estética. (+4 Ptos)")
            
        # Rule 3.3: Uso Principal (se puntúa más si el tag clave está presente)
        if primary_use_tag in car['tags']:
            score += 3
            # JUSTIFICACIÓN CORTA Y DIRECTA
            car_reasons.append(f"Enfoque Principal: Está optimizado para su uso clave de '{uso_principal}'. (+3 Ptos)")

        # Regla Implícita de Bonificación: Seguridad
        if car['seguridad'] == 5:
            score += 2
            # JUSTIFICACIÓN CORTA Y DIRECTA
            car_reasons.append(f"Seguridad 5/5: Obtiene la máxima calificación de seguridad, crucial para su tranquilidad. (+2 Ptos)")
            
        return score

    def inferir(self, facts):
        """
        Motor de Inferencia.
        Aplica Reglas Rígidas para filtrar y Reglas Suaves para puntuar.
        """
        self.facts = facts
        trazabilidad = []
        autos_candidatos = self.knowledge_base
        
        # -----------------------------------------------------------------------
        # PASO 1: FILTRADO POR RESTRICCIONES RÍGIDAS
        # -----------------------------------------------------------------------
        
        # REGLA 1: Presupuesto
        presupuesto_min, presupuesto_max = self._get_price_range(self.facts.get("presupuesto"))
        autos_filtrados = [
            car for car in autos_candidatos 
            if car["precio_min"] >= presupuesto_min and car["precio_min"] <= presupuesto_max
        ]
        trazabilidad.append(f"REGLA 1: Presupuesto '{self.facts.get('presupuesto')}' ({self._format_currency(presupuesto_min)} - {self._format_currency(presupuesto_max)}). Autos restantes: {len(autos_filtrados)}")

        # REGLA 2: Capacidad Mínima
        capacidad_minima = self.facts.get("capacidad_minima", 5)
        autos_filtrados = [
            car for car in autos_filtrados 
            if car["capacidad_max"] >= capacidad_minima
        ]
        trazabilidad.append(f"REGLA 2: Capacidad mínima de {capacidad_minima} personas. Autos restantes: {len(autos_filtrados)}")
        
        if not autos_filtrados:
            return {"recommendations": [], "trazabilidad": trazabilidad}

        # -----------------------------------------------------------------------
        # PASO 2: PUNTUACIÓN POR RESTRICCIONES SUAVES
        # -----------------------------------------------------------------------
        
        primary_use_tag = self._get_use_tag(self.facts.get("uso_principal"))
        trazabilidad.append(f"REGLA 3: Priorizando autos con el tag clave: '{primary_use_tag}' (Uso Principal: {self.facts.get('uso_principal')}).")
        
        scored_cars = []
        for car in autos_filtrados:
            car_reasons = []
            score = self._score_car_detailed(car, primary_use_tag, car_reasons)
            scored_cars.append({
                "car": car,
                "score": score,
                "detail_reasons": car_reasons
            })
            
        # Ordenar por puntuación descendente
        scored_cars.sort(key=lambda x: x['score'], reverse=True)
        
        # Devolver solo los 3 mejores
        return {"recommendations": scored_cars[:3], "trazabilidad": trazabilidad} 


# =========================================================================================
# 3. INTERFAZ GRÁFICA (Tkinter)
# =========================================================================================

class CarExpertSystemApp:
    def __init__(self, master):
        self.master = master
        master.title("Sistema Experto de Recomendación de Autos (Python)")
        
        # --- Configuración de Estilos (Estética Mejorada) ---
        self._setup_styles()
        
        # Configurar el marco principal
        # Usamos un color de fondo limpio
        main_frame = ttk.Frame(master, padding="20 20 20 20", style='Main.TFrame')
        main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.config(bg='#FAFAFA') # Fondo de la ventana principal

        # Instancia del Sistema Experto
        self.expert_system = ExpertSystem(CAR_DATASET)

        # --- Variables para Hechos (Base de Hechos) ---
        self.presupuesto_var = tk.StringVar(master, value="Medio")
        self.uso_principal_var = tk.StringVar(master, value="Familiar")
        self.estilo_preferido_var = tk.StringVar(master, value="Clásico")
        self.motor_preferido_var = tk.StringVar(master, value="Gasolina")
        self.capacidad_var = tk.IntVar(master, value=5)

        # --- Configuración del Layout de la GUI ---
        row_idx = 0

        # Título
        ttk.Label(main_frame, text="🚗 Sistema Experto de Autos", style='Header.TLabel').grid(column=0, row=row_idx, columnspan=3, pady=(0, 20))
        row_idx += 1

        # Marco para las preguntas (mejor agrupación visual)
        questions_frame = ttk.Frame(main_frame, padding="15", style='QuestionFrame.TFrame')
        questions_frame.grid(column=0, row=row_idx, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        for col in range(3):
            questions_frame.columnconfigure(col, weight=1)

        q_row_idx = 0
        
        # --- Pregunta 1: Presupuesto (Restricción Rígida) ---
        ttk.Label(questions_frame, text="1. Presupuesto (Restricción Rígida):", style='Question.TLabel').grid(column=0, row=q_row_idx, sticky=tk.W, columnspan=3, pady=(5, 2))
        q_row_idx += 1
        budget_options = ["Bajo", "Medio", "Alto"]
        for i, option in enumerate(budget_options):
            ttk.Radiobutton(questions_frame, text=f"{option} ({self._get_budget_range_text(option)})", variable=self.presupuesto_var, value=option, style='Standard.TRadiobutton').grid(column=i, row=q_row_idx, sticky=tk.W, padx=5, pady=2)
        q_row_idx += 1

        # --- Pregunta 2: Capacidad Mínima (Restricción Rígida) ---
        ttk.Separator(questions_frame, orient='horizontal').grid(column=0, row=q_row_idx, columnspan=3, sticky="ew", pady=10)
        q_row_idx += 1
        ttk.Label(questions_frame, text="2. Capacidad Mínima (Restricción Rígida):", style='Question.TLabel').grid(column=0, row=q_row_idx, sticky=tk.W, pady=(5, 5))
        
        capacity_group = ttk.Frame(questions_frame, style='Main.TFrame')
        capacity_group.grid(column=1, row=q_row_idx, columnspan=2, sticky=tk.W)
        
        self.capacidad_entry = ttk.Entry(capacity_group, textvariable=self.capacidad_var, width=5, style='TEntry')
        self.capacidad_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(capacity_group, text="personas", style='Standard.TLabel').pack(side=tk.LEFT)
        q_row_idx += 1
        
        # --- Pregunta 3: Uso Principal (Restricción Suave) ---
        ttk.Separator(questions_frame, orient='horizontal').grid(column=0, row=q_row_idx, columnspan=3, sticky="ew", pady=10)
        q_row_idx += 1
        ttk.Label(questions_frame, text="3. Uso Principal (Restricción Suave):", style='Question.TLabel').grid(column=0, row=q_row_idx, sticky=tk.W, columnspan=3, pady=(5, 2))
        q_row_idx += 1
        use_options = ["Familiar", "Urbano", "Aventura", "Trabajo", "Deportivo"]
        for i, text in enumerate(use_options):
            col = i % 3
            row = q_row_idx + (i // 3)
            ttk.Radiobutton(questions_frame, text=text, variable=self.uso_principal_var, value=text, style='Standard.TRadiobutton').grid(column=col, row=row, sticky=tk.W, padx=5, pady=2)
        q_row_idx += 2 

        # --- Pregunta 4: Estilo Preferido (Restricción Suave) ---
        ttk.Separator(questions_frame, orient='horizontal').grid(column=0, row=q_row_idx, columnspan=3, sticky="ew", pady=10)
        q_row_idx += 1
        ttk.Label(questions_frame, text="4. Estilo Preferido (Restricción Suave):", style='Question.TLabel').grid(column=0, row=q_row_idx, sticky=tk.W, columnspan=3, pady=(5, 2))
        q_row_idx += 1
        style_options = ["Clásico", "Deportivo", "Moderno", "Robusto", "Único"]
        for i, option in enumerate(style_options):
            col = i % 3
            row = q_row_idx + (i // 3)
            ttk.Radiobutton(questions_frame, text=option, variable=self.estilo_preferido_var, value=option, style='Standard.TRadiobutton').grid(column=col, row=row, sticky=tk.W, padx=5, pady=2)
        q_row_idx += 2 

        # --- Pregunta 5: Motor Preferido (Restricción Suave) ---
        ttk.Separator(questions_frame, orient='horizontal').grid(column=0, row=q_row_idx, columnspan=3, sticky="ew", pady=10)
        q_row_idx += 1
        ttk.Label(questions_frame, text="5. Motor Preferido (Restricción Suave):", style='Question.TLabel').grid(column=0, row=q_row_idx, sticky=tk.W, columnspan=3, pady=(5, 2))
        q_row_idx += 1
        motor_options = ["Gasolina", "Híbrido", "Eléctrico"]
        for i, option in enumerate(motor_options):
            ttk.Radiobutton(questions_frame, text=option, variable=self.motor_preferido_var, value=option, style='Standard.TRadiobutton').grid(column=i, row=q_row_idx, sticky=tk.W, padx=5, pady=2)
        
        row_idx += 1 # Salta la fila del marco de preguntas

        # --- Botón de Inferencia ---
        ttk.Button(main_frame, text="Obtener Recomendaciones", command=self.run_inference, style='Accent.TButton').grid(column=0, row=row_idx, columnspan=3, pady=25)
        row_idx += 1

        # --- Sección de Resultados ---
        ttk.Label(main_frame, text="Resultados de Inferencia:", style='ResultHeader.TLabel').grid(column=0, row=row_idx, sticky=tk.W, columnspan=3, pady=(10, 5))
        row_idx += 1

        # Marco para el widget de texto de resultados
        self.results_frame = ttk.Frame(main_frame, padding="10", relief="solid", borderwidth=1, style='ResultFrame.TFrame')
        self.results_frame.grid(column=0, row=row_idx, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        
        # El widget de texto es donde se ve el resultado (fuente monospace para alineación)
        self.results_text = tk.Text(self.results_frame, height=15, width=70, state='disabled', wrap=tk.WORD, font=('Consolas', 10) if sys.platform.startswith('win') else ('Monospace', 10), bd=0, relief=tk.FLAT, bg='#F0F0F0', fg='#333333')
        self.results_text.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Barra de desplazamiento para resultados
        vsb = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_text.yview, style='TScrollbar')
        vsb.grid(column=1, row=0, sticky='ns')
        self.results_text.configure(yscrollcommand=vsb.set)

    def _setup_styles(self):
        """Configura los estilos estéticos de la aplicación."""
        style = ttk.Style()

        # Paleta de Colores
        COLOR_PRIMARY = '#1E3A8A'  # Deep Blue (Oscuro)
        COLOR_ACCENT = '#F97316'   # Orange (Acento)
        COLOR_BACKGROUND = '#FAFAFA' # Near White
        COLOR_FRAME = '#E0E0E0'      # Light Gray for borders
        
        # Configuración del Fondo Base
        style.configure('Main.TFrame', background=COLOR_BACKGROUND)
        style.configure('Standard.TLabel', background=COLOR_BACKGROUND, foreground='#333333', font=('Arial', 10))
        style.configure('Standard.TRadiobutton', background=COLOR_BACKGROUND, foreground='#333333', font=('Arial', 10))
        
        # Estilos de Headers y Títulos
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), foreground=COLOR_PRIMARY, background=COLOR_BACKGROUND)
        style.configure('Question.TLabel', font=('Arial', 10, 'bold'), foreground='#333333', background=COLOR_BACKGROUND)
        style.configure('ResultHeader.TLabel', font=('Arial', 12, 'bold'), foreground=COLOR_PRIMARY, background=COLOR_BACKGROUND)

        # Estilo para el Marco de Preguntas (Con borde y un fondo ligeramente diferente)
        style.configure('QuestionFrame.TFrame', background='#FFFFFF', relief='flat', borderwidth=1, bordercolor=COLOR_FRAME)
        style.map('QuestionFrame.TFrame', bordercolor=[('active', COLOR_ACCENT)])

        # Estilo del Marco de Resultados
        style.configure('ResultFrame.TFrame', background='#F0F0F0', bordercolor=COLOR_FRAME)

        # Estilo del Botón de Acción (Color de acento)
        style.configure('Accent.TButton', 
                        font=('Arial', 11, 'bold'), 
                        foreground='#FFFFFF', 
                        background=COLOR_ACCENT, 
                        padding=(15, 8, 15, 8),
                        relief='flat')
        
        # Mapeo del botón para el efecto de "hover" o presionado
        style.map('Accent.TButton', 
                  background=[('active', COLOR_ACCENT), ('!disabled', COLOR_ACCENT)],
                  foreground=[('active', '#FFFFFF')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'flat')])
        
        # Estilo de la barra de desplazamiento
        style.configure('TScrollbar', troughcolor=COLOR_BACKGROUND, background=COLOR_PRIMARY)
        
        # Estilo para los Entry widgets
        style.configure('TEntry', fieldbackground='#FFFFFF', bordercolor=COLOR_FRAME)


    def _get_budget_range_text(self, option):
        """Función auxiliar para mostrar los rangos de precios junto a los botones de radio."""
        if option == 'Bajo': return "Hasta $25.000"
        if option == 'Medio': return "$25.001 - $45.000"
        if option == 'Alto': return "Más de $45.000"
        return ""

    def _get_current_facts(self):
        """Recopila hechos de las variables de la GUI y realiza una validación básica."""
        try:
            facts = {
                "presupuesto": self.presupuesto_var.get(),
                "capacidad_minima": self.capacidad_var.get(),
                "uso_principal": self.uso_principal_var.get(),
                "estilo_preferido": self.estilo_preferido_var.get(),
                "motor_preferido": self.motor_preferido_var.get(),
            }
            
            if any(not facts[key] for key in ["presupuesto", "uso_principal", "estilo_preferido", "motor_preferido"]):
                raise ValueError("Complete todas las opciones de selección.")
            
            if facts["capacidad_minima"] < 2:
                raise ValueError("La capacidad mínima debe ser 2 o más.")

            return facts

        except tk.TclError:
            raise ValueError("Asegúrese de que la capacidad sea un número válido.")
        except ValueError as e:
            raise e

    def run_inference(self):
        """Manejador para el botón 'Obtener Recomendaciones'."""
        try:
            facts = self._get_current_facts()
            
            # Ejecutar motor de inferencia
            result = self.expert_system.inferir(facts)
            
            # Mostrar resultados
            self.display_results(result)

        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error del Sistema", f"Ocurrió un error inesperado: {str(e)}")

    def display_results(self, result):
        """Formatea y muestra las recomendaciones y la trazabilidad."""
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END) # Limpiar contenido previo

        recommendations = result.get("recommendations", [])
        trazabilidad = result.get("trazabilidad", [])

        if not recommendations:
            self.results_text.insert(tk.END, "😔 Sin Resultados.\n\n", 'tag_error')
            self.results_text.insert(tk.END, "Ningún auto cumple con los filtros rígidos (Presupuesto y Capacidad mínima de asientos). Pruebe a cambiar sus requisitos.\n", 'tag_error_detail')
        else:
            self.results_text.insert(tk.END, "--- TOP 3 RECOMENDACIONES DE AUTOS ---\n\n", 'tag_header')
            
            for i, item in enumerate(recommendations):
                car = item['car']
                self.results_text.insert(tk.END, f"{i + 1}. {car['modelo']} ({item['score']} Puntos)\n", 'tag_model')
                self.results_text.insert(tk.END, f"    Precio Mínimo: {self.expert_system._format_currency(car['precio_min'])}\n")
                
                motor_type = 'Eléctrico' if car['electricidad'] else 'Híbrido' if car['hibrido'] else 'Gasolina'
                self.results_text.insert(tk.END, f"    Tipo: {car['tipo_carroceria']}, Motor: {motor_type}\n")
                
                self.results_text.insert(tk.END, "    Motivos de Inclusión:\n", 'tag_reasons')
                for reason in item['detail_reasons']:
                    # Se inserta la razón directamente, ya que está formateada en _score_car_detailed
                    self.results_text.insert(tk.END, f"      - {reason}\n") 
                self.results_text.insert(tk.END, "\n")
            
            self.results_text.insert(tk.END, "\n--- TRAZABILIDAD DE LA INFERENCIA ---\n", 'tag_header_trace')
            for line in trazabilidad:
                self.results_text.insert(tk.END, f"> {line}\n", 'tag_trace')
        
        self.results_text.config(state='disabled')

        # Configuración de etiquetas para estilizar la salida de texto
        self.results_text.tag_config('tag_header', font=('Arial', 11, 'bold'), foreground='#1E3A8A')
        self.results_text.tag_config('tag_model', font=('Arial', 11, 'bold'), foreground='#10B981') # Tono verde para autos recomendados
        self.results_text.tag_config('tag_reasons', font=('Arial', 10, 'italic'), foreground='#374151')
        self.results_text.tag_config('tag_header_trace', font=('Arial', 11, 'bold'), foreground='#9333EA') # Morado para trazabilidad
        self.results_text.tag_config('tag_trace', font=('Consolas', 9) if sys.platform.startswith('win') else ('Monospace', 9), foreground='#6B7280')
        self.results_text.tag_config('tag_error', font=('Arial', 11, 'bold'), foreground='#DC2626')
        self.results_text.tag_config('tag_error_detail', font=('Arial', 10), foreground='#DC2626')


if __name__ == "__main__":
    root = tk.Tk()
    app = CarExpertSystemApp(root)
    root.mainloop()
