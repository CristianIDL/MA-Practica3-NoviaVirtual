# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 17:32:47 2025

@author: alan_
"""
import re
import time
from datetime import datetime, date, timedelta
import json, os, random, re, sys

preguntas_json = os.path.join(os.path.dirname(__file__), "respuestas.json")
personalidades = ["celosa", "toxica", "amorosa", "atenta", "platicona"]
temas = ["saludo", "animes", "platica_rutinaria", "videojuegos", "emociones", "despedida", "fallback"]


ANIME_RE = r"anime|manga|one piece|naruto|jujutsu|kimetsu"
VIDEOJUEGOS_RE = r"videojuego|juego|jugar|play|xbox|pc|genshin|zelda"
EMOCIONES_RE = r"siento|estoy (triste|feliz|enojado|raro)|emociones|mal dia"
RUTINA_RE = r"que (haces|hiciste)|como (te va|estas)|tu dia|que me cuentas| "
SALIR_RE = r"adios|bye|me voy|hasta luego"

def minus(text):
    m=text.lower()
    return m

def quitarAcentos(s):
      replacements = (
          ("á", "a"),
          ("é", "e"),
          ("í", "i"),
          ("ó", "o"),
          ("ú", "u"),
          )
      for a, b in replacements:
          s = s.replace(a, b).replace(a.upper(), b.upper())
      return s

def cargar_respuestas():

    if os.path.exists(preguntas_json):
        with open(preguntas_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Bucle de seguridad para asegurar que todas las personalidades y temas existen
        for p in personalidades:
            if p not in data:
                data[p] = {}
            for t in temas:
                data[p].setdefault(t, ["(No tengo una respuesta para este tema... perdón.)"])
        return data
    else:
        # Si no hay JSON, el programa no puede funcionar.
        print("Error: El archivo 'respuestas.json' no se encontró.")
        exit() # Termina el programa
        
        

def obtener_respuesta(personalidad, tema, respuestas_data):
    """Función centralizada para obtener una respuesta aleatoria."""
    print("\n" + random.choice(respuestas_data[personalidad][tema]))
    time.sleep(1.5) # Pequeña pausa para simular que está "escribiendo"
    
def main():
    respuestas = cargar_respuestas()
    
    print('Chatbot lista. Elige una personalidad:')
    print(" | ".join(personalidades))
    personalidad_actual = input("\nHola, soy tu novia virtual. ¿Cómo quieres que sea hoy?\n> ")

    if personalidad_actual not in personalidades:
        print("Esa personalidad no la conozco... seré 'amorosa' por defecto. ❤️")
        personalidad_actual = "amorosa"

    # Diccionario que mapea personalidad a su estado inicial. ¡Esta es la clave de tu idea!
    puntos_de_partida = {
        "amorosa": 0,
        "toxica": 10,
        "celosa": 20,
        "atenta": 30,
        "platicona": 40
    }

    # Asigna el estado inicial basado en la personalidad elegida
    state = puntos_de_partida.get(personalidad_actual, 0) # Si no la encuentra, inicia en 0 (amorosa)
    print(state)
    en_chat = True
    while en_chat:
        # === ESTADOS INICIALES (RAMAS DE PARTIDA) ===
        if state in [0, 10, 20, 30, 40]:
            obtener_respuesta(personalidad_actual, "saludo", respuestas)
            state = 100 # Transición al estado central de escucha

        # === ESTADO CENTRAL DE ESCUCHA ===
        elif state == 100:
            opcion = input("> ")
            opcion=minus(opcion)
            opcion=quitarAcentos(opcion)
            if re.search(ANIME_RE, opcion):
                state = 101 # Ir a la rama de animes
            elif re.search(VIDEOJUEGOS_RE, opcion):
                state = 102 # Ir a la rama de videojuegos
            elif re.search(EMOCIONES_RE, opcion):
                state = 103 # Ir a la rama de emociones
            elif re.search(RUTINA_RE, opcion):
                state = 104 # Ir a la rama de platica rutinaria
            elif re.search(SALIR_RE, opcion):
                state = 999 # Ir al estado de despedida
            else:
                # Si no entiende, usa la respuesta fallback y se mantiene escuchando
                obtener_respuesta(personalidad_actual, "fallback", respuestas)
                state = 100

        # === RAMAS DE CONVERSACIÓN (TEMAS) ===
        elif state == 101: # Tema: Animes
            obtener_respuesta(personalidad_actual, "animes", respuestas)
            state = 100 # Regresa al estado de escucha
        
        elif state == 102: # Tema: Videojuegos
            obtener_respuesta(personalidad_actual, "videojuegos", respuestas)
            state = 100 # Regresa al estado de escucha
            
        elif state == 103: # Tema: Emociones
            obtener_respuesta(personalidad_actual, "emociones", respuestas)
            state = 100 # Regresa al estado de escucha
            
        elif state == 104: # Tema: Platica Rutinaria
            obtener_respuesta(personalidad_actual, "platica_rutinaria", respuestas)
            state = 100 # Regresa al estado de escucha

        # === ESTADO FINAL ===
        elif state == 999:
            obtener_respuesta(personalidad_actual, "despedida", respuestas)
            en_chat = False # Termina el bucle y el programa
    
main()