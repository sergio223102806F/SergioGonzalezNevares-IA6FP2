import json

# =========================================================================================
# 1. BASE DE CONOCIMIENTO (Knowledge Base) - Dataset de Automóviles
#    Se genera un dataset en Python (simulando la conexión a una BD)
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

# Diccionario para simular la persistencia de datos (JSON en este caso)
DATASET_FILENAME = "autos_knowledge_base.json"

def guardar_base_conocimiento(data):
    """Guarda el dataset en un archivo JSON."""
    try:
        with open(DATASET_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Base de Conocimiento guardada en '{DATASET_FILENAME}'.")
    except IOError as e:
        print(f"❌ Error al guardar la Base de Conocimiento: {e}")

# Ejecutar la función para generar el dataset utilizable
guardar_base_conocimiento(CAR_DATASET)

# =========================================================================================
# 2. SISTEMA EXPERTO (Inferencia y Base de Hechos)
# =========================================================================================

class ExpertSystem:
    """Clase principal del Sistema Experto para la recomendación de automóviles."""

    def __init__(self, knowledge_base):
        """Inicializa el sistema con la Base de Conocimiento."""
        self.knowledge_base = knowledge_base
        # Base de Hechos (Working Memory) - Se llena con la entrada del usuario
        self.facts = {}
        self.reasons = [] # Trazabilidad de la inferencia

    def _get_price_range(self, budget_level):
        """Asigna un rango de precios (Hard Constraint) basado en el nivel."""
        if budget_level == 'Bajo':
            return 0, 25000
        elif budget_level == 'Medio':
            return 25001, 45000
        elif budget_level == 'Alto':
            return 45001, float('inf')
        return 0, float('inf')

    def _get_use_tag(self, use):
        """Mapea el uso principal a un tag clave para la puntuación."""
        if use == "Deportivo": return "Velocidad"
        if use == "Urbano": return "Urbano"
        if use == "Trabajo": return "Carga"
        if use == "Aventura": return "Todoterreno"
        return "Familiar"

    def _score_car(self, car, primary_use_tag):
        """Aplica las reglas de puntuación (Soft Constraints - Gusto Personal) a un auto."""
        score = 0
        motor_pref = self.facts.get("motor_preferido", "Gasolina")
        estilo_pref = self.facts.get("estilo_preferido", "Clásico")

        # Regla 3.1: Preferencia de Motor (Eficiencia vs. Potencia)
        if motor_pref == 'Eléctrico' and car['electricidad']:
            score += 7
            self.reasons.append(f"  +7 pts: Coincidencia con la preferencia 'Eléctrico'.")
        elif motor_pref == 'Híbrido' and car['hibrido']:
            score += 5
            self.reasons.append(f"  +5 pts: Coincidencia con la preferencia 'Híbrido'.")
        elif motor_pref == 'Gasolina' and not car['hibrido'] and not car['electricidad']:
            score += 2
            self.reasons.append(f"  +2 pts: Coincidencia con motor 'Gasolina' tradicional.")

        # Regla 3.2: Estilo Personal
        if estilo_pref == car['estilo']:
            score += 4
            self.reasons.append(f"  +4 pts: Coincidencia con el estilo '{estilo_pref}'.")
        
        # Regla 3.3: Uso Principal
        if primary_use_tag in car['tags']:
            score += 3
            self.reasons.append(f"  +3 pts: El auto está etiquetado para el uso '{primary_use_tag}'.")

        # Regla de Bonus Implícita: Seguridad
        if car['seguridad'] == 5:
            score += 2
            self.reasons.append(f"  +2 pts: Bonus por máxima calificación de seguridad (5/5).")
            
        return score

    def inferir(self):
        """
        Motor de Inferencia.
        Aplica reglas (Hard y Soft) a la Base de Conocimiento usando la Base de Hechos.
        """
        self.reasons = [] # Limpiar razones
        autos_candidatos = self.knowledge_base
        
        print("\n--- 🧠 Motor de Inferencia Ejecutándose ---")

        # -----------------------------------------------------------------------
        # ETAPA 1: FILTRADO POR REGLAS RÍGIDAS (Hard Constraints)
        # -----------------------------------------------------------------------
        
        # REGLA 1: Presupuesto
        presupuesto_min, presupuesto_max = self._get_price_range(self.facts.get("presupuesto"))
        autos_filtrados = [
            car for car in autos_candidatos 
            if car["precio_min"] >= presupuesto_min and car["precio_min"] <= presupuesto_max
        ]
        self.reasons.append(f"✅ REGLA 1: Se aplicó filtro de presupuesto '{self.facts.get('presupuesto')}' (${presupuesto_min:,} - ${presupuesto_max:,}). Autos restantes: {len(autos_filtrados)}")

        # REGLA 2: Capacidad Mínima
        capacidad_minima = self.facts.get("capacidad_minima", 5)
        autos_filtrados = [
            car for car in autos_filtrados 
            if car["capacidad_max"] >= capacidad_minima
        ]
        self.reasons.append(f"✅ REGLA 2: Se aplicó filtro de capacidad mínima de {capacidad_minima} personas. Autos restantes: {len(autos_filtrados)}")
        
        if not autos_filtrados:
            return [], self.reasons # No hay autos que cumplan las restricciones básicas

        # -----------------------------------------------------------------------
        # ETAPA 2: PUNTUACIÓN POR REGLAS SUAVES (Soft Constraints - Gusto y Uso)
        # -----------------------------------------------------------------------
        
        primary_use_tag = self._get_use_tag(self.facts.get("uso_principal"))
        self.reasons.append(f"✨ Priorizando autos con el tag: '{primary_use_tag}' (Uso Principal: {self.facts.get('uso_principal')}).")
        
        scored_cars = []
        for car in autos_filtrados:
            car_reasons = []
            # Necesitamos re-implementar _score_car para que no use la lista reasons global
            score = self._score_car_detailed(car, primary_use_tag, car_reasons)
            scored_cars.append({
                "car": car,
                "score": score,
                "detail_reasons": car_reasons
            })
            
        # Ordenar por puntuación descendente
        scored_cars.sort(key=lambda x: x['score'], reverse=True)
        
        self.reasons.append(f"✅ REGLA FINAL: Autos puntuados y ordenados. Se recomiendan los 3 mejores.")

        return scored_cars[:3], self.reasons # Devolver solo el top 3

    def _score_car_detailed(self, car, primary_use_tag, car_reasons):
        """Versión detallada de puntuación para mostrar los puntos de cada auto."""
        score = 0
        motor_pref = self.facts.get("motor_preferido", "Gasolina")
        estilo_pref = self.facts.get("estilo_preferido", "Clásico")

        if motor_pref == 'Eléctrico' and car['electricidad']:
            score += 7
            car_reasons.append(" (+7) Coincide con motor Eléctrico.")
        elif motor_pref == 'Híbrido' and car['hibrido']:
            score += 5
            car_reasons.append(" (+5) Coincide con motor Híbrido.")
        elif motor_pref == 'Gasolina' and not car['hibrido'] and not car['electricidad']:
            score += 2
            car_reasons.append(" (+2) Coincide con motor Gasolina.")

        if estilo_pref == car['estilo']:
            score += 4
            car_reasons.append(f" (+4) Coincide con el estilo '{estilo_pref}'.")
        
        if primary_use_tag in car['tags']:
            score += 3
            car_reasons.append(f" (+3) El tag '{primary_use_tag}' coincide con el uso.")

        if car['seguridad'] == 5:
            score += 2
            car_reasons.append(" (+2) Máxima seguridad (5/5).")
            
        return score

# =========================================================================================
# 3. INTERFAZ DE USUARIO (Adquisición de Hechos)
# =========================================================================================

def get_user_facts(se):
    """Guía al usuario por el cuestionario para alimentar la Base de Hechos."""
    print("\n" + "="*50)
    print("  Bienvenido al Sistema Experto de Automóviles  ")
    print("="*50)

    # ETAPA 1: Presupuesto (Necesidad - Hard Constraint)
    print("\n--- ETAPA 1: Presupuesto (Hard Constraint) ---")
    budget_options = {
        '1': 'Bajo', '2': 'Medio', '3': 'Alto'
    }
    print("1. ¿Cuál es su rango de presupuesto?")
    print("   1) Bajo (Hasta $25,000)")
    print("   2) Medio ($25,000 a $45,000)")
    print("   3) Alto (Más de $45,000)")
    while True:
        choice = input("Ingrese el número de opción (1-3): ")
        if choice in budget_options:
            se.facts["presupuesto"] = budget_options[choice]
            break
        print("Opción inválida. Intente de nuevo.")

    # ETAPA 2: Capacidad y Uso (Necesidad y Restricción - Hard/Soft Constraint)
    print("\n--- ETAPA 2: Capacidad y Uso ---")
    
    while True:
        try:
            capacidad = int(input("2. ¿Cuál es el número MÍNIMO de asientos que necesita? (Ej: 2, 4, 5): "))
            if capacidad >= 2:
                se.facts["capacidad_minima"] = capacidad
                break
            print("Debe ingresar un número de asientos válido (mínimo 2).")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")

    use_options = {
        '1': 'Familiar', '2': 'Urbano', '3': 'Aventura', '4': 'Trabajo', '5': 'Deportivo'
    }
    print("3. ¿Cuál será el USO PRINCIPAL del vehículo?")
    print("   1) Familiar (Viajes, niños)")
    print("   2) Urbano (Ciudad, bajo consumo)")
    print("   3) Aventura (Todoterreno, caminos difíciles)")
    print("   4) Trabajo (Carga, remolque)")
    print("   5) Deportivo (Velocidad, desempeño)")
    while True:
        choice = input("Ingrese el número de opción (1-5): ")
        if choice in use_options:
            se.facts["uso_principal"] = use_options[choice]
            break
        print("Opción inválida. Intente de nuevo.")

    # ETAPA 3: Estilo y Motor (Gusto Personal - Soft Constraint)
    print("\n--- ETAPA 3: Gusto Personal y Estilo ---")
    
    style_options = {
        '1': 'Clásico', '2': 'Deportivo', '3': 'Moderno', '4': 'Robusto', '5': 'Único'
    }
    print("4. ¿Qué ESTILO visual prefiere?")
    print("   1) Clásico (Discreto, tradicional)")
    print("   2) Deportivo (Agresivo, aerodinámico)")
    print("   3) Moderno (Minimalista, futurista)")
    print("   4) Robusto (Grande, imponente)")
    print("   5) Único (Distintivo, retro)")
    while True:
        choice = input("Ingrese el número de opción (1-5): ")
        if choice in style_options:
            se.facts["estilo_preferido"] = style_options[choice]
            break
        print("Opción inválida. Intente de nuevo.")

    motor_options = {
        '1': 'Gasolina', '2': 'Híbrido', '3': 'Eléctrico'
    }
    print("5. ¿Qué tipo de MOTOR prefiere?")
    print("   1) Gasolina (Convencional)")
    print("   2) Híbrido (Eficiencia y autonomía)")
    print("   3) Eléctrico (Cero emisiones, tecnología)")
    while True:
        choice = input("Ingrese el número de opción (1-3): ")
        if choice in motor_options:
            se.facts["motor_preferido"] = motor_options[choice]
            break
        print("Opción inválida. Intente de nuevo.")
        
    print("\n--- Base de Hechos Completa. Iniciando Inferencia... ---")

def display_recommendations(scored_cars, reasons):
    """Muestra las recomendaciones finales y la trazabilidad del sistema."""
    print("\n" + "#"*60)
    print("###       RECOMENDACIONES FINALES DEL SISTEMA EXPERTO      ###")
    print("#"*60)

    if not scored_cars:
        print("\n😔 Lo sentimos, ningún automóvil en la Base de Conocimiento cumple con sus filtros rígidos (Presupuesto y Capacidad).")
        print("Por favor, reinicie el sistema y sea más flexible con las necesidades básicas.")
        return

    for i, item in enumerate(scored_cars):
        car = item['car']
        print(f"\n--- RECOMENDACIÓN #{i + 1} (Puntuación: {item['score']} pts) ---")
        print(f"Modelo: {car['modelo']} ({car['tipo_carroceria']} - {car['segmento']})")
        print(f"Precio: ${car['precio_min']:,}+")
        print(f"Capacidad: {car['capacidad_max']} personas")
        print(f"Motor: {'Eléctrico' if car['electricidad'] else 'Híbrido' if car['hibrido'] else 'Gasolina'}")
        print(f"Estilo: {car['estilo']}")
        
        # Muestra el detalle de la puntuación para este auto (Trazabilidad)
        print("\nDetalle de Puntuación:")
        for detail in item['detail_reasons']:
            print(f"  {detail}")

    print("\n" + "="*60)
    print("TRAZABILIDAD DEL PROCESO DE INFERENCIA (DEBUGGING DEL SE)")
    print("="*60)
    for reason in reasons:
        print(reason)
    print("="*60)


# =========================================================================================
# 4. PUNTO DE ENTRADA PRINCIPAL
# =========================================================================================

if __name__ == "__main__":
    # 1. Cargar/Inicializar la Base de Conocimiento (simula la BD)
    try:
        with open(DATASET_FILENAME, 'r', encoding='utf-8') as f:
            kb = json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{DATASET_FILENAME}'. Usando la lista predefinida.")
        kb = CAR_DATASET
    
    # 2. Inicializar el Sistema Experto
    sistema_experto = ExpertSystem(kb)
    
    # 3. Adquisición de Hechos (Interacción con el usuario)
    get_user_facts(sistema_experto)
    
    # 4. Ejecución del Motor de Inferencia
    top_recommendations, trazabilidad = sistema_experto.inferir()
    
    # 5. Presentación de Resultados
    display_recommendations(top_recommendations, trazabilidad)