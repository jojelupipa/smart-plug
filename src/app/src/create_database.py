# Python Ver: 2.7

import os
import sqlite3
import optparse

db_dir = "../db/"
db_power_name = db_dir + "power_consumption.db"
db_power_schema = """
create table if not exists power_consumption_data (
  id integer primary key autoincrement,
  date_time text,
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


def set_parser_options(parser):
    parser.add_option('-f', '--force', action="store_true", dest="force",
                      help="Overwrite any existing database", default=False)


def create_power_database(force=False):
    table_schema = ""
    if force:
        table_schema += "drop table if exists power_consumption_data;"
    table_schema += db_power_schema
    # Create database (connection)
    connection = sqlite3.connect(db_power_name)
    # Create
    cursor = connection.cursor()
    cursor.executescript(table_schema)
    # Close database
    cursor.close()
    connection.close()


def create_settings_database(force=False):
    table_schema = ""
    if force:
        table_schema += "drop table if exists settings;"
    table_schema += db_settings_schema
    # Create database (connection)
    connection = sqlite3.connect(db_settings_name)
    # Create
    cursor = connection.cursor()
    cursor.executescript(table_schema)
    # Close database
    cursor.close()
    connection.close()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    set_parser_options(parser)
    options, args = parser.parse_args()
    if not os.path.isdir(db_dir):
        os.makedirs(db_dir)
    if options.force:
        create_power_database(force=True)
        create_settings_database(force=True)
    else:
        create_power_database()
        create_settings_database()
