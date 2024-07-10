import PySimpleGUI as sg
def homePatient(patient, patientContracts, healthFileContracts, private_key):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Benvenuto {patient.name} {patient.surname}')],
        [sg.Button('Visualizza cartella clinica'), sg.Button('Modifica profilo')]
    ]

    windowHome = sg.Window('Home Paziente', layout)

    while True:
        event, values = windowHome.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Visualizza cartella clinica':
            healthFile = researchHealthFile(patient.cf, healthFileContracts)
            windowHome.Hide()
            viewHealthFile(healthFile, windowHome)
        elif event == 'Modifica profilo':
            windowHome.Hide()
            modifyProfile(patient,patientContracts, windowHome, private_key)

    windowHome.close()

def viewHealthFile(healthFile, windowHome):
    sg.theme('DarkAmber')
    layout = [
        [sg.Text(f'Cartella di {healthFile.name} {healthFile.surname}')],
        [sg.Text(f'Nome: {healthFile.name}')],
        [sg.Text(f'Cognome: {healthFile.surname}')],
        [sg.Text(f'Codice fiscale: {healthFile.cf}')],
        [sg.Text('Prescrizioni:')],
        [sg.Listbox(values=healthFile.prescriptions, size=(30, 5))],
        [sg.Text('Note:')],
        [sg.Listbox(values=healthFile.notes, size=(30, 5))],
        [sg.Button('Chiudi')]
    ]

    windowHealthFile = sg.Window('Cartella Clinica', layout)

    while True:
        event, values = windowHealthFile.read()

        if event == sg.WINDOW_CLOSED or event == 'Chiudi':
            break

    windowHealthFile.close()
    windowHome.UnHide()

def modifyProfile(patient,patientContracts, windowHome, private_key):
    sg.theme('DarkAmber')
    layoutProfile = [[sg.Text('Nome'), sg.InputText(patient.name,key='name')],
                     [sg.Text('Cognome'), sg.InputText(patient.surname,key='surname')],
                     [sg.Text('Codice fiscale'), sg.Text(patient.cf, key='cf')],
                     [sg.Button('Salva'), sg.Button('Home')]]
    windowProfile = sg.Window('Profile', layoutProfile)

    while True:
        event, values = windowProfile.read()  # SANIFICARE
        if event == sg.WIN_CLOSED:
            break
        if event == 'Home':
            break
        if event == 'Salva':
            if checkValues(values):
                patientContracts.update_patient(patient.cf, private_key, values['name'], values['surname'])
                windowProfile['-OUTPUT-'].update('Modifiche registrate', text_color='green')
                patient.name = values['name']
                patient.surname = values['surname']

            else:
                windowProfile['-OUTPUT-'].update('Modifiche non valide', text_color='red')
                windowProfile['name'].update(patient.name)
                windowProfile['surname'].update(patient.surname)
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
    if values['name'] == '' or values['surname'] == '':
        sg.popup_error('Uno dei campi è vuoto, inserire un input valido')
        return 0
    return 1