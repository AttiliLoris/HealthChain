import PySimpleGUI as sg

def login(doctorContracts, caregiverContracts, patientContracts):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Benvenuto, Inserire username e password')],
        [sg.Text('Username', size=(15, 1)), sg.InputText(key='username')],
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
            utente = checkCredentials(values['username'], values['password'],doctorContracts, caregiverContracts, patientContracts)
            if utente:
                windowLogin['-OUTPUT-'].update('Login Successful', text_color='green')
                windowLogin.close()
                return utente
            else:
                windowLogin['-OUTPUT-'].update('Login Failed', text_color='red')
                # Azzerare il contenuto degli input text
                windowLogin['username'].update('')
                windowLogin['password'].update('')

def checkCredentials(username, password,doctorContracts, caregiverContracts, patientContracts):
    pass