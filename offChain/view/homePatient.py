import PySimpleGUI as sg
def homePatient(patient,patientContracts, caregiverContracts, healthFileContracts):
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
            viewHealthFile(healthFile, windowHome)
        elif event == 'Modifica profilo':
            windowHome.Hide()
            modifyProfile(patient,patientContracts, windowHome)
        elif event == 'Conferma cure':
            viewConfirmTreatement(patient, caregiverContracts,healthFileContracts, windowHome)
        elif event == 'Logout':
            break
    windowHome.close()

def viewHealthFile(healthFile, windowHome):
    sg.theme('DarkAmber')
    layout = [

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

def modifyProfile(patient,patientContracts, windowHome):
    sg.theme('DarkAmber')
    layoutProfile = [[sg.Text('Nome'), sg.InputText(patient.name,key='name')],
                     [sg.Text('Cognome'), sg.InputText(patient.lastname,key='lastname')],
                     [sg.Text('Codice fiscale'), sg.InputText(patient.cf, key='cf')],#non dovrebbe essere modificabile
                     [sg.Text('Luogo di nascita'), sg.InputText(patient.birthPlace, key='birthPlace')],
                     [sg.Text('Indipendente'), sg.InputText(patient.isIndependent, key='isIndependent')],#bottone
                     [sg.Text('Password'), sg.InputText(patient.password, key='password')],#per modificare la password dovremmo fare una cosa a parte
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
                patientContracts.update_patient(values['name'], values['lastname'],values['birthPlace'],values['password'],bool(values['isIndependent']),values['cf'])
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
    if values['name'] == '' or values['lastname'] == '':
        sg.popup_error('Uno dei campi è vuoto, inserire un input valido')
        return 0
    return 1

def viewConfirmTreatement(patient,caregiverContracts, healthFileContracts, windowHome):
    sg.theme('DarkAmber')
    layout=[[sg.Text('Inserire codice fiscale del caregiver: '),sg.InputText('', key='cfCaregiver')],
            [sg.Text('', size=(30, 1), key='-OUTPUT-')],
            [sg.Button('Indietro'), sg.Button('Conferma')]]
    windowConfirmTreatement = sg.Window('Conferma cure', layout)

    while True:
        event, values = windowHome.read()

        if event == sg.WINDOW_CLOSED or event == 'Indietro':
            break
        elif event == 'Conferma':
            if checkCaregiver(values['cfCaregiver'], caregiverContracts):
                healthFileContracts.confirm_treatement( values['cfCaregiver'],patient.cf , patient.isIndependent)
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