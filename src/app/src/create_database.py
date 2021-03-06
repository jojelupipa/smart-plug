# This Python file uses the following encoding: utf-8
# ------------------------------------------
# --- Author: Jesús Sánchez de Lechina Tejada
# ------------------------------------------

"""
Script para la creación de una base de datos para almacenar la
configuración de conexión al broker.
"""

import os
import sqlite3
import optparse

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
db_settings_name = db_dir + "settings.db"
db_settings_schema = """
create table if not exists settings (
  parameter text primary key not null,
  value text not null
);
"""
# Insert default settings into database if aren't already defined
db_default_settings = """
insert into settings select 'user', 'esp32'
where not exists(select 1 from settings where parameter = 'user');
insert into settings select 'password', 'esp32tfg'
where not exists(select 1 from settings where parameter = 'password');
insert into settings select 'broker_ip', '192.168.1.10'
where not exists(select 1 from settings where parameter = 'broker_ip');
insert into settings select 'port', '1883'
where not exists(select 1 from settings where parameter = 'port');
"""


def set_parser_options(parser):
    """ Crea opciones del parser """
    parser.add_option('-f', '--force', action="store_true", dest="force",
                      help="Overwrite any existing database", default=False)


def create_settings_database(force=False):
    """ Crea la base de datos de la configuración de conexión.
        force: booleano para sobreescribir una base de datos si existía
    """
    creation_command = ""
    if force:
        creation_command += "drop table if exists settings;"
    creation_command += db_settings_schema
    creation_command += db_default_settings
    # Create database (connection)
    connection = sqlite3.connect(db_settings_name)
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
        create_settings_database(force=True)
    else:
        create_settings_database()
