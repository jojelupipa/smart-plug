# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import paho.mqtt.client as mqtt
import sqlite3
import datetime
import time

db_dir = "../db/"
db_power_name = db_dir + "power_consumption.db"


VERBOSE = False
keep_alive_interval = 100
MQTT_topic = "/data/consumption/#"
settings = {"user": "esp32",
            "password": "esp32tfg",
            "broker_ip": "127.0.0.1",
            "port": "1883"}


# Define Callbacks

def on_connect(client, userdata, rc):
    print("Suscribed to /data/consumption/# ", flush=True)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unable to disconnect")
    elif VERBOSE:
        print("Disconnected!")


def on_message(mosq, obj, msg):
    if VERBOSE:
        print("Topic: %s Message: %s" % (msg.topic, msg.payload))
    save_to_db(msg.topic, msg.payload.decode("utf-8"))


# Set up connection

def set_up_connection(mqttc, user, password, broker_ip, port):
    mqttc.username_pw_set(user, password)
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_message = on_message
    mqttc.connect(broker_ip, int(port), int(keep_alive_interval))
    mqttc.subscribe(MQTT_topic)


def save_to_db(topic, message):
    command = """
    INSERT INTO power_consumption_data (name, date_time, power_consumption)
    VALUES ('%s', '%s', '%s');
    """ % (topic, datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
           message)
    if VERBOSE:
        print("Executing: " + command + " into " + db_power_name + " database")
    conn = sqlite3.connect(db_power_name)
    cursor = conn.executescript(command)
    cursor.close()
    conn.close()


class Subscriber():

    def __init__(self, verbose=False):
        global VERBOSE
        VERBOSE = verbose
        self.mqttc = mqtt.Client()
        connected = False
        while not connected:
            try:
                set_up_connection(self.mqttc, settings["user"],
                                  settings["password"],
                                  settings["broker_ip"],
                                  settings["port"])
                connected = True
            except ConnectionRefusedError as e:
                print(e)
                print("Broker not ready yet.")
                time.sleep(5)

    def subscribe(self):
        self.mqttc.loop_forever()
        if VERBOSE:
            print("Ended loop", flush=True)

    def disconnect(self):
        self.mqttc.disconnect()


if __name__ == "__main__":
    subscriber = Subscriber()
    subscriber.subscribe()
