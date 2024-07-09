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
private_key="privateKey"
def main():
    doctorContracts=Doctor(provider_url,contract_address,abi)
    caregiverContracts = Caregiver(provider_url, contract_address, abi)
    patientContracts = Patient(provider_url, contract_address, abi)
    healthFileContracts = HealthFile(provider_url, contract_address, abi)

    user = login(doctorContracts, caregiverContracts, patientContracts)

    if isinstance(user, DoctorData):
        homeDoctor(user,doctorContracts, healthFileContracts, private_key)
    elif isinstance(user, CaregiverData):
        homeCaregiver(user,caregiverContracts, healthFileContracts, private_key)
    elif isinstance(user, PatientData):
        homePatient(user,patientContracts, healthFileContracts,private_key)



