import paho.mqtt.client as paho
import logging
import time
from brokerData import * #MANU Informacion de la conexion
from clienteclass import * #MANU Clase manejo de Clientes

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
client.subscribe(("usuarios/27/Ronald", qos))
client.subscribe(("salas/27/S02", qos))
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