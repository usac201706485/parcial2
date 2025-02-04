import paho.mqtt.client as paho
import logging
import time
from brokerData import * #MANU Informacion de la conexion
from clienteclass import * #MANU Clase manejo de Clientes

#MANU Lectura truncada de los textos planos 
sala = fileReadS()  
usuario = '{:.9}'.format(fileReadU())

#MANU Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )

#MANU Tiempo de espera [para mostrar el menu de una forma mas ordenada]
DEFAULT_DELAY = 1 #MANU segundos

logging.info("Sesion en Linea") #MANU Mensaje en consola

#MANU Nos conectaremos a distintos topics:
qos = 2
#MANU Subscripcion a los topics segun el texto plano de USUARIO
subID = "usuarios/27/" + str(usuario)
subAU = "audio/27/" + str(usuario)
client.subscribe((subID , qos))
client.subscribe((subAU , qos))
#Manu Subscripcion a los topics segun el texto plano de SALAS
for i in range(len(sala)):
    subSala = "salas/27/" + str(sala[i])
    subAUSala = "audio/27/" + str(sala[i])
    client.subscribe((subSala, qos))
    client.subscribe((subAUSala, qos))
#MANU Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()
estado = 0
#MANU Loop principal 
try:
    while estado == 0:
        time.sleep(DEFAULT_DELAY)    #MANU Retardo hasta la proxima publicacion de info
        MENU1 = texto(input("ENVIAR TEXTO = 1 \nENVIAR AUDIO = 2 \nSALIR = 3 \nSeleccion:\n"))

        estado = MENU1.menu()
        
except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...") #MANU al ejecutar ^C el programa se cierra

finally:
    client.disconnect() #MANU desconexion del broker
    logging.info("Se ha desconectado del broker. Saliendo...")