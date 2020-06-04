# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import sys
import subprocess
import app_utils
import SettingsWindows
import PlugListWindow
from PySide2 import QtWidgets


''' Main Window '''


class HomeWindow(QtWidgets.QMainWindow):
    """ Clase para controlar la ventana principal de la app """
    main_window = app_utils.UI_PATH + "main_window.ui"

    def __init__(self, parent=None):
        super(HomeWindow, self).__init__(parent)
        self.window = app_utils.load_scene(self.main_window)
        self.create_database()
        self.button_plug_list = self.window.central_widget.findChild(
            QtWidgets.QPushButton, "open_plug_list"
        )
        self.button_plug_list.clicked.connect(self.open_plug_list_widget)
        self.button_settings = self.window.central_widget.findChild(
            QtWidgets.QPushButton, "settings_button"
        )
        self.button_settings.clicked.connect(self.open_settings_widget)
        self.status_text = self.window.central_widget.findChild(
            QtWidgets.QLabel, "status_text"
        )
        self.check_connection()
        self.resize(self.window.size())
        self.setCentralWidget(self.window)

    def open_plug_list_widget(self):
        """ Abre la ventana de la lista de enchufes """
        window_plug_list = PlugListWindow.PlugListWindow()
        window_plug_list.window.setModal(True)
        self.hide()
        window_plug_list.window.exec()
        self.show()
        self.check_connection()

    def open_settings_widget(self):
        """ Abre la ventana de los ajustes """
        window_settings = SettingsWindows.SettingsWindows()
        window_settings.window.setModal(True)
        self.hide()
        window_settings.window.exec()
        self.show()
        self.check_connection()

    def create_database(self, force=False):
        """ Crea la base de datos """
        command = "python create_database.py"
        if force:
            command += " -f"
        subprocess.call(command, shell=True)

    def check_connection(self):
        """ Comprueba la conexión con el broker """
        status_label = self.window.findChild(QtWidgets.QLabel, "status_text")
        if app_utils.check_connection():
            status_label.setText("Conectado al broker")
        else:
            status_label.setText(
                "Error de conexión\nRevise ajustes y servidor"
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    home_window = HomeWindow()
    home_window.show()

    sys.exit(app.exec_())
