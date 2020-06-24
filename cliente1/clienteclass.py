import paho.mqtt.client as paho
import logging
from brokerData import * #MANU Informacion de la conexion
import os 
#MANU Nombres de Topics 
USUARIOS = 'usuarios'
SALAS = 'salas'
AUDIO = 'audio'
GRUPO = '27'
#MANU Handler en caso suceda la conexion con el broker MQTT
def on_connect(client, userdata, flags, rc): 
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
    logging.info(connectionText)

#MANU Handler en caso se publique satisfactoriamente en el broker MQTT
def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)

#MANU Callback que se ejecuta cuando llega un mensaje al topic suscrito
def on_message(client, userdata, msg):
    from datetime import datetime
    #MANU Se muestra en pantalla informacion que ha llegado
    logging.info("Fuente: " + str(msg.topic))
    firstopic = '{:.5}'.format(str(msg.topic))
    if firstopic == 'audio':#AAMS Se compara si el mensaje llegado fue de Audio o Texto
        now = datetime.now()
        name_ar = str(int(datetime.timestamp(now))) + '.wav' #AAMS Nombre del archivo de audio para el receptor del mismo
        archivo = open(name_ar,'wb') #AAMS Abrir para SOBREESCRIBIR el archivo existente
        a = msg.payload
        archivo.write(a) #AAMS Sobreescribiendo el archivo de audio
        archivo.close() #AAMS Siempre cerrar el archivo al finalizar la escritura
        escuchar = 'aplay ' + name_ar
        os.system(escuchar) #AAMS Reproduccion del archivo de audio
        print("ENVIAR TEXTO = 1 \nENVIAR AUDIO = 2 \nSeleccion:")
    else:
        logging.info("\n1 Mensaje Recibido: " + str(msg.payload))
        print("ENVIAR TEXTO = 1 \nENVIAR AUDIO = 2 \nSeleccion:")
    
client = paho.Client(clean_session=True) #MANU Nueva instancia de cliente
client.on_connect = on_connect #MANU Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message #MANU Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.on_publish = on_publish #MANU Se configura la funcion "Handler" que se activa al publicar algo
client.username_pw_set(MQTT_USER, MQTT_PASS) #MANU Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #MANUConectar al servidor remoto

def publishData(topicRoot, topicName, value, qos = 0, retain = False): #MANU Funcion para recibir topics y publicarlos
    topic = topicRoot + "/" + topicName
    client.publish(topic, value, qos, retain)

def fileReadU(fileName = 'usuario'):#MANU leer el archivo de texto plano
    archivo = open(fileName,'r') #MANU Abrir el archivo en modo de LECTURA
    for line in archivo: #MANU Leer cada linea del archivo
        usuario = (line) #MANU Guardar el texto de USUARIO
    return usuario
    archivo.close()

def fileReadS(fileName = 'salas'):#MANU leer el archivo de texto plano
    archivo = open(fileName,'r') #MANU Abrir el archivo en modo de LECTURA
    sala = []
    for line in archivo: #MANU Leer cada linea del archivo
        sala.append('{:.3}'.format(line)) #MANU lista de SALAS 
    return sala
    archivo.close()


def fileReadAU(fileName = 'prueba.wav'):#AAMS Creacion el archivo de audio local
    tiempo = input('Duracion: ')
    if int(tiempo) > 30:#AAMS Limitacion del tiempo a solo 30 segundos maximo
        print('El mensaje No debe ser mayor a 30 Segundos')
    else:
        comando = 'arecord -d' + tiempo + ' -f U8 -r 8000 prueba.wav'
        logging.info('Comenzando grabacion')
        os.system(comando)
        logging.info('Grabacion finalizada')
        archivo = open(fileName,'rb') #AAMS Abrir el archivo en modo de LECTURA
        for line in archivo: #AAMS Leer cada linea del archivo
            a = line #AAMS Guardar el texto del archivo leido
        return a
        archivo.close() #AAMS Cerrar el archivo al finalizar
        
#OOP[PARA CLIENTES]
class   texto(object): #MANU CLASE PARA EL MANEJO DE LA INTERFAZ DEL CLIENTE
    def __init__(self, MENU1):#MANU CONSTRUCTOR
        self.MENU1 = str(MENU1)


    
    def menu(self):
        estado = 0
        if str(self.MENU1) == '1':#AAMS El usuario desea enviar texto
            MENU2 = input("ENVIAR A USUARIO = 1 \nENVIAR A SALA = 2 \nSeleccion:\n")
            if MENU2 == '1': # AAMS el Usuario desea enviar texto a un usuario
                DESTINO = input("Destinatario/Usuario: \n")
                texto_enviar = input("Escribir mensaje: \n")
                publishData(USUARIOS, GRUPO + "/" + DESTINO , texto_enviar)
                logging.info("Mensaje enviado\n")
            if MENU2 == '2':# AAMS el usuario desea enviar texto a una sala
                DESTINO = input("Destinatario/#Sala: \n")
                texto_enviar = input("Escribir mensaje: \n")
                publishData(SALAS, GRUPO + "/" + DESTINO , texto_enviar)
                logging.info("Mensaje enviado\n")
            estado = 0 #AAMS El while principal seguira funcionando
            return estado
        if str(self.MENU1) == '2': # AAMS El usuario desea enviar un audio
            MENU2 = input("ENVIAR A USUARIO = 1 \nENVIAR A SALA = 2 \nSeleccion:\n")
            if MENU2 == '1':#AAMS El usuario desea enviar un audio a un usuario
                DESTINO = input("Destinatario/Usuario: \n")
                textob = fileReadAU()
                if textob != None:
                    publishData(AUDIO, GRUPO + "/" + DESTINO , textob)
                    logging.info("Mensaje enviado\n")
            if MENU2 == '2':#AAMS El usuario desea enviar un audio a una sala
                DESTINO = input("Destinatario/#Sala: \n")
                textob = fileReadAU()
                publishData(AUDIO, GRUPO + "/" + DESTINO , textob)
                logging.info("Mensaje enviado\n")
            estado = 0#AAMS El while principal seguira funcionando
            return estado
        if str(self.MENU1) == '3':#AAMS El usuario desea cerrar su sesion
            estado = 1#AAMS El while principal dejara de funcionar
            return estado
            
            

   