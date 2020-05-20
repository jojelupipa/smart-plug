# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import app_utils
from PySide2 import QtCore
from PySide2 import QtWidgets
import subprocess

class SettingsWindows:
    settings_ui_path = app_utils.UI_PATH + "settings.ui"

    def __init__(self):
        self.window = app_utils.load_scene(self.settings_ui_path)
        self.settings = app_utils.get_settings()
        self.button_box = self.window.findChild(QtWidgets.QDialogButtonBox, "button_box")
        self.button_box.accepted.connect(self.save_settings)
        self.button_box.rejected.connect(self.back)
        self.user_textbox = self.window.findChild(QtWidgets.QTextEdit, "user_text")
        self.user_textbox.setText(self.settings["user"])
        self.password_textbox = self.window.findChild(QtWidgets.QTextEdit, "password_text")
        self.password_textbox.setText(self.settings["password"])
        self.broker_ip_textbox = self.window.findChild(QtWidgets.QTextEdit, "broker_ip_text")
        self.broker_ip_textbox.setText(self.settings["broker_ip"])
        self.port_textbox = self.window.findChild(QtWidgets.QTextEdit, "port_text")
        self.port_textbox.setText(self.settings["port"])
        self.reset_checkbox = self.window.findChild(QtWidgets.QCheckBox, "reset_database_checkbox")

    def update_local_settings(self):
        user_textbox = self.window.findChild(QtWidgets.QTextEdit, "user_text")
        self.settings["user"] = user_textbox.toPlainText()
        password_textbox = self.window.findChild(QtWidgets.QTextEdit, "password_text")
        self.settings["password"] = password_textbox.toPlainText()
        broker_ip_textbox = self.window.findChild(QtWidgets.QTextEdit, "broker_ip_text")
        self.settings["broker_ip"] = broker_ip_textbox.toPlainText()
        port_textbox = self.window.findChild(QtWidgets.QTextEdit, "port_text")
        self.settings["port"] = port_textbox.toPlainText()

    def save_settings(self):
        self.update_local_settings()
        app_utils.set_settings(self.settings)
        print("Saved settings")
        if self.reset_checkbox.isChecked():
            subprocess.call("pyhton create_database.py -f", shell=True)

    def back(self):
        self.window.close()
