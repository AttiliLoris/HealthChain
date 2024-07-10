import PySimpleGUI as sg

def login(doctorContracts, caregiverContracts, patientContracts):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Benvenuto, Inserire codice fiscale e password')],
        [sg.Text('Codice fiscale', size=(15, 1)), sg.InputText(key='cf')],
        [sg.Text('Password', size=(15, 1)), sg.InputText(key='password', password_char='*')],
        [ sg.Button('Esci'), sg.Button('Conferma')],
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
