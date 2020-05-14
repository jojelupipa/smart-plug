# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import app_utils
import subprocess
from PySide2 import QtWidgets

MQTT_Topic_Toggle = "/control/toggle/"


class PlugWindow:
    plug = app_utils.UI_PATH + "./plug.ui"

    def __init__(self, name="general"):
        self.window = app_utils.load_scene(self.plug)
        self.button_back = self.window.findChild(QtWidgets.QPushButton,
                                            "back_plug_button")
        self.button_back.clicked.connect(self.back)
        self.button_toggle = self.window.findChild(QtWidgets.QPushButton,
                                              "toggle")
        self.button_toggle.clicked.connect(self.toggle)
        self.button_log = self.window.findChild(QtWidgets.QPushButton,
                                                "history_button")
        self.button_log.clicked.connect(self.show_log)
        self.current_consumption = self.window.findChild(QtWidgets.QLabel, "updated_consumption_label")
        self.current_consumption.setText(app_utils.getFromDB(name=name, last=True) + "W")
        self.name = name

    def back(self):
        self.window.close()

    def toggle(self):
        pub_command = "python paho_publish.py"
        settings = app_utils.get_settings()
        pub_command += " -u " + settings["user"]
        pub_command += " -P " + settings["password"]
        pub_command += " -b " + settings["broker_ip"]
        pub_command += " -p " + settings["port"]
        pub_command += " -t " + MQTT_Topic_Toggle + self.name
        pub_command += " -m '" + self.name + " toggle'"
        subprocess.call(pub_command,
                        shell=True)

    def show_log(self):
        print("Showing log", flush=True)
        log = app_utils.load_scene(app_utils.UI_PATH + "consumption_log.ui")
        log.setModal(True)
        log_text = log.findChild(QtWidgets.QPlainTextEdit, "log")
        log_text.insertPlainText(app_utils.getFromDB(name="enchufe001"))
        log.exec()
