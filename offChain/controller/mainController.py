from collections import namedtuple

from view.login import login
from view.homeCaregiver import homeCaregiver
from view.homeDoctor import homeDoctor
from view.homePatient import homePatient

from model.caregiver import Caregiver
from model.doctor import Doctor
from model.healthFile import HealthFile
from model.patient import Patient


DoctorData = namedtuple('DoctorData', ['name', 'lastName','password','isRegistered','cf'])
CaregiverData = namedtuple('CaregiverData', ['name', 'lastName','password','isRegistered','cf'])
PatientData = namedtuple('PatientData', ['name', 'lastName', 'birthPlace','password','isRegistered','isIndependent','cf'])
HealthFileData = namedtuple('HealthData', ['cf','clinicalHistory','prescriptions','treatmentPlan','notes'])

#provider_url, contract_address, abi
provider_url = "http://ganache:8080"
contract_address = "contractAddr"


private_key = "privateKey"
def main():

    doctorContracts = Doctor(provider_url)
    caregiverContracts = Caregiver(provider_url)
    patientContracts = Patient(provider_url)
    healthFileContracts = HealthFile(provider_url)

    user = login(doctorContracts, caregiverContracts, patientContracts, healthFileContracts)

    if isinstance(user, DoctorData):
        homeDoctor(user,doctorContracts, healthFileContracts, private_key)
    elif isinstance(user, CaregiverData):
        homeCaregiver(user,caregiverContracts, healthFileContracts, patientContracts, private_key)
    elif isinstance(user, PatientData):
        homePatient(user,patientContracts, caregiverContracts, healthFileContracts,private_key)





