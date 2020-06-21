import paho.mqtt.client as paho
import logging
import time
import random
from brokerData import * #MANU Informacion de la conexion

#MANU Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )

#MANU Nombres de Topics 
USUARIOS = 'usuarios'
GRUPO = '27'

#MANU Tiempo de espera 
DEFAULT_DELAY = 1 #MANU segundos

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
    logging.info("\n1 Mensaje Recibido: " + str(msg.payload))


logging.info("Sesion en Linea") #MANU Mensaje en consola


'''
MANU Config. inicial del cliente MQTT
'''
client = paho.Client(clean_session=True) #MANU Nueva instancia de cliente
client.on_connect = on_connect #MANU Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message #MANU Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.on_publish = on_publish #MANU Se configura la funcion "Handler" que se activa al publicar algo
client.username_pw_set(MQTT_USER, MQTT_PASS) #MANU Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #MANUConectar al servidor remoto

#MANU Funcion para la publicacion de mensajes
def publishData(topicRoot, topicName, value, qos = 0, retain = False):
    topic = topicRoot + "/" + topicName
    client.publish(topic, value, qos, retain)


#Nos conectaremos a distintos topics:
qos = 2

#Subscripcion simple con tupla (topic,qos)
client.subscribe(("usuarios/27/201706485", qos))

#Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()

#MANU Loop principal 
try:
    while True:
        time.sleep(DEFAULT_DELAY)    
        MENU1 = input("ENVIAR TEXTO = 1 \nENVIAR AUDIO = 2 \nSeleccion:\n")
        if MENU1 == '1':
            MENU2 = input("ENVIAR A USUARIO = 1 \nENVIAR A SALA = 2 \nSeleccion:\n")
            if MENU2 == '1':
                DESTINO = input("Destinatario/Usuario: \n")
                texto_enviar = input("Escribir mensaje: \n")
                publishData(USUARIOS, GRUPO + "/" + DESTINO , texto_enviar)
                logging.info("Mensaje enviado\n")
            if MENU2 == '2':
                print("Funcion en Desarrollo")
        if MENU1 == '2':
                print("Funcion en Desarrollo")

                    

        #MANU Retardo hasta la proxima publicacion de info
        

except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")

finally:
    client.disconnect()
    logging.info("Se ha desconectado del broker. Saliendo...")