# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import sys
import subprocess
import app_utils
import SettingsWindows
import PlugListWindow
import threading
from PySide2 import QtWidgets


''' Main Window '''


class HomeWindow(QtWidgets.QMainWindow):
    main_window = app_utils.UI_PATH + "main_window.ui"

    def __init__(self):
        self.window = app_utils.load_scene(self.main_window)
        self.create_database()
        button_plug_list = self.window.central_widget.findChild(QtWidgets.QPushButton, "open_plug_list")
        button_plug_list.clicked.connect(self.open_plug_list_widget)
        button_settings = self.window.central_widget.findChild(QtWidgets.QPushButton, "settings_button")
        button_settings.clicked.connect(self.open_settings_widget)
        thr = threading.Thread(target=self.sub_to_broker, args=(), kwargs={})
        thr.start()

    def open_plug_list_widget(self):
        window_plug_list = PlugListWindow.PlugListWindow()
        window_plug_list.window.setModal(True)
        self.window.hide()
        window_plug_list.window.exec()
        self.window.show()

    def open_settings_widget(self):
        window_settings = SettingsWindows.SettingsWindows()
        window_settings.window.setModal(True)
        self.window.hide()
        window_settings.window.exec()
        self.window.show()

    def create_database(self, force=False):
        command = "python create_database.py"
        if force:
            command += " -f"
        subprocess.call(command, shell=True)

    def sub_to_broker(self):
        command = "python paho_sub.py"
        subprocess.call(command, shell=True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    home_window = HomeWindow()
    home_window.window.show()

    sys.exit(app.exec_())
