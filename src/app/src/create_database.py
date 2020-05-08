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
    parser.add_option('-f', '--force', action="store_true", dest="force",
                      help="Overwrite any existing database", default=False)


def create_power_database(force=False):
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


def create_settings_database(force=False):
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
