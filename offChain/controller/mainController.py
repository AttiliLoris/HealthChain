import json
import threading
import time
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



'''from offChain.model.caregiver import Caregiver
from offChain.model.doctor import Doctor
from offChain.model.healthFile import HealthFile
from offChain.model.patient import Patient
from offChain.view.homeCaregiver import homeCaregiver
from offChain.view.homeDoctor import homeDoctor
from offChain.view.homePatient import homePatient
from offChain.view.login import login'''


provider_url = "http://ganache:8080"

#fare un evento che fa bloccare tuttp quando c'è esci o etc nfnnf

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

def main():

    doctorContracts = Doctor(provider_url)
    caregiverContracts = Caregiver(provider_url)
    patientContracts = Patient(provider_url)
    healthFileContracts = HealthFile(provider_url)
    event_listener_thread = threading.Thread(target=listen_to_events, args=(doctorContracts,caregiverContracts,patientContracts))
    event_listener_thread.start()

    while True:
        user = login(doctorContracts, caregiverContracts, patientContracts, healthFileContracts)
        if isinstance(user, DoctorData):
            homeDoctor(user,doctorContracts, healthFileContracts)
        elif isinstance(user, CaregiverData):
            homeCaregiver(user,caregiverContracts, healthFileContracts, patientContracts)
        elif isinstance(user, PatientData):
            homePatient(user,patientContracts, caregiverContracts, healthFileContracts)
        elif isinstance(user, Admin):
            homeAdmin(user, doctorContracts, caregiverContracts)



def handle_event(event):
    file_path='onChain/address/addressList.json'
    data = load_addresses(file_path)
    cf = event['args']['cf']
    address = event['args']['addres']
    private_key = event['args']['private_key']
    type = event['args']['ctype']

    data[cf] = {
        "address": str(address),
        "private_key": str(private_key),
        "type": type
    }
    save_addresses(file_path, data)

def load_addresses(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


fine = threading.Event()

def save_addresses(file_path, addresses):
    with open(file_path, 'w') as file:
        json.dump(addresses, file, indent=4)