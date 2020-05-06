# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import app_utils
import subprocess
from PySide2 import QtWidgets


''' Plug List Window '''


class PlugListWindow(QtWidgets.QDialog):
    plug_list = app_utils.UI_PATH + "./smart_plug_list.ui"
    window = None

    def __init__(self):
        self.window = app_utils.load_scene(self.plug_list)
        button_back = self.window.findChild(QtWidgets.QPushButton,
                                            "back_button")
        button_back.clicked.connect(self.back)
        button_general_toggle = self.window.findChild(QtWidgets.QPushButton,
                                                      "general_toggle")
        button_general_toggle.clicked.connect(self.general_toggle)
        self.update_status()

    def update_status(self):
        status_label = self.window.findChild(QtWidgets.QLabel, "status_label")
        settings = app_utils.get_settings()
        pub_command = "python paho_publish.py"
        pub_command += " -u " + settings["user"]
        pub_command += " -P " + settings["password"]
        pub_command += " -b " + settings["broker_ip"]
        pub_command += " -p " + settings["port"]
        pub_command += " -t /control/connection/"
        pub_command += " -m 'connection test'"
        try:
            subprocess.check_output(pub_command,
                                    shell=True)
            status_label.setText("Conectado")
        except subprocess.CalledProcessError:
            status_label.setText("Error de conexión\nRevise ajustes y servidor")
            button_general_toggle = self.window.findChild(QtWidgets.QPushButton,
                                                          "general_toggle")
            button_general_toggle.setEnabled(False)

    def back(self):
        self.window.close()

    def general_toggle(self):
        pub_command = "python paho_publish.py"
        settings = app_utils.get_settings()
        pub_command += " -u " + settings["user"]
        pub_command += " -P " + settings["password"]
        pub_command += " -b " + settings["broker_ip"]
        pub_command += " -p " + settings["port"]
        pub_command += " -m 'general toggle'"
        subprocess.call(pub_command,
                        shell=True)
