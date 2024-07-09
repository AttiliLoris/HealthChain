from collections import namedtuple
from ..view.login import login
from ..view.homeCaregiver import homeCaregiver
Doctor = namedtuple('Doctor', ['name', 'surname', 'cf'])
Caregiver = namedtuple('Caregiver', ['name', 'surname'])
Patient = namedtuple('Patient', ['name', 'surname', 'cf'])
HealthFile = namedtuple('HealthFile', ['name', 'surname', 'cf'])

def main():
    user = login()
    if isinstance(user, Doctor):
        pass
    elif isinstance(user, Caregiver):
        homeCaregiver(user)
    elif isinstance(user, Patient):
        pass


