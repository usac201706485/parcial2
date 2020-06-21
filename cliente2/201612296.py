import paho.mqtt.client as mqtt
import logging
import time
import os 
from brokerData import * #MANU Informacion de la conexion


#MANU Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

#MANU Nombres de Topics 
USUARIOS = 'usuarios'
GRUPO = '27'

#MANU Tiempo de espera 
DEFAULT_DELAY = 1 #MANU segundos

#MANU Callback que se ejecuta cuando nos conectamos al broker
def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")

#MANU Callback que se ejecuta cuando llega un mensaje al topic suscrito
def on_message(client, userdata, msg):
    #MANU Se muestra en pantalla informacion que ha llegado
    logging.info("\n1 Mensaje Recibido: " + str(msg.payload))

#MANU Handler en caso se publique satisfactoriamente en el broker MQTT
def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)

    
client = mqtt.Client(clean_session=True) #MANU Nueva instancia de cliente 
client.on_connect = on_connect #MANU Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message #MANU Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.on_publish = on_publish #MANU Se configura la funcion "Handler" que se activa al publicar algo
client.username_pw_set(MQTT_USER, MQTT_PASS) #MANU Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #MANU Conectar al servidor remoto

#MANU Funcion para la publicacion de mensajes
def publishData(topicRoot, topicName, value, qos = 0, retain = False):
    topic = topicRoot + "/" + topicName
    client.publish(topic, value, qos, retain)

#Nos conectaremos a distintos topics:
qos = 2

#Subscripcion simple con tupla (topic,qos)
client.subscribe(("usuarios/27/201612296", qos))


#Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()

#El thread de MQTT queda en el fondo, mientras en el main loop hacemos otra cosa

try:
    while True:
        logging.info("Sesion en linea")
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



except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")
