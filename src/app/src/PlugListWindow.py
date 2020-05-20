# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import app_utils
import subprocess
import PlugWindow
from PySide2 import QtWidgets


''' Plug List Window '''


class PlugListWindow:
    plug_list = app_utils.UI_PATH + "./smart_plug_list.ui"

    def __init__(self):
        self.window = app_utils.load_scene(self.plug_list)
        self.button_back = self.window.findChild(QtWidgets.QPushButton,
                                            "back_button")
        self.button_back.clicked.connect(self.back)
        self.button_general = self.window.findChild(QtWidgets.QPushButton,
                                               "general_button")
        self.button_general.clicked.connect(self.general_button)
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
        pub_command += " -m 'client_connection_check'"
        try:
            subprocess.check_output(pub_command,
                                    shell=True)
            status_label.setText("Conectado al broker")
        except subprocess.CalledProcessError:
            status_label.setText("Error de conexión\nRevise ajustes y servidor")
            self.button_general.setEnabled(False)

    def back(self):
        self.window.close()

    def general_button(self):
        window_general_plug = PlugWindow.PlugWindow(name="general")
        window_general_plug.window.setModal(True)
        window_general_plug.window.exec()

