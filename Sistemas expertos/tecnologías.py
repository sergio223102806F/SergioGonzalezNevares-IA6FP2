# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 16:06:23 2025

@author: elvin
"""

import json
import os

class SistemaExpertoSimple:
    def __init__(self):
        self.base_conocimiento = {
            "hola": "¡Hola! ¿Cómo estás?",
            "como estas": "Estoy bien, gracias. ¿Y tú?",
            "de que te gustaria hablar": "Me gustaría hablar de tecnología o cualquier tema que te interese"
        }
        self.cargar_conocimiento()
    
    def cargar_conocimiento(self):
        if os.path.exists('conocimiento.json'):
            with open('conocimiento.json', 'r') as f:
                self.base_conocimiento = json.load(f)
    
    def guardar_conocimiento(self):
        with open('conocimiento.json', 'w') as f:
            json.dump(self.base_conocimiento, f, indent=4)
    
    def buscar_respuesta(self, pregunta):
        pregunta = pregunta.lower().strip()
        
        # Buscar coincidencia exacta
        if pregunta in self.base_conocimiento:
            return self.base_conocimiento[pregunta]
        
        # Buscar coincidencia parcial
        for key in self.base_conocimiento:
            if pregunta in key or key in pregunta:
                return self.base_conocimiento[key]
        
        return None
    
    def aprender(self, pregunta, respuesta):
        self.base_conocimiento[pregunta.lower().strip()] = respuesta
        self.guardar_conocimiento()
        return "¡Gracias! He aprendido algo nuevo."
    
    def iniciar_chat(self):
        print("Chatbot: Hola! Soy un bot simple. Escribe 'salir' para terminar.")
        
        while True:
            user_input = input("Tú: ").strip()
            
            if user_input.lower() == 'salir':
                print("Chatbot: ¡Adiós!")
                break
            
            if not user_input:
                continue
            
            respuesta = self.buscar_respuesta(user_input)
            
            if respuesta:
                print(f"Chatbot: {respuesta}")
            else:
                print("Chatbot: No sé responder eso. ¿Qué debería decir?")
                nueva_respuesta = input("Enséñame: ").strip()
                
                if nueva_respuesta:
                    self.aprender(user_input, nueva_respuesta)
                    print("Chatbot: ¡Entendido! Ahora lo sé.")
                else:
                    print("Chatbot: Ok, tal vez después.")

# Ejecutar el sistema
if __name__ == "__main__":
    bot = SistemaExpertoSimple()
    bot.iniciar_chat()