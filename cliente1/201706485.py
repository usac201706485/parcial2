import paho.mqtt.client as paho
import logging
import time
import random

#Parametros de conexion
MQTT_HOST = "167.71.243.238"
MQTT_PORT = 1883

#Credenciales
#Se acostumbra solicitar al usuario que ingrese su user/pass
#no es buena practica dejar escritas en el codigo las credenciales
MQTT_USER = "proyectos"
MQTT_PASS = "proyectos980"
'''
Ejemplo de cliente MQTT: gateway de red de sensores
'''

#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )

#Nombres de Topics de ejemplo
USUARIOS = 'usuarios'
GRUPO = '27'
DESTINO = '201612296'
TEMPERATURA = 'temp'

#Cantidad de sensores de ejemplo que se simulan
CNT_SENSORES = 10

#Tiempo de espera entre lectura y envio de dato de sensores a broker (en segundos)
DEFAULT_DELAY = 240 #3 minuto

#Handler en caso suceda la conexion con el broker MQTT
def on_connect(client, userdata, flags, rc): 
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
    logging.info(connectionText)

#Handler en caso se publique satisfactoriamente en el broker MQTT
def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)


logging.info("Cliente MQTT con paho-mqtt") #Mensaje en consola


'''
Config. inicial del cliente MQTT
'''
client = paho.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto

#Mensaje de prueba MQTT en el topic "test"
client.publish("test", "Mensaje inicial", qos = 0, retain = False)


def publishData(topicRoot, topicName, value, qos = 0, retain = False):
    topic = topicRoot + "/" + topicName
    client.publish(topic, value, qos, retain)



#Loop principal: leer los datos de los sensores y enviarlos al broker en los topics adecuados cada cierto tiempo
try:
    while True:

        publishData(USUARIOS, GRUPO + "/" + DESTINO , 'HOLA QUE TAL?')

        logging.info("Mensaje enviado: HOLA QUE TAL?")            

        #Retardo hasta la proxima publicacion de info
        time.sleep(DEFAULT_DELAY)

except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")

finally:
    client.disconnect()
    logging.info("Se ha desconectado del broker. Saliendo...")