import PySimpleGUI as sg

def homeCaregiver(caregiver, caregiverContracts, healthFileContracts, patientContracts, private_key):
    sg.theme('DarkAmber')
    layout = [
        [sg.Text(f'Benvenuto {caregiver.name} {caregiver.surname}')],
        [sg.Text('Inserire il codice fiscale del paziente:'), sg.InputText(key='cf'), sg.Button('Ok')],
        [ sg.Button('Indietro'), sg.Button('Profilo')]
    ]

    windowHome = sg.Window('Home', layout)

    while True:
        event, values = windowHome.read()

        if event == sg.WINDOW_CLOSED or event == 'Indietro':
            break
        elif event == 'Profilo':
            windowHome.Hide()
            caregiverProfile(caregiver,caregiverContracts, windowHome, private_key)
        elif event == 'Ok':
            cf = values['cf']
            healthFile = healthFileResearch(cf, healthFileContracts)
            if healthFile:
                windowHome.Hide()
                patientHealthFile(caregiver, healthFile, windowHome,healthFileContracts, patientContracts,private_key)
            break

    windowHome.close()

def patientHealthFile(caregiver, healthFile, windowHome, healthFileContracts, patientContracts, private_key):
    sg.theme('DarkAmber')
    patient= patientContracts.getPatient(healthFile.cf)
    layout = [
        [sg.Text(f'Cartella di {healthFile.name} {healthFile.surname}')],
        [sg.Text(f'Nome: {healthFile.name}')],
        [sg.Text(f'Cognome: {healthFile.surname}')],
        [sg.Text(f'Codice fiscale: {healthFile.cf}')],
        [sg.Text(f'Prescrizioni:{healthFile.prescriptions}')],
        [sg.Text(f'Note: {healthFile.notes}')]]
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
            healthFileContracts.confirm_treatment(caregiver.cf, healthFile.cf, patient.isIndependent, private_key)
        elif event == 'Aggiungi nota':
            addNote(healthFile, windowHealthFile, healthFileContracts,private_key)
        elif event == 'Home':
            windowHome.UnHide()
            break

    windowHealthFile.close()

def addNote(healthFile, windowHealthFile, healthFileContracts,private_key):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Aggiungi Nota per {healthFile.name} {healthFile.surname}')], #amo healthFile non ha name e surname ha solo cf
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
                conferma = sg.popup_ok_cancel(f'Confermi di voler aggiungere la nota?')
                if conferma == 'OK':
                    windowAddNote['-OUTPUT-'].update('')
                    healthFile.notes=healthFile.notes +'\n'+ newNote
                    healthFileContracts.update_healthFile(healthFile.cf, private_key, healthFile.notes)
                    sg.popup(f'Nota aggiunta.')
                    break
            else:
                windowAddNote['-OUTPUT-'].update('Modifiche non valide', text_color='red')

    windowAddNote.close()
    windowHealthFile.UnHide()

def checkValues(values):
    if values['name'] == '' or values['surname'] == '':
        sg.popup_error('Uno dei campi è vuoto, inserire un input valido')
        return 0
    return 1

def caregiverProfile(caregiver, caregiverContracts, windowHome, private_key):
    layoutProfile = [[sg.Text('Nome'), sg.InputText(caregiver.name, key='name')],
                     [sg.Text('Cognome'), sg.InputText(caregiver.surname, key='surname')],
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
                caregiverContracts.update_caregiver(caregiver.cf, private_key, values['name'], values['surname'])
                windowProfile['-OUTPUT-'].update('Modifiche registrate', text_color='green')
                caregiver.name = values['name']
                caregiver.surname = values['surname']

            else:
                windowProfile['-OUTPUT-'].update('Modifiche non valide', text_color='red')
                windowProfile['name'].update(caregiver.name)
                windowProfile['surname'].update(caregiver.surname)
                windowProfile['cf'].update(caregiver.cf)
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

