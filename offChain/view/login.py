import json
import re
from collections import namedtuple

import PySimpleGUI as sg

Admin = namedtuple('Admin', ['username','password','address','private_key'])

def login(doctorContracts, caregiverContracts, patientContracts,healthFileContract,fine):
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
            windowLogin.close()
            break
        elif event == 'Conferma':
            utente = checkCredentials(values['cf'], values['password'],doctorContracts, caregiverContracts, patientContracts)
            if utente:
                windowLogin['-OUTPUT-'].update('Login Successful', text_color='green')
                windowLogin.close()
                return utente
            else:
                windowLogin['-OUTPUT-'].update('Login Failed', text_color='red')
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
            admin = Admin(username=user['username'], password=user['password'],address=user['address'], private_key=user['private_key'])
            return admin
        raise ValueError("")
    except ValueError as e:
        return 0

def signIn(patientContracts,healthFileContract,windowLogin):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text('Nome: '), sg.InputText(key='name')],
        [sg.Text('Cognome: '), sg.InputText(key='lastname')],
        [sg.Text('Codice fiscale: '), sg.InputText(key='cf')],
        [sg.Text('Luogo di nascita: '), sg.InputText(key='birthPlace')],
        [sg.Text('Indipendente: '), sg.InputText(key='isIndependent')],#come bottone
        [sg.Text('Password: '), sg.InputText(key='password',password_char='*')],
        [sg.Text('', size=(30, 1), key='-OUTPUT-')],
        [sg.Button('Registrati'), sg.Button('Annulla')]
    ]

    windowSignIn = sg.Window('Registrazione', layout)


    while True:
        event, values = windowSignIn.read()

        if event == sg.WINDOW_CLOSED or event == 'Annulla':
            break
        elif event == 'Registrati':
            values['name'] = sanitizeInput(values['name'])
            values['lastname'] = sanitizeInput(values['lastname'])
            values['birthPlace'] = sanitizeInput(values['birthPlace'])
            values['password'] = sanitizeInput(values['password'])
            values['isIndependent'] = sanitizeInput(values['isIndependent'])
            values['cf'] = sanitizeInput(values['cf'])
            if checkValues(values) and checkCf(values['cf']) and checkPassword(values['password']):
                patientContracts.create_patient(values['name'], values['lastname'],values['birthPlace'], values['password'], bool(int(values['isIndependent'])),values['cf'])
                healthFileContract.create_healthFile(values['cf'])
                windowSignIn['-OUTPUT-'].update('Paziente registrato', text_color='green')
                windowSignIn.close()
                windowLogin.UnHide()
            else:
                windowSignIn['name'].update(values['name'])
                windowSignIn['lastname'].update(values['lastname'])
                windowSignIn['birthPlace'].update(values['birthPlace'])
                windowSignIn['isIndependent'].update(values['isIndependent'])
                windowSignIn['password'].update(values['password'])
                windowSignIn['cf'].update(values['cf'])
            if not checkPassword(values['password']):
                windowSignIn['-OUTPUT-'].update('La password è troppo corta', text_color='red')
    windowSignIn.close()
    windowLogin.UnHide()

def loadAdmin():
    with open("offChain/credential/credential.json", 'r') as file:
        data = json.load(file)
    return data

def sanitizeInput(value):

    sanitizedValue = re.sub(r'\b(import|exec|eval)\b', '', value, flags=re.IGNORECASE)

    if re.search(r'[^a-zA-Z0-9\s]', sanitizedValue):
        return ''

    return sanitizedValue

def checkValues(values):
    for key, value in values.items():
        if not value or (key == 'cf' and not checkCf(value)):
            sg.popup_error(f'Il campo "{key}" non è valido')
            return False
    return True

def checkCf(cf):
    if re.match(r'^[a-zA-Z0-9]{16}$', cf):
        return True
    else:
        return False

def checkPassword(password):
    if len(password) < 8:
        return False
    return password