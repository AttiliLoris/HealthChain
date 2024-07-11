import PySimpleGUI as sg

def login(doctorContracts, caregiverContracts, patientContracts,healthFileContract):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Benvenuto, Inserire codice fiscale e password')],
        [sg.Text('Codice fiscale', size=(15, 1)), sg.InputText(key='cf')],
        [sg.Text('Password', size=(15, 1)), sg.InputText(key='password', password_char='*')],
        [ sg.Button('Esci'), sg.Button('Conferma'), sg.Button('Registritati')],
        [sg.Text('', size=(30, 1), key='-OUTPUT-')]
    ]

    windowLogin = sg.Window('Login', layout)

    while True:
        event, values = windowLogin.read()

        if event == sg.WINDOW_CLOSED or event == 'Esci':
            return None
        elif event == 'Conferma':
            utente = checkCredentials(values['cf'], values['password'],doctorContracts, caregiverContracts, patientContracts)
            if utente:
                windowLogin['-OUTPUT-'].update('Login Successful', text_color='green')
                windowLogin.close()
                return utente
            else:
                windowLogin['-OUTPUT-'].update('Login Failed', text_color='red')
                # Azzera il contenuto degli input text
                windowLogin['cf'].update('')
                windowLogin['password'].update('')
        elif event == 'Registrati':
            signIn(patientContracts,healthFileContract,windowLogin)#?????? non so cosa sto facendo
def checkCredentials (cf,password,doctorContracts, caregiverContracts, patientContracts):
    try:
        user = doctorContracts.getDoctor(cf)
        if user.password == password:
            return user
        user = caregiverContracts.getDoctor(cf)
        if user.password == password:
            return user
        user = patientContracts.getDoctor(cf)
        if user.password == password:
            return user
        raise ValueError("")
    except ValueError as e:
        return 0

def signIn(patientContracts,healthFileContract,windowLogin):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text('Nome: '), sg.InputText(key='name')],
        [sg.Text('Cognome: '), sg.InputText(key='surname')],
        [sg.Text('Codice fiscale: '), sg.InputText(key='cf')],
        [sg.Text('Data di nascita: '), sg.InputText(key='birthday')], #zi la toglierei è solo no sbatti
        [sg.Text('Luogo di nascita: '), sg.InputText(key='birthPlace')],
        [sg.Text('Password: '), sg.InputText(key='hashedPwd')], #forse da mettere doppia e che non se vede dai
        [sg.Text('', size=(30, 1), key='-OUTPUT-')],
        [sg.Button('Registrati'), sg.Button('Annulla')]
    ]

    windowSignIn = sg.Window('Registrazione', layout)


    while True:
        event, values = windowSignIn.read()

        if event == sg.WINDOW_CLOSED or event == 'Annulla':
            break
        elif event == 'Registrati':
            patientContracts.create_patient(values['name'], values['surname'], values['birthday'],values['birthPlace'],values['cf'], values['hashedPwd'])
            healthFileContract.create_healthFile(values['cf'])
            windowSignIn['-OUTPUT-'].update('Paziente registrato', text_color='green')
        windowSignIn.close()
        windowLogin.UnHide()
