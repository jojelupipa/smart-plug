# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import paho.mqtt.client as mqtt
import optparse

# MQTT Settings
MQTT_Broker = "192.168.1.10"
MQTT_Port = 1883
Keep_Alive_Interval = 100
MQTT_Topic_Toggle = "/control/toggle/"
MQTT_User = "esp32"
MQTT_Password = "esp32tfg"


# Define Callbacks

def on_connect(client, userdata, rc):
    if rc != 0:
        print("Unable to connect to MQTT Broker...")
    else:
        print("Connected with MQTT Broker")


def on_publish(client, userdata, mid):
    print("Publishing to topic " + mid)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unable to disconnect")
    else:
        print("Disconnected!")


# Set up connection

def set_up_connection(mqttc, user, password, broker_ip, port):
    mqttc.username_pw_set(user, password)
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_publish = on_publish
    mqttc.connect(broker_ip, int(port), int(Keep_Alive_Interval))


# Function for publishing to a topic


def publish_to_topic(mqttc, topic, message):
    mqttc.publish(topic, message)
    print("Published: \"" + str(message) + "\" " +
          "on MQTT Topic: \"" + str(topic) + "\"")


# Set parser options


def set_parser_options(parser):
    parser.add_option('-u', '--user', action="store", dest="user",
                      help="Set MQTT user", default=MQTT_User)
    parser.add_option('-P', '--password', action="store", dest="password",
                      help="Set MQTT password", default=MQTT_Password)
    parser.add_option('-b', '--broker-ip', action="store", dest="broker_ip",
                      help="Set broker's ip", default=MQTT_Broker)
    parser.add_option('-p', '--port', action="store", dest="port",
                      help="Set MQTT port, default 1883", default=MQTT_Port)
    parser.add_option('-m', '--message', action="store", dest="message",
                      help="Set message to be sent", default="")
    parser.add_option('-t', '--topic', action="store", dest="topic",
                      help="Set MQTT topic", default=MQTT_Topic_Toggle)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    set_parser_options(parser)
    options, args = parser.parse_args()
    mqttc = mqtt.Client()
    set_up_connection(mqttc, options.user, options.password,
                      options.broker_ip, options.port)
    publish_to_topic(mqttc, options.topic, options.message)
    mqttc.disconnect(mqttc)
