# -*- coding: utf-8 -*-
""" Simple API for SmartPlugController """

import os
import argparse
import subprocess
import threading
import sqlite3
import datetime
import src.paho_sub as paho_sub
from flask import Flask, request, jsonify

HOST_IP = "192.168.1.10"
PORT = 8080
CONSUMPTION_PATH = "../db/power_consumption.db"
app = Flask(__name__)


@app.route("/consumption", methods=["GET"])
def get_from_db():
    name = request.args.get("name")
    last = (request.args.get("last") == "True")
    conn = sqlite3.connect(CONSUMPTION_PATH)
    column = "*"
    if last:
        column = "power_consumption"
    if name == "general":
        cursor = conn.execute("SELECT " + column + " FROM power_consumption_data")
    else:
        cursor = conn.execute("SELECT " + column + " FROM power_consumption_data WHERE name = '/data/consumption/" + name + "'")
    result = ""
    if not last:
        for row in cursor:
            result += str(row) + "\n"
    else:
        result = cursor.fetchall()[-1][0]
    return result


@app.route("/last_consumption", methods=["GET"])
def get_date_power():
    name = request.args.get("name")
    where_clause = ""
    if name != "general":
        where_clause = " WHERE name = '/data/consumption/" + name + "'"
    conn = sqlite3.connect(CONSUMPTION_PATH)
    cursor = conn.execute("SELECT date_time, power_consumption FROM power_consumption_data" + where_clause)
    result = cursor.fetchall()
    formated_result = []
    for row in result:
        formated_result.append([datetime.datetime.strptime(row[0], "%a %b %d %H:%M:%S %Y"),
                                float(row[1])])
    return jsonify(formated_result)


@app.route("/plugs", methods=["GET"])
def get_plug_list():
    conn = sqlite3.connect(CONSUMPTION_PATH)
    cursor = conn.execute("SELECT DISTINCT name FROM power_consumption_data")
    result = cursor.fetchall()
    list = []
    for row in result:
        plug_name = row[0].replace("/data/consumption/", "")
        list.append(plug_name)
    return jsonify(list)


def create_database(force=False):
    command = "python src/create_database.py"
    if force:
        command += " -f"
    subprocess.call(command, shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs database simple API")
    parser.add_argument("-H", "--ip", action="store", default=HOST_IP,
                        dest="ip_addr", help="Select IP address for the API")
    parser.add_argument("-p", "--port", action="store", default=PORT,
                        dest="port", help="Select the port")
    args = parser.parse_args()

    os.chdir("src")
    create_database()
    subscriber = paho_sub.Subscriber()
    thr = threading.Thread(target=subscriber.subscribe, args=(), kwargs={})
    thr.start()
    app.run(host=args.ip_addr, port=args.port)
    subscriber.disconnect()
