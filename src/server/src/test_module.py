import unittest
import create_database
from paho_sub import Subscriber
import os


class TestCreateDatabase(unittest.TestCase):
    """ Clase para testear create_database """

    def test_create_database(self):
        """ Testeo de la creación de la base de datos """
        print(self._testMethodName)
        create_database.check_dir()
        self.assertTrue(os.path.isdir("../db/"), "Directory creation failed")
        create_database.create_power_database()
        self.assertTrue(os.path.isfile("../db/power_consumption.db"),
                        "Database not created")
        os.remove("../db/power_consumption.db")
        os.rmdir("../db/")


class TestPahoSubscriber(unittest.TestCase):
    """ Clase para testear paho_sub """

    def test_connection(self):
        print(self._testMethodName)
        with self.assertRaises(ConnectionRefusedError):
            self.suscriber = Subscriber()


if __name__ == '__main__':
    unittest.main()
