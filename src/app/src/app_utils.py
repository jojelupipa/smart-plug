# This Python file uses the following encoding: utf-8
# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------


import sqlite3
from dateutil import parser
import subprocess
import requests
from PySide2 import QtCore, QtWidgets
from PySide2.QtUiTools import QUiLoader

UI_PATH = "../ui/"
SETTINGS_PATH = "../db/settings.db"
CONSUMPTION_PATH = "../db/power_consumption.db"


''' Main functions'''

def load_scene(file_name):
    loader = QUiLoader()
    file = QtCore.QFile(file_name)
    file.open(QtCore.QFile.ReadOnly)
    file.close()
    return loader.load(file, None)


def get_settings():
    settings = {}
    conn = sqlite3.connect(SETTINGS_PATH)
    # Create
    cursor = conn.execute("SELECT * FROM settings")
    for row in cursor:
        settings[row[0]] = row[1]
    return settings


def set_settings(settings):
    conn = sqlite3.connect(SETTINGS_PATH)
    cursor = conn.cursor()
    for parameter in settings:
        cursor.executescript("UPDATE settings SET value = '" + settings[parameter] + "' WHERE parameter = '" + parameter + "';")


def getFromDB(name="general", last=False):
    settings = get_settings()
    url = "http://" + settings["broker_ip"] + ":8080/consumption"
    params = {"name": name, "last": last}
    result = requests.get(url=url, params=params).json()
    return result


def get_date_power(name="general"):
    settings = get_settings()
    url = "http://" + settings["broker_ip"] + ":8080/date_power"
    params = {"name": name}
    result = requests.get(url=url, params=params).json()
    formated_result = []
    for row in result:
        formated_result.append([parser.parse(row[0]), float(row[1])])
    return formated_result

def get_plug_list():
    settings = get_settings()
    url = "http://" + settings["broker_ip"] + ":8080/plugs"
    list = requests.get(url).json()
    return list

def check_connection():
    settings = get_settings()
    pub_command = "python paho_publish.py"
    pub_command += " -u " + settings["user"]
    pub_command += " -P " + settings["password"]
    pub_command += " -b " + settings["broker_ip"]
    pub_command += " -p " + settings["port"]
    pub_command += " -t /control/connection/"
    pub_command += " -m 'client_connection_check'"
    try:
        subprocess.check_output(pub_command,
                                shell=True)
        return True
    except subprocess.CalledProcessError:
        return False
