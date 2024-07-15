from collections import namedtuple

from view.login import login
from view.homeCaregiver import homeCaregiver
from view.homeDoctor import homeDoctor
from view.homePatient import homePatient

from model.caregiver import Caregiver
from model.doctor import Doctor
from model.healthFile import HealthFile
from model.patient import Patient


DoctorData = namedtuple('DoctorData', ['name', 'surname', 'cf'])
CaregiverData = namedtuple('CaregiverData', ['name', 'surname'])
PatientData = namedtuple('PatientData', ['name', 'surname', 'cf'])
HealthFileData = namedtuple('HealthData', ['name', 'surname', 'cf'])

#provider_url, contract_address, abi
provider_url = "http://ganache:8080"
contract_address = "contractAddr"
abiD = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"indexed": true,
				"internalType": "string",
				"name": "ctype",
				"type": "string"
			}
		],
		"name": "DoctorRegistered",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"indexed": true,
				"internalType": "string",
				"name": "ctype",
				"type": "string"
			}
		],
		"name": "DoctorUpdated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "authorizedEditors",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "doctors",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "hashedPwd",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "isRegistered",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"name": "getDoctor",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_cf",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "password",
				"type": "string"
			}
		],
		"name": "registerDoctor",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"name": "updateDoctor",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "password",
				"type": "string"
			}
		],
		"name": "verifyPassword",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

abiC = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"indexed": true,
				"internalType": "string",
				"name": "ctype",
				"type": "string"
			}
		],
		"name": "CaregiverRegistered",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"indexed": true,
				"internalType": "string",
				"name": "ctype",
				"type": "string"
			}
		],
		"name": "CaregiverUpdated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "authorizedEditors",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "caregivers",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "hashedPwd",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "isRegistered",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"name": "getCaregiver",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_cf",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "password",
				"type": "string"
			}
		],
		"name": "registerCaregiver",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"name": "updateCaregiver",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "password",
				"type": "string"
			}
		],
		"name": "verifyPassword",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
abiH = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "string",
				"name": "cfCaregiver",
				"type": "string"
			},
			{
				"indexed": true,
				"internalType": "string",
				"name": "cfPatient",
				"type": "string"
			}
		],
		"name": "ConfirmTreatment",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"name": "HealthFileUpdated",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"name": "NewHealthFile",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "cfCaregiver",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "cfPatient",
				"type": "string"
			}
		],
		"name": "confirmTreatment",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "clinicalHistory",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "prescriptions",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "treatmentPlan",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "note",
				"type": "string"
			}
		],
		"name": "createHealthFile",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"name": "getHealthFile",
		"outputs": [
			{
				"internalType": "string",
				"name": "clinicalHistory",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "prescriptions",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "treatmentPlan",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "note",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "healthFiles",
		"outputs": [
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "clinicalHistory",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "prescriptions",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "treatmentPlan",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "note",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "clinicalHistory",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "prescriptions",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "treatmentPlan",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "note",
				"type": "string"
			}
		],
		"name": "updateHealthFile",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
abiP = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"indexed": true,
				"internalType": "string",
				"name": "ctype",
				"type": "string"
			}
		],
		"name": "PatientRegistered",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"indexed": true,
				"internalType": "string",
				"name": "ctype",
				"type": "string"
			}
		],
		"name": "PatientUpdated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "authorizedEditors",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"name": "getPatient",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "birthPlace",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "isIndependent",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "_cf",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "patients",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "birthPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "hashedPwd",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "isRegistered",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "isIndependent",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "birthPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "isIndependent",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "password",
				"type": "string"
			}
		],
		"name": "registerPatient",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "lastName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "birthPlace",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			}
		],
		"name": "updatePatient",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "cf",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "password",
				"type": "string"
			}
		],
		"name": "verifyPassword",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

private_key = "privateKey"
def main():

    doctorContracts = Doctor(provider_url,contract_address,abiD)
    caregiverContracts = Caregiver(provider_url, contract_address, abiC)
    patientContracts = Patient(provider_url, contract_address, abiP)
    healthFileContracts = HealthFile(provider_url, contract_address, abiH)

    user = login(doctorContracts, caregiverContracts, patientContracts, healthFileContracts)

    if isinstance(user, DoctorData):
        homeDoctor(user,doctorContracts, healthFileContracts, private_key)
    elif isinstance(user, CaregiverData):
        homeCaregiver(user,caregiverContracts, healthFileContracts, patientContracts, private_key)
    elif isinstance(user, PatientData):
        homePatient(user,patientContracts, caregiverContracts,healthFileContracts,private_key)





