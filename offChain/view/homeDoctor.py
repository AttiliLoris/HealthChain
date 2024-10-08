import re

import PySimpleGUI as sg
import logging
def homeDoctor(doctor,doctorContracts,healthFileContracts):
    logging.info('Autenticato il dottore: ' + doctor.lastname + ' ' + doctor.name)
    sg.theme('DarkAmber')
    layoutHome = [[sg.Text('Inserire il codice fiscale di un paziente per vedere il suo fascicolo'), sg.InputText(key='cf')],
                [sg.Button('Ok'), sg.Button('Profilo'), sg.Button('Esci')],
                  [sg.Text('', size=(30, 1), key='-OUTPUT-')] ]


    windowHome = sg.Window('Home', layoutHome)

    while True:
        event, values = windowHome.read() #SANIFICARE
        cf=values['cf']
        if event == sg.WIN_CLOSED or event == 'Esci':
            break
        if event == 'Profilo':
            windowHome['-OUTPUT-'].update('')
            windowHome.Hide()
            doctorProfile(doctor, windowHome,doctorContracts)
        if event == 'Ok':
            healthFile = healthFileResearch(cf,healthFileContracts)
            if healthFile:
                windowHome['-OUTPUT-'].update('')
                windowHome.Hide()
                logging.info('Fascicolo con codice: ' + healthFile.cf +
                             ' aperto dal dottore: ' + doctor.lastname + ' ' + doctor.name + ' con codice fiscale: '
                             + doctor.cf)
                patientHealthFile(healthFile, windowHome, healthFileContracts)

            else:

                windowHome['-OUTPUT-'].update('Cartella non trovata', text_color='red')
                windowHome['cf'].update('')

    windowHome.close()

