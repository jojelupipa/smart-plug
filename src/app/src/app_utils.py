# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import sqlite3
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

def getFromDB(name="general"):
    conn = sqlite3.connect(CONSUMPTION_PATH)
    if name == "general":
        cursor = conn.execute("SELECT * FROM power_consumption_data")
    else:
        cursor = conn.execute("SELECT * FROM power_consumption_data WHERE name = '/data/consumption/" + name + "'")
    result = ""
    for row in cursor:
        result += str(row) + "\n"
    return result

