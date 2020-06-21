#OOP PARA LA TRANSMISION DE MENSAJES DE TEXT
import paho.mqtt.client as paho
import logging
from brokerData import * #MANU Informacion de la conexion
#MANU Nombres de Topics 
USUARIOS = 'usuarios'
SALAS = 'salas'
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
    #MANU Se muestra en pantalla informacion que ha llegado
    logging.info("Fuente: " + str(msg.topic))
    logging.info("\n1 Mensaje Recibido: " + str(msg.payload))
client = paho.Client(clean_session=True) #MANU Nueva instancia de cliente
client.on_connect = on_connect #MANU Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message #MANU Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.on_publish = on_publish #MANU Se configura la funcion "Handler" que se activa al publicar algo
client.username_pw_set(MQTT_USER, MQTT_PASS) #MANU Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #MANUConectar al servidor remoto

def publishData(topicRoot, topicName, value, qos = 0, retain = False):
    topic = topicRoot + "/" + topicName
    client.publish(topic, value, qos, retain)

class   texto(object):
    def __init__(self, MENU1):
        self.MENU1 = str(MENU1)


    
    def menu(self):
        if str(self.MENU1) == '1':
            MENU2 = input("ENVIAR A USUARIO = 1 \nENVIAR A SALA = 2 \nSeleccion:\n")
            if MENU2 == '1':
                DESTINO = input("Destinatario/Usuario: \n")
                texto_enviar = input("Escribir mensaje: \n")
                publishData(USUARIOS, GRUPO + "/" + DESTINO , texto_enviar)
                logging.info("Mensaje enviado\n")
            if MENU2 == '2':
                DESTINO = input("Destinatario/#Sala: \n")
                texto_enviar = input("Escribir mensaje: \n")
                publishData(SALAS, GRUPO + "/" + DESTINO , texto_enviar)
                logging.info("Mensaje enviado\n")
        if str(self.MENU1) == '2':
                print("Funcion en Desarrollo")

   