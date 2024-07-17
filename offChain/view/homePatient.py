import PySimpleGUI as sg
def homePatient(patient, caregiverContracts, patientContracts, healthFileContracts, private_key):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Benvenuto {patient.name} {patient.lastname}')]
    ]
    if not patient.isIndependent:
        layout.append([sg.Button('Visualizza cartella clinica'), sg.Button('Modifica profilo')])
    else:
        layout.append([sg.Button('Visualizza cartella clinica'), sg.Button('Conferma cure'), sg.Button('Modifica profilo')])

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
        elif event == 'Conferma cure':
            viewConfirmTreatement(patient, caregiverContracts,healthFileContracts, windowHome, private_key)
    windowHome.close()

def viewHealthFile(healthFile, windowHome):
    sg.theme('DarkAmber')
    layout = [
        [sg.Text(f'Cartella di {healthFile.name} {healthFile.lastname}')],
        [sg.Text(f'Nome: {healthFile.name}')],
        [sg.Text(f'Cognome: {healthFile.lastname}')],
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
                     [sg.Text('Cognome'), sg.InputText(patient.lastname,key='lastname')],
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
                patientContracts.update_patient(patient.cf, private_key, values['name'], values['lastname'])
                windowProfile['-OUTPUT-'].update('Modifiche registrate', text_color='green')
                patient.name = values['name']
                patient.lastname = values['lastname']

            else:
                windowProfile['-OUTPUT-'].update('Modifiche non valide', text_color='red')
                windowProfile['name'].update(patient.name)
                windowProfile['lastname'].update(patient.lastname)
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
    if values['name'] == '' or values['lastname'] == '':
        sg.popup_error('Uno dei campi è vuoto, inserire un input valido')
        return 0
    return 1

def viewConfirmTreatement(patient,caregiverContracts, healthFileContracts, windowHome, private_key):
    sg.theme('DarkAmber')
    layout=[[sg.Text('Inserire codice fiscale del caregiver: '),sg.InputText('', key='cfCaregiver')],
            [sg.Text('', size=(30, 1), key='-OUTPUT-')],
            [sg.Button('Indietro'), sg.Button('Conferma')]]
    windowConfirmTreatement = sg.Window('Conferma cure', layout)

    while True:
        event, values = windowHome.read()

        if event == sg.WINDOW_CLOSED or event == 'Indietro':
            break
        elif event == 'Conferma cure':
            if checkCaregiver(values['cfCaregiver'], caregiverContracts):
                healthFileContracts.confirm_treatement( values['cfCaregiver'],patient.cf , patient.isIndependent, private_key)
            else:
                windowConfirmTreatement['-OUTPUT-'].update('Modifiche non valide', text_color='red')
                windowConfirmTreatement['cfCaregover'].update('')

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