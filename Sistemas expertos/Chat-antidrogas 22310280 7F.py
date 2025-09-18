# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 17:02:21 2025

@author: elvin
"""

import json
import os

class ExpertoEnDrogas:
    def __init__(self):
        self.base_conocimiento = {
            "hola": "¡Hola! Soy un experto en farmacología y drogas. ¿En qué puedo ayudarte?",
            "que es una droga": "Una droga es cualquier sustancia que, introducida en el organismo, puede modificar una o más funciones y tiene potencial de abuso o dependencia.",
            "tipos de drogas": "Existen varios tipos: estimulantes (cocaína, anfetaminas), depresores (alcohol, benzodiacepinas), alucinógenos (LSD, hongos) y opioides (heroína, morfina).",
            "efectos de la cocaina": "La cocaína es un estimulante que produce euforia, energía y alerta, pero también puede causar ansiedad, paranoia y problemas cardiovasculares.",
            "que es la marihuana": "La marihuana es una droga derivada del cannabis que contiene THC. Puede producir relajación pero también afectar la memoria y coordinación.",
            "riesgos del alcohol": "El alcohol es un depresor del SNC. Su consumo excesivo puede dañar hígado, cerebro y aumentar riesgo de adicción.",
            "drogas sinteticas": "Son sustancias creadas en laboratorio como el éxtasis o metanfetaminas. Suelen ser impredecibles y muy peligrosas.",
            "adiccion": "La adicción es una enfermedad cerebral crónica caracterizada por la búsqueda y uso compulsivo de drogas a pesar de sus consecuencias negativas.",
            "tratamiento": "Existen diversos tratamientos: terapia conductual, medicamentos, grupos de apoyo y programas de rehabilitación.",
            "prevencion": "La prevención incluye educación, desarrollo de habilidades sociales y evitar situaciones de riesgo."
        }
        self.cargar_conocimiento()
    
    def cargar_conocimiento(self):
        if os.path.exists('conocimiento_drogas.json'):
            with open('conocimiento_drogas.json', 'r', encoding='utf-8') as f:
                self.base_conocimiento = json.load(f)
    
    def guardar_conocimiento(self):
        with open('conocimiento_drogas.json', 'w', encoding='utf-8') as f:
            json.dump(self.base_conocimiento, f, indent=4, ensure_ascii=False)
    
    def buscar_respuesta(self, pregunta):
        pregunta = pregunta.lower().strip()
        
        # Buscar coincidencia exacta
        if pregunta in self.base_conocimiento:
            return self.base_conocimiento[pregunta]
        
        # Búsqueda por palabras clave
        palabras_clave = {
            "droga": "que es una droga",
            "coca": "efectos de la cocaina",
            "marihuana": "que es la marihuana",
            "alcohol": "riesgos del alcohol",
            "sintetic": "drogas sinteticas",
            "adiccion": "adiccion",
            "tratamiento": "tratamiento",
            "prevencion": "prevencion",
            "tipo": "tipos de drogas",
            "efecto": "tipos de drogas"
        }
        
        for palabra, respuesta_key in palabras_clave.items():
            if palabra in pregunta:
                return self.base_conocimiento[respuesta_key]
        
        return None
    
    def aprender(self, pregunta, respuesta):
        self.base_conocimiento[pregunta.lower().strip()] = respuesta
        self.guardar_conocimiento()
        return "¡Gracias por la información! He ampliado mi conocimiento sobre drogas."
    
    def mostrar_info_basica(self):
        print("\n--- Temas sobre los que puedo informarte ---")
        print("• Tipos de drogas y sus efectos")
        print("• Riesgos y consecuencias del consumo")
        print("• Adicción y dependencia")
        print("• Tratamientos disponibles")
        print("• Medidas de prevención")
        print("• Información sobre drogas específicas")
        print("\nPregúntame sobre cualquier aspecto relacionado con drogas...\n")
    
    def iniciar_consulta(self):
        print("=== CONSULTORIO VIRTUAL SOBRE DROGAS ===")
        print("Soy un experto en farmacología y sustancias psicoactivas")
        self.mostrar_info_basica()
        
        while True:
            user_input = input("Tu pregunta: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'adiós']:
                print("Experto: Espero haberte sido de ayuda. ¡Cuídate!")
                break
            
            if not user_input:
                continue
            
            respuesta = self.buscar_respuesta(user_input)
            
            if respuesta:
                print(f"\nExperto: {respuesta}\n")
            else:
                print("\nExperto: No tengo información específica sobre eso.")
                print("¿Podrías proporcionarme una respuesta adecuada para esta pregunta?")
                
                nueva_respuesta = input("Respuesta correcta: ").strip()
                
                if nueva_respuesta:
                    self.aprender(user_input, nueva_respuesta)
                    print("Experto: ✅ Información añadida a mi base de conocimiento.\n")
                else:
                    print("Experto: Entiendo. Te recomiendo consultar con un profesional de la salud.\n")

# Ejecutar el sistema experto
if __name__ == "__main__":
    experto = ExpertoEnDrogas()
    experto.iniciar_consulta()