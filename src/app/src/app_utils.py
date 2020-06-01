# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import sqlite3
import datetime
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
    conn = sqlite3.connect(CONSUMPTION_PATH)
    column = "*"
    if last:
        column = "power_consumption"
    if name == "general":
        cursor = conn.execute("SELECT " + column + " FROM power_consumption_data")
    else:
        cursor = conn.execute("SELECT " + column + " FROM power_consumption_data WHERE name = '/data/consumption/" + name + "'")
    result = ""
    if not last:
        for row in cursor:
            result += str(row) + "\n"
    else:
        result = cursor.fetchall()[-1][0]
    return result


def get_date_power(name="general"):
    where_clause = ""
    if name != "general":
        where_clause = " WHERE name = '/data/consumption/" + name + "'"
    conn = sqlite3.connect(CONSUMPTION_PATH)
    cursor = conn.execute("SELECT date_time, power_consumption FROM power_consumption_data" + where_clause)
    result = cursor.fetchall()
    formated_result = []
    for row in result:
        formated_result.append([datetime.datetime.strptime(row[0], "%a %b %d %H:%M:%S %Y"),
                               float(row[1])])
    return formated_result

def get_plug_list():
    conn = sqlite3.connect(CONSUMPTION_PATH)
    cursor = conn.execute("SELECT DISTINCT name FROM power_consumption_data")
    result = cursor.fetchall()
    list = []
    for row in result:
        plug_name = row[0].replace("/data/consumption/","")
        list.append(plug_name)
    return list
