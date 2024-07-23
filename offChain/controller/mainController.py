import json
import threading
import time
from collections import namedtuple


from view.login import login
from view.homeCaregiver import homeCaregiver
from view.homeDoctor import homeDoctor
from view.homePatient import homePatient

from model.caregiver import Caregiver
from model.doctor import Doctor
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

DoctorData = namedtuple('DoctorData', ['name', 'lastname','password','isRegistered','cf'])
CaregiverData = namedtuple('CaregiverData', ['name', 'lastname','password','isRegistered','cf'])

HealthFileData = namedtuple('HealthData', ['cf','clinicalHistory','prescriptions','treatmentPlan','notes'])

provider_url = "http://ganache:8080"




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

def main():

    doctorContracts = Doctor(provider_url)
    caregiverContracts = Caregiver(provider_url)
    patientContracts = Patient(provider_url)
    healthFileContracts = HealthFile(provider_url)
    event_listener_thread = threading.Thread(target=listen_to_events, args=(doctorContracts,caregiverContracts,patientContracts))
    event_listener_thread.start()

    user = login(doctorContracts, caregiverContracts, patientContracts, healthFileContracts)
    #come si fa con l'admin?????? ad accedere alla sua home dico
    if isinstance(user, DoctorData):
        homeDoctor(user,doctorContracts, healthFileContracts)
    elif isinstance(user, CaregiverData):
        homeCaregiver(user,caregiverContracts, healthFileContracts, patientContracts)
    elif isinstance(user, PatientData):
        homePatient(user,patientContracts, caregiverContracts, healthFileContracts)


def handle_event(event):
    file_path='onChain/address/addressList.json'
    data = load_addresses(file_path)
    cf = event['args']['cf']
    address = event['args']['addres']
    private_key = event['args']['private_key']
    type = event['args']['ctype']

    data[cf] = {
        "address": str(address),
        "private_key": private_key,
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



def save_addresses(file_path, addresses):
    with open(file_path, 'w') as file:
        json.dump(addresses, file, indent=4)