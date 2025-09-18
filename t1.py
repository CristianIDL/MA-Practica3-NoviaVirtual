# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 17:32:47 2025

@author: alan_
"""
import re
import time
from datetime import datetime, date, timedelta
import json, os, random, re, sys

preguntas_json = os.path.join(os.path.dirname(__file__), "respuestas2.json")
personalidades = ["celosa", "toxica", "amorosa", "atenta", "platicona"]
temas = ["saludo", "animes", "platica_rutinaria", "videojuegos", "emociones", "despedida", "fallback"]

"""
ANIME_RE = r"anime|manga|one piece|naruto|jujutsu|kimetsu"
VIDEOJUEGOS_RE = r"videojuego|juego|jugar|play|xbox|pc|genshin|zelda"
EMOCIONES_RE = r"siento|estoy (triste|feliz|enojado|raro)|emociones|mal dia"
RUTINA_RE = r"que (haces|hiciste)|como (te va|estas)|tu dia|que me cuentas"
SALIR_RE = r"adios|bye|me voy|hasta luego"

"""
ANIME_RE = r"\b(anime|animes|manga|one\s*piece|naruto|jujutsu\s*kaisen|jujutsu|kimetsu\s*no\s*yaiba|kimetsu|demon\s*slayer|bleach|attack\s*on\s*titan|shingeki|dragon\s*ball|dbz|chainsaw\s*man|my\s*hero\s*academia|bnha|haikyuu|spy\s*x\s*family|solo\s*leveling|evangelion|fullmetal|fma)\b"

VIDEOJUEGOS_RE = r"\b(videojuego|videojuegos|juego|jugar|gaming|play|playstation|ps4|ps5|xbox|switch|nintendo|pc|steam|genshin|zelda|totk|mario|smash|pokemon|minecraft|roblox|lol|league\s*of\s*legends|dota|valorant|csgo|counter\s*strike|fortnite|apex|overwatch|call\s*of\s*duty|cod|gta|red\s*dead|fifa|ea\s*fc)\b"

EMOCIONES_RE = r"\b(siento|me\s*siento|estoy\s*(triste|feliz|enojad[oa]|molest[oa]|raro|ansios[oa]|estresad[oa]|agotad[oa]|cansad[oa]|desmotivad[oa]|motivad[oa]|preocupad[oa]|aburrid[oa]|emocionad[oa])|emociones|mal\s*dia)\b"

RUTINA_RE = r"\b(que\s*(haces|hiciste|planes?)|como\s*(te\s*va|estas|va\s*todo)|tu\s*dia|que\s*me\s*cuentas|que\s*tal|que\s*hay|en\s*que\s*andas|que\s*plan(?:es)?)\b"

SALIR_RE = r"\b(adios|bye|me\s*voy|hasta\s*luego|nos\s*vemos|hasta\s*pronto|cuidate|tengo\s*que\s*irme|me\s*desconecto)\b"
AFIRMACION_RE = r"si|simon|claro|ok|esta bien|bueno|va"
NEGACION_RE = r"no|nel|paso|ahora no|no quiero"

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
        
        

def obtener_respuesta(personalidad, respuestas_data, contador, contexto={}):
    try:
        
        respuesta_plantilla = respuestas_data[personalidad][contexto['tema']][contador]
        respuesta_formateada = respuesta_plantilla.format(**contexto)
        print("\n" + respuesta_formateada)
        time.sleep(1.5)
        contador = contador + 1
    except IndexError:
       
        print("(Vaya, parece que ya no tengo más que decir sobre este tema.)")
        contador = 999 
    except KeyError as e:
        print(f"(Error de formato: no se encontró la clave {e})")
    
    return contador

    
def main():
    respuestas = cargar_respuestas()
    memoria = {}

    print('Chatbot lista. Elige una personalidad:')
    print(" | ".join(personalidades))
    personalidad_actual = input("\nHola, soy tu novia virtual. ¿Cómo quieres que sea hoy?\n> ")
    nombre = input("¿Cuál es tu nombre?\n")
    memoria['nombre'] = nombre

    if personalidad_actual not in personalidades:
        print("Esa personalidad no la conozco... seré 'amorosa' por defecto.")
        personalidad_actual = "amorosa"
    
    # Mapeo de temas a estados para simplificar el código
    tema_a_estado = {
        "animes": 101, "videojuegos": 102, "emociones": 103,
        "platica_rutinaria": 104
    }

    # El estado 0 es el inicio, 100 es escucha, 200 es pregunta proactiva, 999 es salida.
    state = 0
    contador = 0
    en_chat = True

    while en_chat:
        # === ESTADO 0: SALUDO INICIAL ===
        if state == 0:
            memoria['tema'] = "saludo"
            contador = obtener_respuesta(personalidad_actual, respuestas, 0, memoria)
            state = 100 # Pasamos al estado de escucha

        # === ESTADO 100: ESCUCHA INTELIGENTE ===
        elif state == 100:
            opcion = input("\n> ")
            opcion = minus(opcion)
            opcion = quitarAcentos(opcion)

            # Buscamos si el usuario quiere cambiar de tema a la fuerza
            nuevo_tema_encontrado = None
            if re.search(ANIME_RE, opcion): nuevo_tema_encontrado = "animes"
            elif re.search(VIDEOJUEGOS_RE, opcion): nuevo_tema_encontrado = "videojuegos"
            elif re.search(EMOCIONES_RE, opcion): nuevo_tema_encontrado = "emociones"
            elif re.search(RUTINA_RE, opcion): nuevo_tema_encontrado = "platica_rutinaria"
            elif re.search(SALIR_RE, opcion): state = 999; continue

            if nuevo_tema_encontrado:
                # Si se encontró un tema, iniciamos esa conversación
                memoria['tema'] = nuevo_tema_encontrado
                contador = 0 # Reiniciamos el contador para el nuevo tema
                state = tema_a_estado[nuevo_tema_encontrado]
            elif memoria.get('tema') in tema_a_estado:
                # Si NO se encontró un nuevo tema, simplemente continuamos con el tema actual
                state = tema_a_estado[memoria['tema']]
            else:
                # Si no hay tema previo y no se detectó uno nuevo, es un fallback
                memoria['tema'] = "fallback"
                contador = obtener_respuesta(personalidad_actual, respuestas, 0, memoria)
                # Nos quedamos en estado de escucha
                state = 100

        # === ESTADOS 101-104: DURANTE UNA CONVERSACIÓN TEMÁTICA ===
        elif state in tema_a_estado.values():
            tema_actual = memoria['tema']
            respuestas_del_tema = respuestas[personalidad_actual][tema_actual]

            if contador < len(respuestas_del_tema):
                # Si todavía hay respuestas en la lista, decimos la siguiente
                contador = obtener_respuesta(personalidad_actual, respuestas, contador, memoria)
                state = 100 # Y volvemos a escuchar la respuesta del usuario
            else:
                # Si se acabaron las respuestas, pasamos al estado de pregunta proactiva
                state = 200

        # === ESTADO 200: PREGUNTA PROACTIVA PARA CAMBIAR DE TEMA ===
        elif state == 200:
      
            preguntas = respuestas[personalidad_actual].get("preguntas_proactivas", [])
            
            if not preguntas:
                # Si la personalidad no tiene preguntas, usamos una genérica
                preguntas = ["Bueno, cambiando de tema... ¿qué has jugado últimamente?", 
                             "Oye, y... ¿cómo te has sentido estos días?"]
            
            pregunta_elegida = random.choice(preguntas)
            
            # Analizamos la pregunta para "adivinar" el tema propuesto
            if "juego" in pregunta_elegida or "jugar" in pregunta_elegida:
                memoria['tema_propuesto'] = "videojuegos"
            elif "sentido" in pregunta_elegida or "emocion" in pregunta_elegida:
                memoria['tema_propuesto'] = "emociones"
            else:
                memoria['tema_propuesto'] = "platica_rutinaria"

            print("\n" + pregunta_elegida)
            state = 201 # Pasamos a esperar la respuesta SÍ/NO

        # === ESTADO 201: ESPERANDO RESPUESTA A PREGUNTA PROACTIVA ===
        elif state == 201:
            opcion = input("\n> ")
            opcion = minus(opcion)
            opcion = quitarAcentos(opcion)

            if re.search(AFIRMACION_RE, opcion):
                # El usuario aceptó, cambiamos al tema propuesto
                memoria['tema'] = memoria.pop('tema_propuesto', 'platica_rutinaria')
                contador = 0
                state = tema_a_estado[memoria['tema']]
            elif re.search(NEGACION_RE, opcion):
                # El usuario no quiso, volvemos a la escucha neutral
                print("\nOh, está bien. ¿De qué quieres hablar entonces?")
                memoria.pop('tema_propuesto', None)
                state = 100
            else:
                # No se entendió, insistimos una vez
                print("\nPerdona, no te entendí. ¿Quieres que hablemos de eso o no?")
                # Nos quedamos en el estado 201 para la siguiente respuesta

        # === ESTADO 999: DESPEDIDA ===
        elif state == 999:
            memoria['tema'] = "despedida"
            obtener_respuesta(personalidad_actual, respuestas, 0, memoria)
            en_chat = False # Termina el bucle y el programa


main()
