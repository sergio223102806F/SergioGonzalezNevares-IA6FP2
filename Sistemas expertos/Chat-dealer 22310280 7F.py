# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 16:27:22 2025

@author: elvin
"""

import json
import os

class TraficanteChatbot:
    def __init__(self):
        self.base_conocimiento = {
            "hola": "¿Qué onda? ¿Buscas algo? Tengo de todo...",
            "que tienes": "Tengo merca blanca, cristal, hierba, pastillas... ¿qué necesitas?",
            "precios": "Blanca: 500 el g, cristal: 600, hierba: 300 el g, pastillas: 200 c/u",
            "donde nos vemos": "Solo lugares seguros. Te doy punto cuando confirmes pedido",
            "calidad": "Todo premium, 100% puro. Mis clientes siempre vuelven",
            "pago": "Solo efectivo. Nada de transacciones digitales",
            "entrega": "Entrego personalmente. Nada de correos ni intermediarios",
            "cantidad": "Mínimo 5g por producto. Si quieres prueba, 1g extra",
            "seguridad": "Sistema de señales. Todo discreto y seguro",
            "emergencia": "Si hay problema, borra chat. Yo nunca estuve aquí"
        }
        self.cargar_conocimiento()
    
    def cargar_conocimiento(self):
        if os.path.exists('conocimiento_mercancia.json'):
            with open('conocimiento_mercancia.json', 'r', encoding='utf-8') as f:
                self.base_conocimiento = json.load(f)
    
    def guardar_conocimiento(self):
        with open('conocimiento_mercancia.json', 'w', encoding='utf-8') as f:
            json.dump(self.base_conocimiento, f, indent=4, ensure_ascii=False)
    
    def buscar_respuesta(self, pregunta):
        pregunta = pregunta.lower().strip()
        
        if pregunta in self.base_conocimiento:
            return self.base_conocimiento[pregunta]
        
        palabras_clave = {
            "precio": "precios",
            "cuesta": "precios",
            "cuanto": "precios",
            "cobra": "precios",
            "producto": "que tienes",
            "mercancia": "que tienes",
            "droga": "que tienes",
            "hierba": "que tienes",
            "marihuana": "que tienes",
            "coca": "que tienes",
            "cristal": "que tienes",
            "meta": "que tienes",
            "pasto": "que tienes",
            "verde": "que tienes",
            "blanca": "que tienes",
            "encuentro": "donde nos vemos",
            "donde": "donde nos vemos",
            "lugar": "donde nos vemos",
            "punto": "donde nos vemos",
            "calidad": "calidad",
            "puro": "calidad",
            "buena": "calidad",
            "pagar": "pago",
            "efectivo": "pago",
            "transferencia": "pago",
            "dinero": "pago",
            "entrega": "entrega",
            "entregas": "entrega",
            "llevar": "entrega",
            "recoger": "entrega",
            "cantidad": "cantidad",
            "gramo": "cantidad",
            "kilo": "cantidad",
            "poco": "cantidad",
            "mucho": "cantidad",
            "seguro": "seguridad",
            "seguridad": "seguridad",
            "policia": "seguridad",
            "problema": "emergencia",
            "emergencia": "emergencia",
            "peligro": "emergencia"
        }
        
        for palabra, respuesta_key in palabras_clave.items():
            if palabra in pregunta:
                return self.base_conocimiento[respuesta_key]
        
        return None
    
    def aprender(self, pregunta, respuesta):
        self.base_conocimiento[pregunta.lower().strip()] = respuesta
        self.guardar_conocimiento()
        return "✅ Anotado. Ahora sé responder a eso..."
    
    def iniciar_chat(self):
        print("🔒 Chat seguro activado (auto-destrucción en 24h)")
        print("🐍 Contacto: 'El Serpiente'")
        print("💊 Productos disponibles: Blanca, Cristal, Hierba, Pastillas")
        print("📞 Escribe 'salir' para borrar conversación\n")
        
        print("🐍: ¿Qué necesitas? Tengo todo premium...")
        
        while True:
            user_input = input("👤: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'borrar']:
                print("🐍: Chat borrado. Hasta luego...")
                break
            
            if not user_input:
                continue
            
            respuesta = self.buscar_respuesta(user_input)
            
            if respuesta:
                print(f"🐍: {respuesta}")
            else:
                print("🐍: No entiendo... ¿qué quieres decir?")
                nueva_respuesta = input("Enseñame cómo responder: ").strip()
                
                if nueva_respuesta:
                    self.aprender(user_input, nueva_respuesta)
                    print("🐍: ✅ Ya quedó...")
                else:
                    print("🐍: 🤐 Mejor así...")

if __name__ == "__main__":
    chatbot = TraficanteChatbot()
    chatbot.iniciar_chat()