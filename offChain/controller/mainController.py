import json
import threading
import time
import psutil
import logging
import mysql.connector
from collections import namedtuple

from view.login import login
from view.login import Admin
from view.homeCaregiver import homeCaregiver
from view.homeDoctor import homeDoctor
from view.homePatient import homePatient
from view.homeAdmin import homeAdmin

from model.caregiver import Caregiver
from model.caregiver import CaregiverData
from model.doctor import Doctor
from model.doctor import DoctorData
from model.healthFile import HealthFile
from model.patient import Patient
from model.patient import PatientData




provider_url = "http://ganache:8080"

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    filename='offChain/monitoring/softwareLog.log', filemode='a')

try:
    conn = mysql.connector.connect(
        host="host.docker.internal",  # IP o nome host del database
        port=3306,             # Porta del database (predefinita 3306 per MySQL)
        user="root",     # Username del database
        password="loris", # Password del database
        database="healthchain"  # Nome del database
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

except Exception as err:
    print('connessione al database fallita')

def main():
    try:
        doctorContracts = Doctor(provider_url, conn)
        caregiverContracts = Caregiver(provider_url, conn)
        patientContracts = Patient(provider_url, conn)
        healthFileContracts = HealthFile(provider_url, conn)
    except Exception as err:
        return -1

    event_listener_thread = threading.Thread(target=listen_to_events,
                                             args=(doctorContracts,caregiverContracts,patientContracts))
    event_listener_thread.start()

    sistem_monitoring = threading.Thread(target=monitor_system,
                                             args=())
    sistem_monitoring.start()
    flag = beginLogin(doctorContracts, caregiverContracts, patientContracts, healthFileContracts)
    return flag
def beginLogin(doctorContracts, caregiverContracts, patientContracts, healthFileContracts):
    while True:
        user = login(doctorContracts, caregiverContracts, patientContracts, healthFileContracts,fine)
        if isinstance(user, DoctorData):
            homeDoctor(user,doctorContracts, healthFileContracts)
        elif isinstance(user, CaregiverData):
            homeCaregiver(user,caregiverContracts, healthFileContracts, patientContracts)
        elif isinstance(user, PatientData):
            homePatient(user,patientContracts, caregiverContracts, healthFileContracts)
        elif isinstance(user, Admin):
            homeAdmin(user, doctorContracts, caregiverContracts)
        else:
            fine.set()
            break
    return 0

def listen_to_events(doctorContracts,caregiverContracts,patientContracts):
    filters = {
        '1': doctorContracts.contract.events.DoctorRegistered().create_filter(fromBlock='latest'),
        '2': patientContracts.contract.events.PatientRegistered().create_filter(fromBlock='latest'),
        '3': caregiverContracts.contract.events.CaregiverRegistered().create_filter(fromBlock='latest')
    }
    while True:
        for event_name, event_filter in filters.items():
            for event in event_filter.get_new_entries():
                handle_event(event)
        time.sleep(2)
        if fine.is_set():
            break

def handle_event(event):
    cf = event['args']['cf']
    address = event['args']['addres']
    private_key = event['args']['private_key']
    ctype = event['args']['ctype']

    query = "INSERT INTO users (cf, address, private_key, ctype) VALUES (%s, %s, %s, %s)"
    c.execute(query, (cf, address, private_key, ctype))
    conn.commit()




fine = threading.Event()


def monitor_system():
    file_path = 'offChain/monitoring/systemMonitoring.txt'
    with open(file_path, 'w') as file:
        while True:
            file.write(f"CPU usage: {psutil.cpu_percent()}%")
            file.write(f"Memory usage: {psutil.virtual_memory().percent}%")
            file.write(f"Disk usage: {psutil.disk_usage('/').percent}%")
            file.write(f"VRAM usage: 0,1%")
            file.write("Data e ora formattata:" + time.strftime("%d-%m-%Y %H:%M:%S", time.localtime()))
            file.write("\n")
            file.flush()
            time.sleep(10)
            if fine.is_set():
                break
