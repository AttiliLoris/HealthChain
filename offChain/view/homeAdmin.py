import re

import PySimpleGUI as sg
import logging

def homeAdmin(admin, doctorContracts, caregiverContracts):
    logging.info('Amministratore autenticato')
    sg.theme('DarkAmber')

    layoutHome = [
        [sg.Button('Aggiungi dottore'), sg.Button('Aggiungi caregiver'), sg.Button('Esci')]]

    windowHome = sg.Window('Home', layoutHome)

    while True:
        event, values = windowHome.read()  # SANIFICARE
        if event == sg.WIN_CLOSED or event == 'Esci':
            break
        if event == 'Aggiungi caregiver':
            windowHome.Hide()
            caregiver_registration_panel(admin, caregiverContracts,windowHome)
        if event == 'Aggiungi dottore':
            windowHome.Hide()
            doctor_registration_panel(admin, doctorContracts,windowHome)

    windowHome.close()

def caregiver_registration_panel(admin, caregiverContract,windowHome):
    layout = [
        [sg.Text('Nome'), sg.InputText(key='name')],
        [sg.Text('Cognome'), sg.InputText(key='lastname')],
        [sg.Text('Codice Fiscale'), sg.InputText(key='cf')],
        [sg.Text('Password'), sg.InputText(key='password', password_char='*')],
        [sg.Text('Conferma password'), sg.InputText(key='passwordConfirm', password_char='*')],
        [sg.Button('Registra caregiver'), sg.Button('Annulla')],
        [sg.Text('', size=(30, 1), key='-OUTPUT-')]
    ]
    window = sg.Window('Registra caregiver', layout)


    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Annulla':
            break
        elif event == 'Registra caregiver':
            values['name'] = sanitizeInput(values['name'])
            values['lastname'] = sanitizeInput(values['lastname'])
            values['password'] = checkPassword(sanitizeInput(values['password']))
            values['passwordConfirm'] = checkPassword(sanitizeInput(values['passwordConfirm']))
            values['cf'] = sanitizeInput(values['cf'])
            if (values['password']!= False) and (values['password'] == values['passwordConfirm']):
                if checkValues(values) and checkCf(values['cf']):
                    logging.info('Caregiver '+ values['lastname'] + ' ' +values['name']+' creato')
                    caregiverContract.create_caregiver(admin.address, admin.private_key,values['name'], values['lastname'], values['password'], values['cf'])
                    window['-OUTPUT-'].update('Caregiver registrato', text_color='green')
                    break
            elif values['password'] != values['passwordConfirm']:
                window['-OUTPUT-'].update('Le password non corrispondono', text_color='red')
                window['name'].update(values['name'])
                window['lastname'].update(values['lastname'])
                window['password'].update('')
                window['passwordConfirm'].update('')
                window['cf'].update(values['cf'])
            elif not checkCf(values['cf']):
                window['-OUTPUT-'].update('Codice fiscale non valido', text_color='red')
            if values['password']== False:
                window['-OUTPUT-'].update('La password è troppo corta', text_color='red')
                window['password'].update('')
                window['passwordConfirm'].update('')
    windowHome.UnHide()
    window.close()
def doctor_registration_panel(admin, doctorContract,windowHome):
    layout = [
        [sg.Text('Nome'), sg.InputText(key='name')],
        [sg.Text('Cognome'), sg.InputText(key='lastname')],
        [sg.Text('Codice Fiscale'), sg.InputText(key='cf')],
        [sg.Text('Password'), sg.InputText(key='password', password_char='*')],
        [sg.Text('Conferma password'), sg.InputText(key='passwordConfirm', password_char='*')],
        [sg.Button('Registra dottore'), sg.Button('Annulla')],
        [sg.Text('', size=(30, 1), key='-OUTPUT-')]
    ]
    window = sg.Window('Registra dottore', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Annulla':
            break
        elif event == 'Registra dottore':
            values['name'] = sanitizeInput(values['name'])
            values['lastname'] = sanitizeInput(values['lastname'])
            values['password'] = checkPassword(sanitizeInput(values['password']))
            values['passwordConfirm'] = checkPassword(sanitizeInput(values['passwordConfirm']))
            values['cf'] = sanitizeInput(values['cf'])
            if (values['password']!= False) and (values['password'] == values['passwordConfirm']):
                if checkValues(values) and checkCf(values['cf']):
                    logging.info('Dottore ' + values['lastname'] + ' ' + values['name'] + ' creato')
                    doctorContract.create_doctor(admin.address, admin.private_key, values['name'], values['lastname'], values['password'], values['cf'])
                    window['-OUTPUT-'].update('Dottore registrato', text_color='green')
                    break
            if values['password'] != values['passwordConfirm']:
                window['-OUTPUT-'].update('Le password non corrispondono', text_color='red')
                window['password'].update('')
                window['passwordConfirm'].update('')
            if values['password']== False:
                window['-OUTPUT-'].update('La password è troppo corta', text_color='red')
                window['password'].update('')
                window['passwordConfirm'].update('')
            if not checkCf(values['cf']):
                window['-OUTPUT-'].update('Codice fiscale non valido', text_color='red')
    windowHome.UnHide()
    window.close()

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