# This Python file uses the following encoding: utf-8

# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

import os
import sqlite3
import optparse

"""
Script para la creación de una base de datos para almacenar el
consumo energético
"""


db_dir = "../db/"
db_power_name = db_dir + "power_consumption.db"
db_power_schema = """
create table if not exists power_consumption_data (
  id integer primary key autoincrement,
  name text not null,
  date_time text not null,
  power_consumption text not null
);
"""


def set_parser_options(parser):
    """ Crea opciones del parser """
    parser.add_option('-f', '--force', action="store_true", dest="force",
                      help="Overwrite any existing database", default=False)


def create_power_database(force=False):
    """ Crea la base de datos del consumo energético.
        force: booleano para sobreescribir una base de datos si existía
    """
    creation_command = ""
    if force:
        creation_command += "drop table if exists power_consumption_data;"
    creation_command += db_power_schema
    # Create database (connection)
    connection = sqlite3.connect(db_power_name)
    # Create
    cursor = connection.cursor()
    cursor.executescript(creation_command)
    # Close database
    cursor.close()
    connection.close()


def check_dir():
    if not os.path.isdir(db_dir):
        os.makedirs(db_dir)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    set_parser_options(parser)
    options, args = parser.parse_args()
    check_dir()
    if options.force:
        create_power_database(force=True)
    else:
        create_power_database()
