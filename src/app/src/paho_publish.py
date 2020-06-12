# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

""" Script para publicar mensajes en un topic a un broker """

import sys
import paho.mqtt.client as mqtt
import optparse

# MQTT Settings
MQTT_Broker = "192.168.1.10"
MQTT_Port = 1883
Keep_Alive_Interval = 100
MQTT_Topic_Toggle = "/control/toggle/"
MQTT_User = "esp32"
MQTT_Password = "esp32tfg"
VERBOSE = False


# Define Callbacks

def on_connect(client, userdata, rc):
    """ Callback conexión del cliente paho """
    if rc != 0:
        print("Unable to connect to MQTT Broker...")
    else:
        print("Connected with MQTT Broker")


def on_publish(client, userdata, mid):
    """ Callback publicación de un mensaje al broker """
    print("Publishing to topic " + mid)


def on_disconnect(client, userdata, rc):
    """ Callback desconexión del cliente paho """
    if rc != 0:
        print("Unable to disconnect")
    elif VERBOSE:
        print("Disconnected!")


# Set up connection

def set_up_connection(mqttc, user, password, broker_ip, port):
    """ Establece la conexión con los parámetros del servidor """
    mqttc.username_pw_set(user, password)
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_publish = on_publish
    try:
        mqttc.connect(broker_ip, int(port), int(Keep_Alive_Interval))
    except OSError as e:
        if VERBOSE:
            print(e)
            print("Unable to connect. Check server status")
        return 1
    return 0

# Function for publishing to a topic


def publish_to_topic(mqttc, topic, message):
    """ Gestiona la publicación en un topic de mqtt """
    mqttc.publish(topic, message)
    if VERBOSE:
        print("Published: \"" + str(message) + "\" " +
              "on MQTT Topic: \"" + str(topic) + "\"")


# Set parser options


def set_parser_options(parser):
    """ Añade parámetros al script """
    parser.add_option("-u", "--user", action="store", dest="user",
                      help="Set MQTT user", default=MQTT_User)
    parser.add_option("-P", "--password", action="store", dest="password",
                      help="Set MQTT password", default=MQTT_Password)
    parser.add_option("-b", "--broker-ip", action="store", dest="broker_ip",
                      help="Set broker's ip", default=MQTT_Broker)
    parser.add_option("-p", "--port", action="store", dest="port",
                      help="Set MQTT port, default 1883", default=MQTT_Port)
    parser.add_option("-m", "--message", action="store", dest="message",
                      help="Set message to be sent", default="")
    parser.add_option("-t", "--topic", action="store", dest="topic",
                      help="Set MQTT topic", default=MQTT_Topic_Toggle)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="Verbose output", default=False)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    set_parser_options(parser)
    options, args = parser.parse_args()
    mqttc = mqtt.Client()
    result = set_up_connection(mqttc, options.user, options.password,
                               options.broker_ip, options.port)
    publish_to_topic(mqttc, options.topic, options.message)
    mqttc.disconnect(mqttc)
    sys.exit(result)
