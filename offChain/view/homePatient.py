import PySimpleGUI as sg
import logging
import re

def homePatient(patient,patientContracts, caregiverContracts, healthFileContracts):
    logging.info('Autenticato il paziente: '+patient.lastname + ' ' + patient.name)
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Salve {patient.name} {patient.lastname}',key='Salve')]
    ]
    if not patient.isIndependent:
        layout.append([sg.Button('Visualizza cartella clinica'), sg.Button('Modifica profilo'), sg.Button('Logout')])
    else:
        layout.append([sg.Button('Visualizza cartella clinica'), sg.Button('Conferma cure'), sg.Button('Modifica profilo'), sg.Button('Logout')])

    windowHome = sg.Window('Home Paziente', layout)

    while True:
        event, values = windowHome.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Visualizza cartella clinica':
            healthFile = researchHealthFile(patient.cf, healthFileContracts)
            windowHome.Hide()
            viewHealthFile(healthFile, patient, windowHome)
        elif event == 'Modifica profilo':
            windowHome.Hide()
            modifyProfile(patient,patientContracts, windowHome)
        elif event == 'Conferma cure':
            viewConfirmTreatement(patient, caregiverContracts,healthFileContracts, windowHome)
        elif event == 'Logout':
            break
    windowHome.close()

def viewHealthFile(healthFile, patient, windowHome):
    logging.info('Fascicolo con codice: '+ healthFile.cf + ' aperto da: ' + patient.lastname +' '+patient.name)
    sg.theme('DarkAmber')

    layout = [

        [sg.Text(f'Codice fiscale: {healthFile.cf}')],
        [sg.Text('Prescrizioni:')],
        [sg.Text(healthFile.prescriptions, size=(30, 5))],
        [sg.Text('Note:')],
        [sg.Text(healthFile.notes, size=(30, 5))],
        [sg.Button('Chiudi')]
    ]

    windowHealthFile = sg.Window('Cartella Clinica', layout)

    while True:
        event, values = windowHealthFile.read()

        if event == sg.WINDOW_CLOSED or event == 'Chiudi':
            break

    windowHealthFile.close()
    windowHome.UnHide()

def modifyProfile(patient,patientContracts, windowHome):
    sg.theme('DarkAmber')
    layoutProfile = [[sg.Text('Nome'), sg.InputText(patient.name,key='name')],
                     [sg.Text('Cognome'), sg.InputText(patient.lastname,key='lastname')],
                     [sg.Text('Codice fiscale'), sg.Text(patient.cf, key='cf')],
                     [sg.Text('Luogo di nascita'), sg.InputText(patient.birthPlace, key='birthPlace')],
                     [sg.Text('Indipendente'), sg.InputText(patient.isIndependent, key='isIndependent')],#bottone
                     [sg.Text('Password'), sg.InputText(patient.password, key='password', password_char='*')],
                     [sg.Button('Salva'), sg.Button('Home')],
                     [sg.Text('', size=(30, 1), key='-OUTPUT-')]]
    windowProfile = sg.Window('Profile', layoutProfile)

    while True:
        event, values = windowProfile.read()  # SANIFICARE
        if event == sg.WIN_CLOSED:
            break
        if event == 'Home':
            break
        if event == 'Salva':

            values['name'] = sanitizeInput(values['name'])
            values['lastname'] = sanitizeInput(values['lastname'])
            values['birthPlace'] = sanitizeInput(values['birthPlace'])
            values['password'] = sanitizeInput(values['password'])
            values['isIndependent'] = sanitizeInput(values['isIndependent'])

            if checkValues(values):
                logging.info('Modificato il profilo del paziente: '+ patient.name + ' ' + patient.lastname)
                patientContracts.update_patient(values['name'], values['lastname'],values['birthPlace'],values['password'],bool(int(values['isIndependent'])),patient.cf)
                windowProfile['-OUTPUT-'].update('Modifiche registrate', text_color='green')
                patient.name = values['name']
                patient.lastname = values['lastname']
                patient.isIndependent = values['isIndependent']
                patient.birthPlace = values['birthPlace']
                windowHome['Salve'].update(f'Salve {patient.name} {patient.lastname}')
                break
            else:
                windowProfile['-OUTPUT-'].update('Modifiche non valide', text_color='red')
                windowProfile['name'].update(patient.name)
                windowProfile['lastname'].update(patient.lastname)
                windowProfile['birthPlace'].update(patient.birthPlace)
                windowProfile['isIndependent'].update(patient.isIndependent)
                windowProfile['password'].update(patient.password)
                windowProfile['cf'].update(patient.cf)
    windowProfile.close()
    windowHome.UnHide()
def researchHealthFile(cf, healthFileContracts):
    try:
        healthFile = healthFileContracts.get_healthFile(cf)
        if healthFile:
            return healthFile
    except ValueError as e:
        return None
    return None

def checkValues(values):
    for key, value in values.items():
        if not value:
            sg.popup_error(f'Il campo "{key}" non è valido')
            return False
    return True



def viewConfirmTreatement(patient,caregiverContracts, healthFileContracts, windowHome):
    sg.theme('DarkAmber')
    layout=[[sg.Text('Inserire codice fiscale del caregiver: '),sg.InputText('', key='cfCaregiver')],
            [sg.Text('', size=(30, 1), key='-OUTPUT-')],
            [sg.Button('Indietro'), sg.Button('Conferma')]]
    windowConfirmTreatement = sg.Window('Conferma cure', layout)

    while True:
        event, values = windowConfirmTreatement.read()

        if event == sg.WINDOW_CLOSED or event == 'Indietro':
            break
        elif event == 'Conferma':
            values['cfCaregiver'] = sanitizeInput(values['cfCaregiver'])
            if checkCaregiver(values['cfCaregiver'], caregiverContracts):
                logging.info('Cure per: ' + patient.lastname + ' ' + patient.name + ' confermate dal paziente')
                healthFileContracts.confirm_treatment( values['cfCaregiver'],patient.cf , patient.isIndependent)
                break
            else:
                windowConfirmTreatement['-OUTPUT-'].update('Codice non valido', text_color='red')
                windowConfirmTreatement['cfCaregiver'].update('')

    windowConfirmTreatement.close()
    windowHome.UnHide()


def checkCaregiver(cf, caregiverContracts):
    try:
        caregiver = caregiverContracts.get_caregiver(cf)
        if caregiver:
            return 1
    except ValueError as e:
        return None
    return None



def sanitizeInput(value):

    sanitizedValue = re.sub(r'\b(import|exec|eval)\b', '', value, flags=re.IGNORECASE)

    if re.search(r'[^a-zA-Z0-9\s]', sanitizedValue):
        return False

    return sanitizedValue
