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


private_key = "0xd4485a65c4f843d9d1169d6ccca7caf2cf22b6fb3f5a1b0c5ba008e688aaf725"
def main():

    doctorContracts = Doctor(provider_url)
    caregiverContracts = Caregiver(provider_url)
    patientContracts = Patient(provider_url)
    healthFileContracts = HealthFile(provider_url)

    user = login(doctorContracts, caregiverContracts, patientContracts, healthFileContracts, private_key)

    if isinstance(user, DoctorData):
        homeDoctor(user,doctorContracts, healthFileContracts, private_key)
    elif isinstance(user, CaregiverData):
        homeCaregiver(user,caregiverContracts, healthFileContracts, patientContracts, private_key)
    elif isinstance(user, PatientData):
        homePatient(user,patientContracts, caregiverContracts, healthFileContracts,private_key)





