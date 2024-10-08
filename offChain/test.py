import os
import unittest
from faker import Faker
from model.model import Model
import mysql.connector
class testClass (unittest.TestCase):

    def setUp(self):
        """Setup for test."""
        self.faker = Faker()
        self.service = "http://127.0.0.1:8080"
        self.dbConn, self.cursor = self.dbConnect()

    def tearDown(self):
        """Cleaning after test."""
        pass

    def dbConnect(self):
        conn = mysql.connector.connect(
            host="127.0.0.1",  # IP o nome host del database
            port=3306,  # Porta del database (predefinita 3306 per MySQL)
            user="root",  # Username del database
            password="loris",  # Password del database
            database="healthchain"
        )

        c = conn.cursor()
        c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    cf VARCHAR(16) UNIQUE NOT NULL,
                    address VARCHAR(100) UNIQUE NOT NULL,
                    private_key VARCHAR(100) UNIQUE NOT NULL,
                    ctype VARCHAR(100) NOT NULL
                )
            ''')
        return conn, c

    def test_contract_deploy(self):
        for name in ['patient', 'caregiver', 'doctor','healthfile']:
            with self.subTest(name=name):
                self.Model(name)

    def Model(self,contract_name):
        os.chdir(r"C:\Users\loris\PycharmProjects\HealthChain")
        testModel = Model(self.service,contract_name, self.dbConn, solc_version='0.8.0')
        print("testing deploy of contract "+contract_name+"...")
        self.assertIsNotNone(testModel.contract, f"Deploy for contract {contract_name} failed")
        print("OK")


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase())