import re

import PySimpleGUI as sg
import logging




def homeCaregiver(caregiver, caregiverContracts, healthFileContracts, patientContracts):
    logging.info('Autenticato il caregiver: ' + caregiver.lastname + ' ' + caregiver.name)
    sg.theme('DarkAmber')
    layout = [
        [sg.Text(f'Benvenuto {caregiver.name} {caregiver.lastname}', key='benvenuto')],
        [sg.Text('Inserire il codice fiscale del paziente:'), sg.InputText(key='cf'), sg.Button('Ok')],
        [sg.Text('', size=(30, 1), key='-OUTPUT-')],
        [ sg.Button('Esci'), sg.Button('Profilo')]
    ]

    windowHome = sg.Window('Home', layout)

    while True:
        event, values = windowHome.read()

        if event == sg.WINDOW_CLOSED or event == 'Esci':
            break
        elif event == 'Profilo':
            windowHome['-OUTPUT-'].update('')
            windowHome.Hide()
            caregiverProfile(caregiver,caregiverContracts, windowHome)
        elif event == 'Ok':
            cf = values['cf']
            if checkCf(cf):
                healthFile = healthFileResearch(cf, healthFileContracts)
                if healthFile:
                    windowHome['-OUTPUT-'].update('Caricando il fascicolo...', text_color='green')
                    windowHome.Hide()
                    patient = patientResearch(cf, patientContracts)
                    patientHealthFile(caregiver, patient, healthFile, windowHome,healthFileContracts)
            else:
                windowHome['-OUTPUT-'].update('codice fiscale non valido', text_color='red')

    windowHome.close()

def patientHealthFile(caregiver, patient, healthFile, windowHome, healthFileContracts):
    logging.info('Fascicolo del paziente: ' + patient.lastname + ' ' + patient.name + 'aperto dal caregiver: ' +
                 caregiver.lastname + ' ' + caregiver.name)
    sg.theme('DarkAmber')
    layout = [
        [sg.Text(f'Cartella di {patient.name} {patient.lastname}')],
        [sg.Text(f'Nome: {patient.name}')],
        [sg.Text(f'Cognome: {patient.lastname}')],
        [sg.Text(f'Codice fiscale: {healthFile.cf}')],
        [sg.Text(f'Prescrizioni:{healthFile.prescriptions}')],
        [sg.Text(f'Note: {healthFile.notes}', key='notes')],
        [sg.Text('', size=(30, 1), key='-OUTPUT-')]]
    if not patient.isIndependent:
        layout.append([sg.Button('Aggiungi nota'), sg.Button('Conferma cure'), sg.Button('Home')])
    else:
        layout.append([sg.Button('Aggiungi nota'), sg.Button('Home')])


    windowHealthFile = sg.Window('Cartella Paziente', layout)

    while True:
        event, values = windowHealthFile.read()

        if event == sg.WINDOW_CLOSED or event == 'Chiudi':
            break
        elif event == 'Conferma cure':
            logging.info('Cure per: ' + patient.lastname + ' ' + patient.name +
                         ' confermate dal caregiver: '+caregiver.lastname +' '+caregiver.name)
            healthFileContracts.confirm_treatment(caregiver.cf, healthFile.cf, patient.isIndependent)
            windowHealthFile['-OUTPUT-'].update('Cure confermate', text_color='green')
        elif event == 'Aggiungi nota':
            addNote(healthFile, patient, caregiver, windowHealthFile, healthFileContracts)
        elif event == 'Home':
            windowHome['-OUTPUT-'].update('')
            windowHome['cf'].update('')
            break

    windowHealthFile.close()
    windowHome.UnHide()


def addNote(healthFile, patient, caregiver, windowHealthFile, healthFileContracts):
    logging.info('Aggiunta nota al fascicolo del paziente: '+patient.lastname + ' ' +patient.name + 'da parte del caregiver: '
                 +caregiver.lastname + ' '+caregiver.name)
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Aggiungi Nota per {patient.name} {patient.lastname}')],
        [sg.Text('Nuova Nota:'), sg.InputText(healthFile.notes,key='nuova_nota')],
        [sg.Text('', size=(30, 1), key='-OUTPUT-')],
        [sg.Button('Aggiungi'), sg.Button('Annulla')]
    ]

    windowAddNote = sg.Window('Aggiungi Nota', layout)

    while True:
        event, values = windowAddNote.read()

        if event == sg.WINDOW_CLOSED or event == 'Annulla':
            break
        elif event == 'Aggiungi':
            values['nuova_nota'] = sanitizeInput(values['nuova_nota'])
            if checkValues(values):
                healthFile.notes = values['nuova_nota']
                healthFileContracts.update_healthFile(healthFile.cf, healthFile.clinicalHistory,
                                                      healthFile.prescriptions, healthFile.treatmentPlan,
                                                      healthFile.notes)
                windowHealthFile['notes'].update('Note: '+ healthFile.notes)
                break

            else:
                windowAddNote['-OUTPUT-'].update('Modifiche non valide', text_color='red')

    windowAddNote.close()
    windowHealthFile.UnHide()


def caregiverProfile(caregiver, caregiverContracts, windowHome):
    layoutProfile = [[sg.Text('Nome'), sg.InputText(caregiver.name, key='name')],
                     [sg.Text('Cognome'), sg.InputText(caregiver.lastname, key='lastname')],
                     [sg.Text('Codice fiscale'), sg.Text(caregiver.cf, key='cf')],
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
            if checkValues(values):
                logging.info('Profilo del caregiver: '+caregiver.lastname + ' '+ caregiver.name + ' modificato')
                caregiverContracts.update_caregiver(caregiver.cf, values['name'], values['lastname'])
                windowProfile['-OUTPUT-'].update('Modifiche registrate', text_color='green')
                caregiver.name = values['name']
                caregiver.lastname = values['lastname']
                windowHome['benvenuto'].update(f'Benvenuto {caregiver.name} {caregiver.lastname}')

                break
            else:
                windowProfile['-OUTPUT-'].update('Modifiche non valide', text_color='red')
                windowProfile['name'].update(caregiver.name)
                windowProfile['lastname'].update(caregiver.lastname)
                windowProfile['cf'].update(caregiver.cf)
    windowProfile.close()
    windowHome.UnHide()


def healthFileResearch(cf,healthFileContracts):
    healthFile = False
    try:
        healthFile = healthFileContracts.get_healthFile(cf)
        if healthFile:
            return healthFile
    except ValueError as e:
        return None
    return None


def patientResearch(cf, patientContracts):
    try:
        patient = patientContracts.get_patient(cf)
        if patient.cf:
            return patient
    except ValueError as e:
        return None
    return None

def sanitizeInput(value):

    sanitizedValue = re.sub(r'\b(import|exec|eval)\b', '', value, flags=re.IGNORECASE)

    if re.search(r'[^a-zA-Z0-9\s]', sanitizedValue):
        return ''

    return sanitizedValue

def checkValues(values):
    for key, value in values.items():
        if not value:
            sg.popup_error(f'Il campo "{key}" non è valido')
            return False
    return True


def checkCf(cf):
    if re.match(r'^[a-zA-Z0-9]{16}$', cf):
        return True
    else:
        return False