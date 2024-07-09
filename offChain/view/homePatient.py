import PySimpleGUI as sg
def homePatient(patient):
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
            healthFile = researchHealthFile(patient.cf)
            windowHome.Hide()
            viewHealthFile(healthFile, windowHome)
        elif event == 'Modifica profilo':
            windowHome.Hide()
            modifyProfile(patient)

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

def modifyProfile(patient):
    pass

def researchHealthFile(cf):
    pass