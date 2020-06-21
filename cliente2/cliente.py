import paho.mqtt.client as paho
import logging
import time
from brokerData import * #MANU Informacion de la conexion
from clienteclass import * #MANU Clase manejo de Clientes
from usuario import * #MANU Configuracion de nombre de usuario
from salas import * #MANU Configuracion de salas de usuario
#MANU Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )

#MANU Tiempo de espera 
DEFAULT_DELAY = 1 #MANU segundos

logging.info("Sesion en Linea") #MANU Mensaje en consola

#MANU Nos conectaremos a distintos topics:
qos = 2
#MANU Subscripcion simple con tupla (topic,qos)
subID = "usuarios/27/" + str(usuario)
client.subscribe((subID , qos))

for i in range(len(sala)):
    subSala = "salas/27/" + str(sala[i])
    client.subscribe((subSala, qos))
#MANU Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()

#MANU Loop principal 
try:
    while True:
        time.sleep(DEFAULT_DELAY)    #MANU Retardo hasta la proxima publicacion de info
        MENU1 = texto(input("ENVIAR TEXTO = 1 \nENVIAR AUDIO = 2 \nSeleccion:\n"))
        MENU1.menu()
        
except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")

finally:
    client.disconnect()
    logging.info("Se ha desconectado del broker. Saliendo...")