import PySimpleGUI as sg

def homeCaregiver(caregiver, caregiverContracts, healthFileContracts, patientContracts):
    sg.theme('DarkAmber')
    layout = [
        [sg.Text(f'Benvenuto {caregiver.name} {caregiver.lastname}')],
        [sg.Text('Inserire il codice fiscale del paziente:'), sg.InputText(key='cf'), sg.Button('Ok')],
        [ sg.Button('Esci'), sg.Button('Profilo')]
    ]

    windowHome = sg.Window('Home', layout)

    while True:
        event, values = windowHome.read()

        if event == sg.WINDOW_CLOSED or event == 'Esci':
            break
        elif event == 'Profilo':
            windowHome.Hide()
            caregiverProfile(caregiver,caregiverContracts, windowHome)
        elif event == 'Ok':
            cf = values['cf']
            healthFile = healthFileResearch(cf, healthFileContracts)
            if healthFile:
                windowHome.Hide()
                patient = patientResearch(cf, patientContracts)
                patientHealthFile(caregiver, patient, healthFile, windowHome,healthFileContracts)

    windowHome.close()

def patientHealthFile(caregiver, patient, healthFile, windowHome, healthFileContracts):
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
            healthFileContracts.confirm_treatment(caregiver.cf, healthFile.cf, patient.isIndependent)
            windowHealthFile['-OUTPUT-'].update('Cure confermate', text_color='green')
        elif event == 'Aggiungi nota':
            addNote(healthFile, patient, windowHealthFile, healthFileContracts)
        elif event == 'Home':
            break

    windowHealthFile.close()
    windowHome.UnHide()


def addNote(healthFile, patient, windowHealthFile, healthFileContracts):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Aggiungi Nota per {patient.name} {patient.lastname}')],
        [sg.Text('Nuova Nota:'), sg.InputText(key='nuova_nota')],
        [sg.Text('', size=(30, 1), key='-OUTPUT-')],
        [sg.Button('Aggiungi'), sg.Button('Annulla')]
    ]

    windowAddNote = sg.Window('Aggiungi Nota', layout)

    while True:
        event, values = windowAddNote.read()

        if event == sg.WINDOW_CLOSED or event == 'Annulla':
            break
        elif event == 'Aggiungi':
            newNote = values['nuova_nota']
            if newNote:
                healthFileContracts.update_healthFile(healthFile.cf, healthFile.clinicalHistory,
                                                      healthFile.prescriptions, healthFile.treatmentPlan,
                                                      healthFile.notes)
                windowHealthFile['notes'].update(newNote)

            else:
                windowAddNote['-OUTPUT-'].update('Modifiche non valide', text_color='red')

    windowAddNote.close()
    windowHealthFile.UnHide()

def checkValues(values):
    if values['name'] == '' or values['lastname'] == '':
        sg.popup_error('Uno dei campi è vuoto, inserire un input valido')
        return 0
    return 1

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
            if checkValues(values):
                caregiverContracts.update_caregiver(caregiver.cf, values['name'], values['lastname'])
                windowProfile['-OUTPUT-'].update('Modifiche registrate', text_color='green')
                caregiver.name = values['name']
                caregiver.lastname = values['lastname']
                windowHome['name'].update(caregiver.name)
                windowHome['lastname'].update(caregiver.lastname)
                break
            else:
                windowProfile['-OUTPUT-'].update('Modifiche non valide', text_color='red')
                windowProfile['name'].update(caregiver.name)
                windowProfile['lastname'].update(caregiver.lastname)
                windowProfile['cf'].update(caregiver.cf)
    windowProfile.close()
    windowHome.UnHide()


def healthFileResearch(cf,healthFileContracts):
    try:
        healthFile = healthFileContracts.get_healthFile(cf)
        if healthFile.cf:
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