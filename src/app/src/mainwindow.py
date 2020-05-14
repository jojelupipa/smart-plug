# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import sys
import subprocess
import app_utils
import SettingsWindows
import PlugListWindow
import paho_sub
import threading
from PySide2 import QtWidgets


''' Main Window '''


class HomeWindow(QtWidgets.QMainWindow):
    main_window = app_utils.UI_PATH + "main_window.ui"

    def __init__(self, parent=None):
        super(HomeWindow, self).__init__(parent)
        self.window = app_utils.load_scene(self.main_window)
        self.create_database()
        self.button_plug_list = self.window.central_widget.findChild(QtWidgets.QPushButton, "open_plug_list")
        self.button_plug_list.clicked.connect(self.open_plug_list_widget)
        self.button_settings = self.window.central_widget.findChild(QtWidgets.QPushButton, "settings_button")
        self.button_settings.clicked.connect(self.open_settings_widget)
        self.status_text = self.window.central_widget.findChild(QtWidgets.QLabel, "status_text")
        self.subscriber = None
        self.subscribe_to_broker()
        self.resize(self.window.size())
        self.setCentralWidget(self.window)

    def open_plug_list_widget(self):
        window_plug_list = PlugListWindow.PlugListWindow()
        window_plug_list.window.setModal(True)
        self.hide()
        window_plug_list.window.exec()
        self.show()
        self.resubscribe()

    def open_settings_widget(self):
        window_settings = SettingsWindows.SettingsWindows()
        window_settings.window.setModal(True)
        self.hide()
        window_settings.window.exec()
        self.show()
        self.resubscribe()

    def resubscribe(self):
        try:
           self.subscriber.disconnect()
        except AttributeError:
            print("Reintentando suscripción al broker", flush=True)
        self.subscribe_to_broker()

    def create_database(self, force=False):
        command = "python create_database.py"
        if force:
            command += " -f"
        subprocess.call(command, shell=True)

    def closeEvent(self, event):
        self.subscriber.disconnect()
        event.accept()

    def subscribe_to_broker(self):
        try:
            self.subscriber = paho_sub.Subscriber()
            thr = threading.Thread(target=self.subscriber.subscribe, args=(), kwargs={})
            thr.start()
            self.status_text.setText("Conectado")
        except (AttributeError, subprocess.CalledProcessError, OSError) as e:
            self.status_text.setText("Desconectado, revise conexión con el servidor")
            print(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    home_window = HomeWindow()
    home_window.show()

    sys.exit(app.exec_())
