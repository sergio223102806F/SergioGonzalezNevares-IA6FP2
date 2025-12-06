import tkinter as tk # Importa la librería principal de Tkinter para la GUI
from tkinter import ttk, messagebox # Importa widgets temáticos, y cajas de diálogo
import sys # Importa funciones y variables específicas del sistema (no usado directamente en la KB)

# =========================================================================================
# 1. BASE DE CONOCIMIENTO (Knowledge Base) - Dataset de Automóviles (60 Opciones) # Define la estructura del dataset de coches
# =========================================================================================

CAR_DATASET = [ # Inicio del array que contiene todos los datos de los vehículos
    # ----------------------------------------------------
    # 1. Económicos y Urbanos (10) # Comienzo de la sección de coches urbanos y económicos
    # ----------------------------------------------------
    { # Primer coche: Dacia Sandero
        "modelo": "Dacia Sandero", "tipo_carroceria": "Hatchback", "segmento": "Económico", # Nombre, tipo de carrocería y segmento
        "precio_min": 12000, "consumo_ciudad": 6.0, "potencia_cv": 90, "seguridad": 3, # Datos numéricos (precio, consumo, potencia, seguridad)
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Baja", "hibrido": False, # Capacidad, estilo, nivel de tecnología, si es híbrido
        "electricidad": False, "tags": ["Barato", "Ahorro", "Urbano", "Práctico"] # Si es eléctrico y etiquetas descriptivas
    },
    { # Renault Clio
        "modelo": "Renault Clio", "tipo_carroceria": "Hatchback", "segmento": "Urbano", # Nombre, tipo de carrocería y segmento
        "precio_min": 16500, "consumo_ciudad": 5.5, "potencia_cv": 100, "seguridad": 4, # Datos numéricos
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Media", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Eficiencia", "Ágil", "Urbano", "Híbrido"] # Etiquetas
    },
    { # Hyundai i10
        "modelo": "Hyundai i10", "tipo_carroceria": "Hatchback", "segmento": "Compacto", # Nombre, tipo de carrocería y segmento
        "precio_min": 15000, "consumo_ciudad": 5.8, "potencia_cv": 84, "seguridad": 4, # Datos numéricos
        "capacidad_max": 4, "estilo": "Moderno", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Compacto", "Urbano", "Maniobrable", "Eficiencia"] # Etiquetas
    },
    { # Toyota Aygo X
        "modelo": "Toyota Aygo X", "tipo_carroceria": "Crossover", "segmento": "Urbano", # Nombre, tipo de carrocería y segmento
        "precio_min": 17500, "consumo_ciudad": 5.0, "potencia_cv": 72, "seguridad": 4, # Datos numéricos
        "capacidad_max": 4, "estilo": "Único", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Compacto", "Estilo", "Urbano", "Eficiencia"] # Etiquetas
    },
    { # Citroën C3
        "modelo": "Citroën C3", "tipo_carroceria": "Hatchback", "segmento": "Económico", # Nombre, tipo de carrocería y segmento
        "precio_min": 14000, "consumo_ciudad": 6.2, "potencia_cv": 83, "seguridad": 3, # Datos numéricos
        "capacidad_max": 5, "estilo": "Único", "tecnologia": "Baja", "hibrido": False, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Barato", "Confort", "Práctico", "Urbano"] # Etiquetas
    },
    { # Fiat 500
        "modelo": "Fiat 500", "tipo_carroceria": "Hatchback", "segmento": "Urbano", # Nombre, tipo de carrocería y segmento
        "precio_min": 18000, "consumo_ciudad": 5.3, "potencia_cv": 70, "seguridad": 4, # Datos numéricos
        "capacidad_max": 4, "estilo": "Clásico", "tecnologia": "Media", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Estilo", "Compacto", "Urbano", "Híbrido"] # Etiquetas
    },
    { # Kia Picanto
        "modelo": "Kia Picanto", "tipo_carroceria": "Hatchback", "segmento": "Compacto", # Nombre, tipo de carrocería y segmento
        "precio_min": 13000, "consumo_ciudad": 6.5, "potencia_cv": 67, "seguridad": 3, # Datos numéricos
        "capacidad_max": 4, "estilo": "Moderno", "tecnologia": "Baja", "hibrido": False, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Compacto", "Barato", "Urbano", "Ahorro"] # Etiquetas
    },
    { # Volkswagen Polo
        "modelo": "Volkswagen Polo", "tipo_carroceria": "Hatchback", "segmento": "Urbano", # Nombre, tipo de carrocería y segmento
        "precio_min": 20000, "consumo_ciudad": 5.7, "potencia_cv": 95, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Calidad", "Urbano", "Confiabilidad", "Eficiencia"] # Etiquetas
    },
    { # Skoda Fabia
        "modelo": "Skoda Fabia", "tipo_carroceria": "Hatchback", "segmento": "Económico", # Nombre, tipo de carrocería y segmento
        "precio_min": 17000, "consumo_ciudad": 5.9, "potencia_cv": 110, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Espacioso", "Práctico", "Urbano", "Seguridad"] # Etiquetas
    },
    { # Peugeot 208
        "modelo": "Peugeot 208", "tipo_carroceria": "Hatchback", "segmento": "Urbano", # Nombre, tipo de carrocería y segmento
        "precio_min": 19500, "consumo_ciudad": 6.1, "potencia_cv": 100, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Deportivo", "tecnologia": "Alta", "hibrido": False, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Diseño", "Ágil", "Urbano", "Tecnología"] # Etiquetas
    },

    # ----------------------------------------------------
    # 2. Sedanes y Familiares (10) # Comienzo de la sección de Sedanes y Familiares
    # ----------------------------------------------------
    { # Toyota Corolla
        "modelo": "Toyota Corolla", "tipo_carroceria": "Sedán", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 22000, "consumo_ciudad": 7.5, "potencia_cv": 140, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Media", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Confiabilidad", "Eficiencia", "Familiar", "Urbano"] # Etiquetas
    },
    { # Skoda Octavia
        "modelo": "Skoda Octavia", "tipo_carroceria": "Sedán", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 28000, "consumo_ciudad": 6.5, "potencia_cv": 150, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Alta", "hibrido": False, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Espacioso", "Práctico", "Viajes", "Calidad"] # Etiquetas
    },
    { # Mazda 3
        "modelo": "Mazda 3", "tipo_carroceria": "Sedán", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 24000, "consumo_ciudad": 7.0, "potencia_cv": 155, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Deportivo", "tecnologia": "Alta", "hibrido": False, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Diseño", "Manejo", "Familiar", "Lujo"] # Etiquetas
    },
    { # Hyundai Elantra
        "modelo": "Hyundai Elantra", "tipo_carroceria": "Sedán", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 21000, "consumo_ciudad": 7.2, "potencia_cv": 147, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Valor", "Diseño", "Confort", "Familiar"] # Etiquetas
    },
    { # Audi A4
        "modelo": "Audi A4", "tipo_carroceria": "Sedán", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 42000, "consumo_ciudad": 9.5, "potencia_cv": 204, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Muy Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Premium", "Lujo", "Tecnología", "Viajes"] # Etiquetas
    },
    { # BMW Serie 3
        "modelo": "BMW Serie 3", "tipo_carroceria": "Sedán", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 45000, "consumo_ciudad": 10.0, "potencia_cv": 255, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Deportivo", "tecnologia": "Muy Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Rendimiento", "Lujo", "Deportivo", "Viajes"] # Etiquetas
    },
    { # Mercedes-Benz Clase C
        "modelo": "Mercedes-Benz Clase C", "tipo_carroceria": "Sedán", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 47000, "consumo_ciudad": 10.5, "potencia_cv": 255, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Muy Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Exclusivo", "Confort", "Lujo", "Tecnología"] # Etiquetas
    },
    { # Tesla Model 3
        "modelo": "Tesla Model 3", "tipo_carroceria": "Sedán", "segmento": "Tecnológico", # Nombre, tipo de carrocería y segmento
        "precio_min": 40000, "consumo_ciudad": 0.0, "potencia_cv": 283, "seguridad": 5, # Datos numéricos (consumo 0.0 por ser eléctrico)
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Innovación", "Rendimiento", "Viajes"] # Etiquetas
    },
    { # Volvo S60
        "modelo": "Volvo S60", "tipo_carroceria": "Sedán", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 39000, "consumo_ciudad": 8.0, "potencia_cv": 250, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Seguridad", "Lujo", "Confort", "Híbrido"] # Etiquetas
    },
    { # Honda Accord
        "modelo": "Honda Accord", "tipo_carroceria": "Sedán", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 32000, "consumo_ciudad": 7.8, "potencia_cv": 192, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Media", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Confiabilidad", "Espacioso", "Familiar", "Híbrido"] # Etiquetas
    },
    
    # ----------------------------------------------------
    # 3. SUVs Compactos y Crossovers (15) # Comienzo de la sección de SUVs Compactos y Crossovers
    # ----------------------------------------------------
    { # Mazda CX-5
        "modelo": "Mazda CX-5", "tipo_carroceria": "SUV", "segmento": "Aventura", # Nombre, tipo de carrocería y segmento
        "precio_min": 28000, "consumo_ciudad": 9.0, "potencia_cv": 187, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Deportivo", "tecnologia": "Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Diseño", "Lujo", "Espacioso", "Viajes"] # Etiquetas
    },
    { # Honda CR-V
        "modelo": "Honda CR-V", "tipo_carroceria": "SUV", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 30000, "consumo_ciudad": 8.5, "potencia_cv": 190, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Media", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Confiabilidad", "Familiar", "Espacioso", "Híbrido"] # Etiquetas
    },
    { # Nissan Qashqai
        "modelo": "Nissan Qashqai", "tipo_carroceria": "Crossover", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 26000, "consumo_ciudad": 8.2, "potencia_cv": 158, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Media", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Urbano", "Familiar", "Tecnología", "Híbrido"] # Etiquetas
    },
    { # Kia Sportage
        "modelo": "Kia Sportage", "tipo_carroceria": "SUV", "segmento": "Aventura", # Nombre, tipo de carrocería y segmento
        "precio_min": 29000, "consumo_ciudad": 8.8, "potencia_cv": 177, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Diseño", "Garantía", "Espacioso", "Viajes"] # Etiquetas
    },
    { # Toyota RAV4
        "modelo": "Toyota RAV4", "tipo_carroceria": "SUV", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 31000, "consumo_ciudad": 7.9, "potencia_cv": 203, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Media", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Confiabilidad", "Híbrido", "Aventura", "Familiar"] # Etiquetas
    },
    { # Hyundai Tucson
        "modelo": "Hyundai Tucson", "tipo_carroceria": "SUV", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 27500, "consumo_ciudad": 8.0, "potencia_cv": 180, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Diseño", "Tecnología", "Familiar", "Híbrido"] # Etiquetas
    },
    { # Volkswagen Tiguan
        "modelo": "Volkswagen Tiguan", "tipo_carroceria": "SUV", "segmento": "Aventura", # Nombre, tipo de carrocería y segmento
        "precio_min": 32000, "consumo_ciudad": 9.2, "potencia_cv": 184, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Calidad", "Espacioso", "Viajes", "Aventura"] # Etiquetas
    },
    { # Subaru Forester
        "modelo": "Subaru Forester", "tipo_carroceria": "SUV", "segmento": "Aventura", # Nombre, tipo de carrocería y segmento
        "precio_min": 33000, "consumo_ciudad": 9.8, "potencia_cv": 182, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Robusto", "tecnologia": "Media", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Todoterreno", "Seguridad", "Aventura", "Híbrido"] # Etiquetas
    },
    { # Jeep Compass
        "modelo": "Jeep Compass", "tipo_carroceria": "SUV", "segmento": "Aventura", # Nombre, tipo de carrocería y segmento
        "precio_min": 29500, "consumo_ciudad": 10.5, "potencia_cv": 177, "seguridad": 4, # Datos numéricos
        "capacidad_max": 5, "estilo": "Robusto", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Todoterreno", "Diseño", "Aventura", "Viajes"] # Etiquetas
    },
    { # Peugeot 3008
        "modelo": "Peugeot 3008", "tipo_carroceria": "SUV", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 31500, "consumo_ciudad": 8.3, "potencia_cv": 130, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Deportivo", "tecnologia": "Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Diseño", "Confort", "Híbrido", "Familiar"] # Etiquetas
    },
    { # Ford Kuga
        "modelo": "Ford Kuga", "tipo_carroceria": "SUV", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 30500, "consumo_ciudad": 8.1, "potencia_cv": 150, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Media", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Manejo", "Familiar", "Híbrido", "Espacioso"] # Etiquetas
    },
    { # Opel Mokka
        "modelo": "Opel Mokka", "tipo_carroceria": "Crossover", "segmento": "Urbano", # Nombre, tipo de carrocería y segmento
        "precio_min": 24000, "consumo_ciudad": 7.0, "potencia_cv": 130, "seguridad": 4, # Datos numéricos
        "capacidad_max": 5, "estilo": "Único", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Compacto", "Estilo", "Urbano", "Diseño"] # Etiquetas
    },
    { # Cupra Formentor
        "modelo": "Cupra Formentor", "tipo_carroceria": "Crossover", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 35000, "consumo_ciudad": 9.5, "potencia_cv": 245, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Deportivo", "tecnologia": "Muy Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Rendimiento", "Diseño", "Lujo", "Velocidad"] # Etiquetas
    },
    { # Mini Countryman
        "modelo": "Mini Countryman", "tipo_carroceria": "Crossover", "segmento": "Aventura", # Nombre, tipo de carrocería y segmento
        "precio_min": 34000, "consumo_ciudad": 8.6, "potencia_cv": 136, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Único", "tecnologia": "Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Estilo", "Compacto", "Híbrido", "Aventura"] # Etiquetas
    },
    { # Chevrolet Tracker
        "modelo": "Chevrolet Tracker", "tipo_carroceria": "SUV", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 25000, "consumo_ciudad": 7.6, "potencia_cv": 132, "seguridad": 4, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Económico", "Familiar", "Urbano", "Espacioso"] # Etiquetas
    },
    
    # ----------------------------------------------------
    # 4. SUVs de Lujo y Grandes (10) # Comienzo de la sección de SUVs de Lujo y Grandes
    # ----------------------------------------------------
    { # BMW X5
        "modelo": "BMW X5", "tipo_carroceria": "SUV", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 75000, "consumo_ciudad": 12.0, "potencia_cv": 340, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Clásico", "tecnologia": "Muy Alta", "hibrido": True, # Capacidad (7 plazas), estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Lujo", "Potencia", "7 Plazas", "Premium"] # Etiquetas
    },
    { # Audi Q7
        "modelo": "Audi Q7", "tipo_carroceria": "SUV", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 70000, "consumo_ciudad": 11.5, "potencia_cv": 335, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Clásico", "tecnologia": "Muy Alta", "hibrido": True, # Capacidad (7 plazas), estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Lujo", "Tecnología", "7 Plazas", "Viajes"] # Etiquetas
    },
    { # Mercedes-Benz GLE
        "modelo": "Mercedes-Benz GLE", "tipo_carroceria": "SUV", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 72000, "consumo_ciudad": 12.5, "potencia_cv": 367, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Muy Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Exclusivo", "Confort", "Lujo", "Tecnología"] # Etiquetas
    },
    { # Volvo XC90
        "modelo": "Volvo XC90", "tipo_carroceria": "SUV", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 65000, "consumo_ciudad": 9.9, "potencia_cv": 300, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Clásico", "tecnologia": "Alta", "hibrido": True, # Capacidad (7 plazas), estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Seguridad", "7 Plazas", "Lujo", "Híbrido"] # Etiquetas
    },
    { # Land Rover Defender
        "modelo": "Land Rover Defender", "tipo_carroceria": "SUV", "segmento": "Aventura", # Nombre, tipo de carrocería y segmento
        "precio_min": 55000, "consumo_ciudad": 13.5, "potencia_cv": 296, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Robusto", "tecnologia": "Alta", "hibrido": True, # Capacidad (7 plazas), estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Todoterreno", "Aventura", "Robusto", "7 Plazas"] # Etiquetas
    },
    { # Porsche Cayenne
        "modelo": "Porsche Cayenne", "tipo_carroceria": "SUV", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 85000, "consumo_ciudad": 11.8, "potencia_cv": 335, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Deportivo", "tecnologia": "Muy Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Velocidad", "Premium", "Lujo", "Rendimiento"] # Etiquetas
    },
    { # Lexus RX
        "modelo": "Lexus RX", "tipo_carroceria": "SUV", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 60000, "consumo_ciudad": 8.5, "potencia_cv": 250, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Muy Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Confiabilidad", "Lujo", "Híbrido", "Confort"] # Etiquetas
    },
    { # Toyota Highlander
        "modelo": "Toyota Highlander", "tipo_carroceria": "SUV", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 45000, "consumo_ciudad": 8.0, "potencia_cv": 243, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Clásico", "tecnologia": "Media", "hibrido": True, # Capacidad (7 plazas), estilo, tecnología, híbrido
        "electricidad": False, "tags": ["7 Plazas", "Familiar", "Híbrido", "Espacioso"] # Etiquetas
    },
    { # Genesis GV80
        "modelo": "Genesis GV80", "tipo_carroceria": "SUV", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 58000, "consumo_ciudad": 11.0, "potencia_cv": 300, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Exclusivo", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad (7 plazas), estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Diseño", "Premium", "Lujo", "Confort"] # Etiquetas
    },
    { # Ford Explorer
        "modelo": "Ford Explorer", "tipo_carroceria": "SUV", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 48000, "consumo_ciudad": 11.5, "potencia_cv": 300, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Robusto", "tecnologia": "Alta", "hibrido": True, # Capacidad (7 plazas), estilo, tecnología, híbrido
        "electricidad": False, "tags": ["7 Plazas", "Familiar", "Robusto", "Potencia"] # Etiquetas
    },
    
    # ----------------------------------------------------
    # 5. Eléctricos Puros (10) # Comienzo de la sección de Eléctricos Puros
    # ----------------------------------------------------
    { # Hyundai IONIQ 5
        "modelo": "Hyundai IONIQ 5", "tipo_carroceria": "Crossover", "segmento": "Tecnológico", # Nombre, tipo de carrocería y segmento
        "precio_min": 45000, "consumo_ciudad": 0.0, "potencia_cv": 225, "seguridad": 5, # Datos numéricos (consumo 0.0)
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Innovación", "Ecología", "Premium"] # Es eléctrico y etiquetas
    },
    { # Tesla Model Y
        "modelo": "Tesla Model Y", "tipo_carroceria": "SUV", "segmento": "Tecnológico", # Nombre, tipo de carrocería y segmento
        "precio_min": 50000, "consumo_ciudad": 0.0, "potencia_cv": 300, "seguridad": 5, # Datos numéricos (consumo 0.0)
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Rendimiento", "Tecnología", "Viajes"] # Es eléctrico y etiquetas
    },
    { # Kia EV6
        "modelo": "Kia EV6", "tipo_carroceria": "Crossover", "segmento": "Tecnológico", # Nombre, tipo de carrocería y segmento
        "precio_min": 46000, "consumo_ciudad": 0.0, "potencia_cv": 228, "seguridad": 5, # Datos numéricos (consumo 0.0)
        "capacidad_max": 5, "estilo": "Deportivo", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Diseño", "Innovación", "Rendimiento"] # Es eléctrico y etiquetas
    },
    { # Volkswagen ID.4
        "modelo": "Volkswagen ID.4", "tipo_carroceria": "SUV", "segmento": "Tecnológico", # Nombre, tipo de carrocería y segmento
        "precio_min": 42000, "consumo_ciudad": 0.0, "potencia_cv": 201, "seguridad": 5, # Datos numéricos (consumo 0.0)
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Familiar", "Ecología", "Tecnología"] # Es eléctrico y etiquetas
    },
    { # Ford Mustang Mach-E
        "modelo": "Ford Mustang Mach-E", "tipo_carroceria": "Crossover", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 48000, "consumo_ciudad": 0.0, "potencia_cv": 266, "seguridad": 5, # Datos numéricos (consumo 0.0)
        "capacidad_max": 5, "estilo": "Deportivo", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Diseño", "Rendimiento", "Velocidad"] # Es eléctrico y etiquetas
    },
    { # Chevrolet Bolt EV
        "modelo": "Chevrolet Bolt EV", "tipo_carroceria": "Hatchback", "segmento": "Urbano", # Nombre, tipo de carrocería y segmento
        "precio_min": 35000, "consumo_ciudad": 0.0, "potencia_cv": 200, "seguridad": 4, # Datos numéricos (consumo 0.0)
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Urbano", "Ahorro", "Eficiencia"] # Es eléctrico y etiquetas
    },
    { # BMW iX
        "modelo": "BMW iX", "tipo_carroceria": "SUV", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 80000, "consumo_ciudad": 0.0, "potencia_cv": 326, "seguridad": 5, # Datos numéricos (consumo 0.0)
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Lujo", "Tecnología", "Exclusivo"] # Es eléctrico y etiquetas
    },
    { # Mercedes-Benz EQS
        "modelo": "Mercedes-Benz EQS", "tipo_carroceria": "Sedán", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 105000, "consumo_ciudad": 0.0, "potencia_cv": 329, "seguridad": 5, # Datos numéricos (consumo 0.0)
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Lujo", "Confort", "Innovación"] # Es eléctrico y etiquetas
    },
    { # Audi e-tron GT
        "modelo": "Audi e-tron GT", "tipo_carroceria": "Coupé", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 100000, "consumo_ciudad": 0.0, "potencia_cv": 469, "seguridad": 5, # Datos numéricos (consumo 0.0)
        "capacidad_max": 4, "estilo": "Deportivo", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Velocidad", "Alto-Rendimiento", "Lujo"] # Es eléctrico y etiquetas
    },
    { # Nissan Leaf
        "modelo": "Nissan Leaf", "tipo_carroceria": "Hatchback", "segmento": "Urbano", # Nombre, tipo de carrocería y segmento
        "precio_min": 32000, "consumo_ciudad": 0.0, "potencia_cv": 147, "seguridad": 4, # Datos numéricos (consumo 0.0)
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Urbano", "Eficiencia", "Ecología"] # Es eléctrico y etiquetas
    },
    
    # ----------------------------------------------------
    # 6. Deportivos y de Alto Rendimiento (10) # Comienzo de la sección de Deportivos y Alto Rendimiento
    # ----------------------------------------------------
    { # Porsche 911
        "modelo": "Porsche 911", "tipo_carroceria": "Coupé", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 100000, "consumo_ciudad": 12.5, "potencia_cv": 379, "seguridad": 5, # Datos numéricos
        "capacidad_max": 2, "estilo": "Deportivo", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Velocidad", "Exclusivo", "Alto-Rendimiento", "Lujo"] # Etiquetas
    },
    { # Ford Mustang
        "modelo": "Ford Mustang", "tipo_carroceria": "Coupé", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 40000, "consumo_ciudad": 13.5, "potencia_cv": 310, "seguridad": 4, # Datos numéricos
        "capacidad_max": 4, "estilo": "Clásico", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Potencia", "Músculo", "Deportivo", "Rendimiento"] # Etiquetas
    },
    { # Chevrolet Corvette
        "modelo": "Chevrolet Corvette", "tipo_carroceria": "Coupé", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 75000, "consumo_ciudad": 14.0, "potencia_cv": 490, "seguridad": 5, # Datos numéricos
        "capacidad_max": 2, "estilo": "Deportivo", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Velocidad", "Alto-Rendimiento", "Exclusivo", "Lujo"] # Etiquetas
    },
    { # Audi TT
        "modelo": "Audi TT", "tipo_carroceria": "Coupé", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 45000, "consumo_ciudad": 10.5, "potencia_cv": 228, "seguridad": 4, # Datos numéricos
        "capacidad_max": 4, "estilo": "Moderno", "tecnologia": "Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Diseño", "Ágil", "Deportivo", "Estilo"] # Etiquetas
    },
    { # Mazda MX-5 Miata
        "modelo": "Mazda MX-5 Miata", "tipo_carroceria": "Descapotable", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 28000, "consumo_ciudad": 7.5, "potencia_cv": 181, "seguridad": 4, # Datos numéricos
        "capacidad_max": 2, "estilo": "Clásico", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Ágil", "Divertido", "Compacto", "Deportivo"] # Etiquetas
    },
    { # Jaguar F-Type
        "modelo": "Jaguar F-Type", "tipo_carroceria": "Coupé", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 65000, "consumo_ciudad": 13.0, "potencia_cv": 296, "seguridad": 5, # Datos numéricos
        "capacidad_max": 2, "estilo": "Deportivo", "tecnologia": "Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Exclusivo", "Diseño", "Potencia", "Lujo"] # Etiquetas
    },
    { # Nissan GT-R
        "modelo": "Nissan GT-R", "tipo_carroceria": "Coupé", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 115000, "consumo_ciudad": 14.5, "potencia_cv": 565, "seguridad": 5, # Datos numéricos
        "capacidad_max": 4, "estilo": "Robusto", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Velocidad", "Alto-Rendimiento", "Tecnología", "Exclusivo"] # Etiquetas
    },
    { # Mini Cooper JCW
        "modelo": "Mini Cooper JCW", "tipo_carroceria": "Hatchback", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 35000, "consumo_ciudad": 8.5, "potencia_cv": 231, "seguridad": 4, # Datos numéricos
        "capacidad_max": 4, "estilo": "Único", "tecnologia": "Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Compacto", "Rendimiento", "Ágil", "Deportivo"] # Etiquetas
    },
    { # Toyota GR Supra
        "modelo": "Toyota GR Supra", "tipo_carroceria": "Coupé", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 50000, "consumo_ciudad": 10.2, "potencia_cv": 382, "seguridad": 5, # Datos numéricos
        "capacidad_max": 2, "estilo": "Deportivo", "tecnologia": "Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Velocidad", "Rendimiento", "Diseño", "Exclusivo"] # Etiquetas
    },
    { # Alpine A110
        "modelo": "Alpine A110", "tipo_carroceria": "Coupé", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 60000, "consumo_ciudad": 8.0, "potencia_cv": 252, "seguridad": 4, # Datos numéricos
        "capacidad_max": 2, "estilo": "Clásico", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Ágil", "Ligero", "Exclusivo", "Deportivo"] # Etiquetas
    },
    
    # ----------------------------------------------------
    # 7. Pick-ups y Vehículos Todoterreno Puros (5) # Comienzo de la sección de Pick-ups y Todoterreno
    # ----------------------------------------------------
    { # Ford F-150
        "modelo": "Ford F-150", "tipo_carroceria": "Pick-up", "segmento": "Trabajo", # Nombre, tipo de carrocería y segmento
        "precio_min": 35000, "consumo_ciudad": 13.0, "potencia_cv": 325, "seguridad": 4, # Datos numéricos
        "capacidad_max": 5, "estilo": "Robusto", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Potencia", "Carga", "Todoterreno", "Trabajo"] # Etiquetas
    },
    { # Toyota Hilux
        "modelo": "Toyota Hilux", "tipo_carroceria": "Pick-up", "segmento": "Trabajo", # Nombre, tipo de carrocería y segmento
        "precio_min": 38000, "consumo_ciudad": 11.5, "potencia_cv": 204, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Robusto", "tecnologia": "Media", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Confiabilidad", "Todoterreno", "Trabajo", "Carga"] # Etiquetas
    },
    { # Jeep Wrangler
        "modelo": "Jeep Wrangler", "tipo_carroceria": "SUV", "segmento": "Aventura", # Nombre, tipo de carrocería y segmento
        "precio_min": 40000, "consumo_ciudad": 12.0, "potencia_cv": 285, "seguridad": 4, # Datos numéricos
        "capacidad_max": 5, "estilo": "Robusto", "tecnologia": "Media", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Todoterreno", "Aventura", "Robusto", "Único"] # Etiquetas
    },
    { # RAM 1500
        "modelo": "RAM 1500", "tipo_carroceria": "Pick-up", "segmento": "Trabajo", # Nombre, tipo de carrocería y segmento
        "precio_min": 42000, "consumo_ciudad": 15.0, "potencia_cv": 395, "seguridad": 4, # Datos numéricos
        "capacidad_max": 5, "estilo": "Robusto", "tecnologia": "Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Potencia", "Lujo", "Carga", "Híbrido"] # Etiquetas
    },
    { # Mitsubishi L200
        "modelo": "Mitsubishi L200", "tipo_carroceria": "Pick-up", "segmento": "Trabajo", # Nombre, tipo de carrocería y segmento
        "precio_min": 30000, "consumo_ciudad": 10.5, "potencia_cv": 150, "seguridad": 4, # Datos numéricos
        "capacidad_max": 5, "estilo": "Robusto", "tecnologia": "Baja", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Económico", "Trabajo", "Todoterreno", "Carga"] # Etiquetas
    },

    # ----------------------------------------------------
    # 8. Monovolúmenes y Familiares Grandes (10) # Comienzo de la sección de Monovolúmenes y Familiares
    # ----------------------------------------------------
    { # Dodge Grand Caravan
        "modelo": "Dodge Grand Caravan", "tipo_carroceria": "Monovolumen", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 28000, "consumo_ciudad": 12.0, "potencia_cv": 287, "seguridad": 4, # Datos numéricos
        "capacidad_max": 7, "estilo": "Clásico", "tecnologia": "Media", "hibrido": False, # Capacidad (7 plazas), estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["7 Plazas", "Familiar", "Espacioso", "Confort"] # Etiquetas
    },
    { # Chrysler Pacifica
        "modelo": "Chrysler Pacifica", "tipo_carroceria": "Monovolumen", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 35000, "consumo_ciudad": 10.5, "potencia_cv": 287, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Moderno", "tecnologia": "Alta", "hibrido": True, # Capacidad (7 plazas), estilo, tecnología, híbrido
        "electricidad": False, "tags": ["7 Plazas", "Lujo", "Híbrido", "Familiar"] # Etiquetas
    },
    { # Kia Carnival
        "modelo": "Kia Carnival", "tipo_carroceria": "Monovolumen", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 33000, "consumo_ciudad": 11.0, "potencia_cv": 290, "seguridad": 5, # Datos numéricos
        "capacidad_max": 8, "estilo": "Moderno", "tecnologia": "Alta", "hibrido": False, # Capacidad (8 plazas), estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["8 Plazas", "Diseño", "Familiar", "Tecnología"] # Etiquetas
    },
    { # Renault Espace
        "modelo": "Renault Espace", "tipo_carroceria": "Monovolumen", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 38000, "consumo_ciudad": 8.5, "potencia_cv": 200, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Moderno", "tecnologia": "Alta", "hibrido": True, # Capacidad (7 plazas), estilo, tecnología, híbrido
        "electricidad": False, "tags": ["7 Plazas", "Híbrido", "Confort", "Viajes"] # Etiquetas
    },
    { # Citroën Grand C4 SpaceTourer
        "modelo": "Citroën Grand C4 SpaceTourer", "tipo_carroceria": "Monovolumen", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 29000, "consumo_ciudad": 7.8, "potencia_cv": 130, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Único", "tecnologia": "Media", "hibrido": False, # Capacidad (7 plazas), estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["7 Plazas", "Confort", "Espacioso", "Familiar"] # Etiquetas
    },
    { # Volkswagen Touran
        "modelo": "Volkswagen Touran", "tipo_carroceria": "Monovolumen", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 30000, "consumo_ciudad": 7.5, "potencia_cv": 150, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Clásico", "tecnologia": "Media", "hibrido": False, # Capacidad (7 plazas), estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["7 Plazas", "Calidad", "Familiar", "Práctico"] # Etiquetas
    },
    { # Seat Alhambra
        "modelo": "Seat Alhambra", "tipo_carroceria": "Monovolumen", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 31000, "consumo_ciudad": 8.0, "potencia_cv": 150, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Clásico", "tecnologia": "Media", "hibrido": False, # Capacidad (7 plazas), estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["7 Plazas", "Espacioso", "Familiar", "Viajes"] # Etiquetas
    },
    { # Mercedes-Benz Clase V
        "modelo": "Mercedes-Benz Clase V", "tipo_carroceria": "Van", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 60000, "consumo_ciudad": 9.5, "potencia_cv": 237, "seguridad": 5, # Datos numéricos
        "capacidad_max": 8, "estilo": "Clásico", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad (8 plazas), estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["8 Plazas", "Lujo", "Confort", "Exclusivo"] # Etiquetas
    },
    { # Hyundai Staria
        "modelo": "Hyundai Staria", "tipo_carroceria": "Van", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 45000, "consumo_ciudad": 10.0, "potencia_cv": 177, "seguridad": 4, # Datos numéricos
        "capacidad_max": 9, "estilo": "Único", "tecnologia": "Alta", "hibrido": False, # Capacidad (9 plazas), estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["9 Plazas", "Diseño", "Espacioso", "Familiar"] # Etiquetas
    },
    { # Toyota Sienna
        "modelo": "Toyota Sienna", "tipo_carroceria": "Monovolumen", "segmento": "Familiar", # Nombre, tipo de carrocería y segmento
        "precio_min": 38000, "consumo_ciudad": 7.1, "potencia_cv": 245, "seguridad": 5, # Datos numéricos
        "capacidad_max": 7, "estilo": "Moderno", "tecnologia": "Media", "hibrido": True, # Capacidad (7 plazas), estilo, tecnología, híbrido
        "electricidad": False, "tags": ["7 Plazas", "Híbrido", "Confiabilidad", "Familiar"] # Etiquetas
    },
    
    # ----------------------------------------------------
    # 9. Otros Nichos y Complementos (5) # Comienzo de la sección de Otros Nichos
    # ----------------------------------------------------
    { # Suzuki Jimny
        "modelo": "Suzuki Jimny", "tipo_carroceria": "SUV", "segmento": "Aventura", # Nombre, tipo de carrocería y segmento
        "precio_min": 24000, "consumo_ciudad": 8.5, "potencia_cv": 102, "seguridad": 3, # Datos numéricos
        "capacidad_max": 4, "estilo": "Robusto", "tecnologia": "Baja", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Todoterreno", "Compacto", "Robusto", "Aventura"] # Etiquetas
    },
    { # Land Rover Range Rover
        "modelo": "Land Rover Range Rover", "tipo_carroceria": "SUV", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 110000, "consumo_ciudad": 13.0, "potencia_cv": 395, "seguridad": 5, # Datos numéricos
        "capacidad_max": 5, "estilo": "Clásico", "tecnologia": "Muy Alta", "hibrido": True, # Capacidad, estilo, tecnología, híbrido
        "electricidad": False, "tags": ["Exclusivo", "Lujo", "Potencia", "Todoterreno"] # Etiquetas
    },
    { # Tesla Model S (Truncado, completado)
        "modelo": "Tesla Model S", "tipo_carroceria": "Sedán", "segmento": "Lujo", # Nombre, tipo de carrocería y segmento
        "precio_min": 85000, "consumo_ciudad": 0.0, "potencia_cv": 670, "seguridad": 5, # Datos numéricos (consumo 0.0)
        "capacidad_max": 5, "estilo": "Moderno", "tecnologia": "Muy Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": True, "tags": ["Eléctrico", "Rendimiento", "Lujo", "Innovación"] # Es eléctrico y etiquetas
    },
    { # Caterham Seven 170 (Añadido para completar sección)
        "modelo": "Caterham Seven 170", "tipo_carroceria": "Roadster", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 35000, "consumo_ciudad": 7.0, "potencia_cv": 84, "seguridad": 3, # Datos numéricos
        "capacidad_max": 2, "estilo": "Clásico", "tecnologia": "Baja", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Ligero", "Divertido", "Exclusivo", "Track"] # Etiquetas
    },
    { # Ariel Atom (Añadido para completar sección)
        "modelo": "Ariel Atom", "tipo_carroceria": "Roadster", "segmento": "Deportivo", # Nombre, tipo de carrocería y segmento
        "precio_min": 70000, "consumo_ciudad": 11.0, "potencia_cv": 320, "seguridad": 3, # Datos numéricos
        "capacidad_max": 2, "estilo": "Único", "tecnologia": "Alta", "hibrido": False, # Capacidad, estilo, tecnología, no híbrido
        "electricidad": False, "tags": ["Track", "Alto-Rendimiento", "Exclusivo", "Velocidad"] # Etiquetas
    } # Fin del último diccionario de coche
] # Fin del array CAR_DATASET