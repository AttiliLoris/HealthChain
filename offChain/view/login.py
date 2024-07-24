import json
from collections import namedtuple

import PySimpleGUI as sg

Admin = namedtuple('Admin', ['username','password'])

def login(doctorContracts, caregiverContracts, patientContracts,healthFileContract):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Benvenuto, Inserire codice fiscale e password')],
        [sg.Text('Codice fiscale', size=(15, 1)), sg.InputText(key='cf')],
        [sg.Text('Password', size=(15, 1)), sg.InputText(key='password', password_char='*')],
        [ sg.Button('Esci'), sg.Button('Conferma'), sg.Button('Registrati')],
        [sg.Text('', size=(30, 1), key='-OUTPUT-')]
    ]

    windowLogin = sg.Window('Login', layout)

    while True:
        event, values = windowLogin.read()

        if event == sg.WINDOW_CLOSED or event == 'Esci':
            windowLogin.Hide()
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
            windowLogin.Hide()
            signIn(patientContracts,healthFileContract,windowLogin)
def checkCredentials (cf,password,doctorContracts, caregiverContracts, patientContracts):
    try:
        user = doctorContracts.get_doctor(cf)
        if user and user.password == password:
            return user
        user = caregiverContracts.get_caregiver(cf)
        if user and user.password == password:
            return user
        user = patientContracts.get_patient(cf)
        if user and user.password == password:
            return user
        user = loadAdmin()
        if user['username'] == cf and user['password'] == password:
            admin = Admin(user['username'], user['password'])
            return admin
        raise ValueError("")
    except ValueError as e:
        return 0

def signIn(patientContracts,healthFileContract,windowLogin):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text('Nome: '), sg.InputText(key='name')],
        [sg.Text('Cognome: '), sg.InputText(key='surname')],
        [sg.Text('Codice fiscale: '), sg.InputText(key='cf')],
        [sg.Text('Luogo di nascita: '), sg.InputText(key='birthPlace')],
        [sg.Text('Indipendente: '), sg.InputText(key='isIndependent')],#come bottone
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
            patientContracts.create_patient(values['name'], values['surname'],values['birthPlace'], values['hashedPwd'], bool(values['isIndependent']),values['cf'])
            healthFileContract.create_healthFile(values['cf'])
            windowSignIn['-OUTPUT-'].update('Paziente registrato', text_color='green')
        windowSignIn.close()
        windowLogin.UnHide()

def loadAdmin():
    with open("offChain/credential/credential.json", 'r') as file:
        data = json.load(file)
    return data
