import PySimpleGUI as sg


def caregiver_registration_panel(caregiverContract,private_key):
    layout = [
        [sg.Text('Nome'), sg.InputText(key='name')],
        [sg.Text('Cognome'), sg.InputText(key='lastname')],
        [sg.Text('Codice Fiscale'), sg.InputText(key='cf')],
        [sg.Text('Password'), sg.InputText(key='password')],
        [sg.Button('Registra caregiver'), sg.Button('Annulla')]
    ]
    window = sg.Window('Registra caregiver', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Annulla':
            break
        elif event == 'Registra caregiver':
            caregiverContract.create_caregiver(values['cf'], private_key, values['name'], values['lastname'], values['hashedPwd'], values['cf'])

    window.close()
def doctor_registration_panel(doctorContract, private_key):
    layout = [
        [sg.Text('Nome'), sg.InputText(key='name')],
        [sg.Text('Cognome'), sg.InputText(key='lastname')],
        [sg.Text('Codice Fiscale'), sg.InputText(key='cf')],
        [sg.Text('Password'), sg.InputText(key='password')],
        [sg.Button('Registra dottore'), sg.Button('Annulla')]
    ]
    window = sg.Window('Registra dottore', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Annulla':
            break
        elif event == 'Registra dottore':
            doctorContract.create_doctor(values['cf'], private_key, values['name'], values['lastname'], values['hashedPwd'], values['cf'])
            #bobo loris  sta facendo

    window.close()

