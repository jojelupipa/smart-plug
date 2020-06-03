# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import app_utils
import subprocess
import PlugWindow
from PySide2 import QtWidgets, QtCore


''' Plug List Window '''


class PlugListWindow:
    plug_list = app_utils.UI_PATH + "./smart_plug_list.ui"

    def __init__(self):
        self.window = app_utils.load_scene(self.plug_list)
        self.button_back = self.window.findChild(QtWidgets.QPushButton,
                                            "back_button")
        self.button_back.clicked.connect(self.back)
        self.signal_mapper = QtCore.QSignalMapper(self.window)
        self.signal_mapper.mapped[str].connect(self.plug_button)
        self.button_general = self.window.findChild(QtWidgets.QPushButton,
                                               "general_button")
        self.button_general.clicked.connect(self.signal_mapper.map)
        self.signal_mapper.setMapping(self.button_general, "general")
        self.update_plug_list()
        self.update_status()

    def update_status(self):
        status_label = self.window.findChild(QtWidgets.QLabel, "status_label")
        if app_utils.check_connection():
            status_label.setText("Conectado al broker")
        else:
            status_label.setText("Error de conexión\nRevise ajustes y servidor")
            self.button_general.setEnabled(False)

    def update_plug_list(self):
        plug_layout = self.window.findChild(QtWidgets.QVBoxLayout, "plugs_layout")
        plugs = app_utils.get_plug_list()
        for plug in plugs:
            button = QtWidgets.QPushButton(plug)
            button.clicked.connect(self.signal_mapper.map)
            self.signal_mapper.setMapping(button, plug)
            plug_layout.addWidget(button)

    def back(self):
        self.window.close()

    def plug_button(self, name="general"):
        window_general_plug = PlugWindow.PlugWindow(name=name)
        window_general_plug.window.setModal(True)
        window_general_plug.window.exec()
        self.update_status()

