# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import app_utils
import subprocess
from PySide2 import QtWidgets, QtCharts, QtGui, QtCore

MQTT_Topic_Toggle = "/control/toggle/"


class PlugWindow:
    plug = app_utils.UI_PATH + "./plug.ui"

    def __init__(self, name="general"):
        self.name = name
        self.window = app_utils.load_scene(self.plug)
        self.window.setWindowTitle(self.name)
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
        self.current_consumption.setText(app_utils.getFromDB(name=self.name, last=True) + " W")
        self.scatter_plot = self.get_scatter_plot()
        self.scatter_plot_layout = self.window.findChild(QtWidgets.QLayout, "scatter_plot_layout")
        self.scatter_plot_layout.addWidget(self.scatter_plot)

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
        log_text.insertPlainText(app_utils.getFromDB(name=self.name))
        log.exec()

    def get_scatter_plot(self):
        data_series = QtCharts.QtCharts.QScatterSeries()
        data_series.setMarkerSize(15.0)
        data = app_utils.get_date_power(self.name)
        for row in data:
            time = QtCore.QDateTime()
            time.setSecsSinceEpoch(row[0].timestamp())
            data_series.append(time.toMSecsSinceEpoch(), row[1])
            #data_series.append(row[0].timestamp(), row[1])

        chart = QtCharts.QtCharts.QChart()
        chart.setAnimationOptions(QtCharts.QtCharts.QChart.AllAnimations)
        axis_x = QtCharts.QtCharts.QDateTimeAxis()
        axis_x.setTickCount(10)
        axis_x.setFormat("dd-MM hh:mm")
        axis_x.setTitleText("Fecha")
        axis_y = QtCharts.QtCharts.QValueAxis()
        axis_y.setLabelFormat("%.1f")
        axis_y.setTitleText("Consumo (W)")
        chart_viewer = QtCharts.QtCharts.QChartView(chart)
        chart_viewer.setRenderHint(QtGui.QPainter.Antialiasing)
        chart_viewer.chart().addSeries(data_series)
        chart_viewer.chart().addAxis(axis_x, QtCore.Qt.AlignmentFlag.AlignBottom)
        chart_viewer.chart().addAxis(axis_y, QtCore.Qt.AlignmentFlag.AlignLeft)
        data_series.attachAxis(axis_x)
        data_series.attachAxis(axis_y)
        chart_viewer.chart().setDropShadowEnabled(False)
        chart_viewer.chart().legend().hide()

        return chart_viewer