def doctorProfile(doctor, windowHome,doctorContracts):
    layoutProfile = [[sg.Text('Nome'), sg.InputText(doctor.name,key='name')],
                    [sg.Text('Cognome'), sg.InputText(doctor.lastname,key='lastname')],
                    [sg.Text('Codice fiscale'), sg.Text(doctor.cf,key='cf')],
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
                logging.info('Profilo del dottore: '+doctor.lastname+ ' ' + doctor.name + ' modificato')
                doctorContracts.update_doctor(doctor.cf,values['name'],values['lastname'])
                windowProfile['-OUTPUT-'].update('Modifiche registrate', text_color='green')
                doctor.name = values['name']
                doctor.lastname = values['lastname']

                windowProfile['name'].update(doctor.name)
                windowProfile['lastname'].update(doctor.lastname)
                break

            else:
                windowProfile['-OUTPUT-'].update('Modifiche non valide', text_color='red')
                windowProfile['name'].update(doctor.name)
                windowProfile['lastname'].update(doctor.lastname)
                windowProfile['cf'].update(doctor.cf)
    windowProfile.close()
    windowHome.UnHide()

def healthFileResearch(cf,healthFileContracts):
    try:
        healthFile = healthFileContracts.get_healthFile(cf)
        if healthFile:
            return healthFile
    except ValueError as e:
        return None
    return None


def patientHealthFile(healthFile, windowHome, healthFileContracts):
    layoutHealthFile = [[sg.Text('Codice fiscale: '+ healthFile.cf)],
                        [sg.Text('Storia clinica: '), sg.Text(healthFile.clinicalHistory, key='Storia clinica')],
                        [sg.Text('Prescrizioni: '), sg.Text(healthFile.prescriptions, key='Prescrizioni')],
                        [sg.Text('Trattamenti: '), sg.Text(healthFile.treatmentPlan, key='Trattamenti')],
                        [sg.Button('Home'), sg.Button('Aggiorna storia clinica'), sg.Button('Modifica prescrizioni'), sg.Button('Aggiungi trattamento')]]

    windowHealthFile = sg.Window('Fascicolo', layoutHealthFile)

    while True:
        event, values = windowHealthFile.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Aggiorna storia clinica':
            windowHealthFile.Hide()
            modififyClinicalHistory(healthFile, windowHealthFile,healthFileContracts)
        if event == 'Modifica prescrizioni':
            windowHealthFile.Hide()
            modifyPrescriptions(healthFile, windowHealthFile, healthFileContracts)
        if event == 'Home':
            windowHome.UnHide()
            break
        if event == 'Aggiungi trattamento':
            windowHealthFile.hide()
            addTreatmentPlan(healthFile, windowHealthFile,healthFileContracts)
    windowHealthFile.close()


def modififyClinicalHistory(healthFile, windowHealthFile, healthFileContracts):
    layoutClinicalHistory = [[sg.Text('Storia clinica: '), sg.InputText(healthFile.clinicalHistory,key='clinicalHistory')],
                            [sg.Button('Conferma'), sg.Button('Indietro')]]
    windowClinicalHistory = sg.Window('Dettaglio', layoutClinicalHistory)
    while True:
        event, values = windowClinicalHistory.read()
        values['clinicalHistory'] = sanitizeInput(values['clinicalHistory'])
        if event == sg.WIN_CLOSED:
            break
        if event == 'Conferma':
            if not checkValues(values):
                windowClinicalHistory['clinicalHistory'].update(healthFile.clinicalHistory)
            else:
                healthFile.clinicalHistory = values['clinicalHistory']
                healthFileContracts.update_healthFile(healthFile.cf,healthFile.clinicalHistory,healthFile.prescriptions,healthFile.treatmentPlan,healthFile.notes)
                windowHealthFile['Storia clinica'].update(healthFile.clinicalHistory)
                break
        if event == 'Indietro':
            break
    windowClinicalHistory.close()
    windowHealthFile.UnHide()
def modifyPrescriptions(healthFile, windowHealthFile, healthFileContracts):
    layoutPrescription = [[sg.Text('Prescrizioni: '), sg.InputText(healthFile.prescriptions, key='prescriptions')],
                           [sg.Button('Conferma'), sg.Button('Indietro')]]
    windowPrescription = sg.Window('Dettaglio', layoutPrescription)

    while True:
        event, values = windowPrescription.read()
        values['prescriptions'] = sanitizeInput(values['prescriptions'])
        if event == sg.WIN_CLOSED:
            break
        if event == 'Conferma':
            if not checkValues(values): #in realtà potrebbe andare bene se è vuoto
                windowPrescription['prescriptions'].update(healthFile.prescriptions)
            else:
                healthFile.prescriptions = values['prescriptions']
                healthFileContracts.update_healthFile(healthFile.cf,healthFile.clinicalHistory,healthFile.prescriptions,healthFile.treatmentPlan,healthFile.notes)
                windowHealthFile['Prescrizioni'].update(healthFile.prescriptions)
                break
        if event == 'Indietro':
            break
    windowPrescription.close()
    windowHealthFile.UnHide()


def addTreatmentPlan(healthFile, windowHealthFile, healthFileContracts):
    sg.theme('DarkAmber')

    layoutTreatmentPlan= [[sg.Text('Trattamenti: '), sg.InputText(healthFile.treatmentPlan, key='treatmentPlan')],
                          [sg.Button('Conferma'), sg.Button('Indietro')]]
    windowTreatmentPlan = sg.Window('Piano di trattamenti', layoutTreatmentPlan)

    while True:
        event, values = windowTreatmentPlan.read()

        if event == sg.WINDOW_CLOSED or event == 'Indietro':
            break
        elif event == 'Conferma':
            values['treatmentPlan'] = sanitizeInput(values['treatmentPlan'])
            if checkValues(values):
                healthFile.treatmentPlan = values['treatmentPlan']
                healthFileContracts.update_healthFile(healthFile.cf, healthFile.clinicalHistory,
                                                      healthFile.prescriptions, healthFile.treatmentPlan,
                                                      healthFile.notes)
                windowHealthFile['Trattamenti'].update(healthFile.treatmentPlan)
                break
            else:
                windowTreatmentPlan['treatmentPlan'].update(healthFile.treatmentPlan)

    windowTreatmentPlan.close()
    windowHealthFile.UnHide()

def checkValues(values):
    for key, value in values.items():
        if not value:
            sg.popup_error(f'Il campo "{key}" non è valido')
            return False
    return True

def sanitizeInput(value):

    sanitizedValue = re.sub(r'\b(import|exec|eval)\b', '', value, flags=re.IGNORECASE)

    if re.search(r'[^a-zA-Z0-9\s]', sanitizedValue):
        return ''

    return sanitizedValue
