from collections import namedtuple
from ..view.login import login
from ..view.homeCaregiver import homeCaregiver
from ..view.homeDoctor import homeDoctor
from ..view.homePatient import homePatient

from ..model.caregiver import Caregiver
from ..model.doctor import Doctor
from ..model.healthFile import HealthFile
from ..model.patient import Patient


DoctorData = namedtuple('DoctorData', ['name', 'surname', 'cf'])
CaregiverData = namedtuple('CaregiverData', ['name', 'surname'])
PatientData = namedtuple('PatientData', ['name', 'surname', 'cf'])
HealthFileData = namedtuple('HealthData', ['name', 'surname', 'cf'])

#provider_url, contract_address, abi
provider_url = "http://ganache:8080"
contract_address="contractAddr"
abi="abiCode"
def main():
    doctorContracts=Doctor(provider_url,contract_address,abi)
    caregiverContracts = Caregiver(provider_url, contract_address, abi)
    patientContracts = Patient(provider_url, contract_address, abi)

    user = login(doctorContracts, caregiverContracts, patientContracts)

    if user['type']=='doctor':
        doctor = DoctorData(user['name'], user['surname'], user['cf'])
        homeDoctor(doctor)
    elif user['type']=='caregiver':
        caregiver = CaregiverData(user['name'], user['surname'])
        homeCaregiver(caregiver)
    elif user['type']=='patient':
        patient = PatientData(user['name'], user['surname'],user['cf'])
        homePatient(patient)



