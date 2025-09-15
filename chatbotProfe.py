#inicialización de estados
import re
import time
from datetime import datetime, date, timedelta

 # Lenguaje natural por expresiones regulares
Promo_RE = r"[pP]romociones|[Pp]romos|[dD]escuentos|[qQ]uiero (las|los) (|promociones|descuentos)"
Cita_RE = r"([Cc]ita|[hH]acer|[Aa]genda(r|)(| servicio))(| [cC]ita)|[nN]ecesito un servicio|[Qq]uiero agendar cita|servicio"
Venta_RE = r"[vV]enta(s|)|[Cc]ompra(r|)|[qQ]uiero|[vV]enden"
placa_Re = r"\d\d\d[\s| |-]?\w\w\w"
afirmacion_RE = r"[Ss][íi|] ([Cc]laro|[Gg]racias)|[Cc]laro|[dD]efinitivamente|[Pp]or supuesto|[Gg]racias|[Pp]or favor|[sS][íi]"
salir_RE = r"[sS]alir|[mM]e equivoque|[pP]erd[oó]n|[aA]di[óo]s|[lL]a cague|[uU]ps|[sS]orry|[eE]rror|[Nn]o|[fF]all[ao]|[sS]kype|[dD]eseo (salir|interrumpir)| "

state=0
Salida=1
while Salida:
    if state==0:
        print("Hola soy el Chatbot de la FORD ¿En qué te puedo ayudar?")
        time.sleep(1)
        opcion=input("Soy capaz de informarte de nuestras promociones, venta de vehículos y ayudarte a agendar un cita. \n\t\t\t")
        if re.findall(Promo_RE, opcion, flags=0)!=[]:
            state=1
        elif re.findall(Cita_RE, opcion, flags=0)!=[]:
            state=2
        elif re.findall(Venta_RE, opcion, flags=0)!=[]:
            state=11
        elif re.findall(salir_RE, opcion, flags=0)!=[]:
            state=7
        else :
          state =8
    if state == 1:
        print("Nuestras promociones son...")
        state=6
    if state == 2:
        name = input("Dime tu nombre para agendar la cita. \n\t\t\t")
        state = 4
    if state == 3:
        print("En un momento te contactara un agente de ventas")
        state=6
    if state == 4:
        placa = input("Podrias proporcionarme tu placa. \n\t\t\t")
        if re.findall(placa_Re, placa, flags=0)!=[]:
            state = 9
        else:
            print("Placa Invalida")
    if state == 5:
        print("Gracias {} en un momento te atendera un operador".format(name))
        state=0
    if state == 6:
        opcion=input("¿te puedo ayudar en algo más?  \n\t\t\t")
        if re.findall(afirmacion_RE, opcion, flags=0!=[]):
            state = 0
        elif re.findall(salir_RE, opcion, flags=0!=[]):
            state = 7

        else:
            print("No pudimos procesar tu información seras redireccionado al menu de inicio")
            state = 0
    if state == 7:
      print("Gracias fue un placer atenderte")
      Salida=0
    if state == 8:
      print("La opción no pudo ser procesada")
      state=0
    if state == 9:
      print("Me podrias dar la fecha que deseas agendar, estamos disponibles los 7 dias")
      pes=29
      pmes=1
      pano=2020
      dia=int(input("Día"))
      mes=int(input("mes"))
      ano=int(input("Año"))
      fecha = datetime.now().date()
      fecha_dada = datetime(ano, mes, dia)
      fecha_final = fecha_dada.strftime('%Y-%m-%d')
      fecha_max = datetime(2020,5,30)
      fecha_tot = fecha_max.strftime('%Y-%m-%d')
      if str(fecha_final) == str(fecha):
        print("No puedes agendar cita para el día de hoy")
        state=9
      elif str(fecha_final) < str(fecha):
        print("No puedes agendar fechas pasadas")
        state=9
      elif str(fecha) > str(fecha_tot):
        print("Aún no tenemos fechas tan lejanas")
        state=9
      else:
        state=10
    if state ==10:
      print ("ahora me puedes dar la hora, estamos disponibles de 9:00 a 18:00,recuerda las citas duran 1 hora")
      hora=int(input("Hora"))
      if hora < 9 :
          print ("A esa hora aún no estamos en servicio")
          state=10
      elif hora>17:
          print ("A esa horano ya nos retiramos lo siento")
          state=10
      else:
          print ("Listo tus datos han sido tomados te comunicaremos al operador para completar la cita")
          state=3
    if state ==11:
      print("Me puedes dar tu correo electronico")
      correo=input()
      if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',correo.lower()):
        print ("Correo correcto")
        state=3
      else:
        print ("Correo incorrecto")
        state=11

