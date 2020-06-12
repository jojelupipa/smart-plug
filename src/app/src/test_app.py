import unittest
import os
import mainwindow, PlugListWindow, PlugWindow
from PySide2 import QtWidgets, QtCore, QtCharts
import app_utils
import create_database
import paho_publish
_instance = None


class TestCreateGUI(unittest.TestCase):
    """ Clase para testear la GUI """
    def setUp(self):
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
        global _instance
        if _instance is None:
            _instance = QtWidgets.QApplication()
        self.app = _instance

    def tearDown(self):
        del self.app
        return super(TestCreateGUI, self).tearDown()

    def test_main_window_creation(self):
        print(self._testMethodName)
        main_window = mainwindow.HomeWindow()
        self.assertTrue(type(main_window.window) == QtWidgets.QMainWindow)
        self.assertTrue(type(
            main_window.button_plug_list == QtWidgets.QPushButton
        ))
        self.assertTrue(type(main_window.status_text == QtWidgets.QLabel))

    def test_plug_list_window(self):
        print(self._testMethodName)
        plug_list_w = PlugListWindow.PlugListWindow()
        self.assertTrue(type(plug_list_w.window) == QtWidgets.QDialog)
        self.assertTrue(type(plug_list_w.button_back == QtWidgets.QPushButton))
        self.assertTrue(type(
            plug_list_w.button_general == QtWidgets.QPushButton
        ))

    def test_plug_window(self):
        print(self._testMethodName)
        plug_w = PlugWindow.PlugWindow()
        self.assertTrue(type(plug_w.window) == QtWidgets.QDialog)
        self.assertTrue(type(plug_w.button_back) == QtWidgets.QPushButton)
        self.assertTrue(type(plug_w.button_toggle) == QtWidgets.QPushButton)
        self.assertTrue(type(plug_w.button_log) == QtWidgets.QPushButton)
        self.assertTrue(type(
            plug_w.scatter_plot) == QtCharts.QtCharts.QChartView
        )


class TestUtils(unittest.TestCase):
    """ Clase para probar las funciones auxiliares """

    def test_load_scene(self):
        print(self._testMethodName)
        window_test = app_utils.load_scene("../ui/plug.ui")
        self.assertTrue(type(window_test) == QtWidgets.QDialog)

    def test_get_settings(self):
        print(self._testMethodName)
        settings = app_utils.get_settings()
        self.assertTrue(type(settings["user"]) == str)
        self.assertTrue(type(settings["password"]) == str)
        self.assertTrue(type(settings["broker_ip"]) == str)
        self.assertTrue(type(settings["port"]) == str)

    def test_get_from_db(self):
        print(self._testMethodName)
        self.assertTrue(type(app_utils.getFromDB()) == str)

    def test_check_connection(self):
        print(self._testMethodName)
        self.assertTrue(type(app_utils.check_connection()) == bool)


class TestCreateDatabase(unittest.TestCase):
    """ Clase para probar la creación de la db """

    def test_create_settings_database(self):
        create_database.create_settings_database()
        create_database.check_dir()
        self.assertTrue(os.path.isdir("../db/"), "Directory creation failed")
        create_database.create_settings_database()
        self.assertTrue(os.path.isfile("../db/settings.db"),
                        "Database not created")


if __name__ == '__main__':
    unittest.main()
