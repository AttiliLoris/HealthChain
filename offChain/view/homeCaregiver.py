import PySimpleGUI as sg

def homeCaregiver(caregiver):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Benvenuto {caregiver.name} {caregiver.surname}')],
        [sg.Text('Inserire il codice fiscale del paziente:'), sg.InputText(key='cf'), sg.Button('Ok')],
        [ sg.Button('Indietro'), sg.Button('Profilo')]
    ]

    windowHome = sg.Window('Home', layout)

    while True:
        event, values = windowHome.read()

        if event == sg.WINDOW_CLOSED or event == 'Indietro':
            break
        elif event == 'Profilo':
            windowHome.Hide()
            caregiverProfile(caregiver, windowHome)
        elif event == 'Ok':
            cf = values['cf']
            healthFile = healthFileResearch(cf)
            if healthFile:
                windowHome.Hide()
                patientHealthFile(healthFile, windowHome)
            break

    windowHome.close()

def patientHealthFile(healthFile, windowHome):
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
        [sg.Button('Chiudi'), sg.Button('Aggiungi nota'), sg.Button('Conferma'), sg.Button('Home')]
    ]

    windowHealthFile = sg.Window('Cartella Paziente', layout)

    while True:
        event, values = windowHealthFile.read()

        if event == sg.WINDOW_CLOSED or event == 'Chiudi':
            break
        elif event == 'Conferma':
            confermaCure(healthFile) #non so come ma conferma di aver adto le cure che il medico
                                            #ha scritto nelle prescrizioni
        elif event == 'Aggiungi':
            note = values['nota_input']
            if note:
                addNote(healthFile, windowHealthFile)
        elif event == 'Home':
            windowHome.UnHide()
            break

    windowHealthFile.close()

def addNote(healthFile, windowHealthFile):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Aggiungi Nota per {healthFile.name} {healthFile.surname}')],
        [sg.Text('Nuova Nota:'), sg.InputText(key='nuova_nota')],
        [sg.Button('Aggiungi'), sg.Button('Annulla')]
    ]

    windowAddNote = sg.Window('Aggiungi Nota', layout)

    while True:
        event, values = windowAddNote.read()

        if event == sg.WINDOW_CLOSED or event == 'Annulla':
            break
        elif event == 'Aggiungi':
            newNote = values['nuova_nota']
            if newNote:
                conferma = sg.popup_ok_cancel(f'Confermi di voler aggiungere la nota?')
                if conferma == 'OK':
                    healthFile.notes.append(newNote)
                    sg.popup(f'Nota aggiunta.')
                    break

    windowAddNote.close()
    windowHealthFile.UnHide()

def caregiverProfile(caregiver, windowHome):
    layoutProfilo = [[sg.Text(f'Nome: {caregiver.name}')],
        [sg.Text(f'Cognome: {caregiver.surname}')],
        [sg.Text(f'Codice fiscale: {caregiver.cf}')],
              [sg.Button('Home')]]

    windowProfile = sg.Window('Home', layoutProfilo)

    while True:
        event, valoriInput = windowProfile.read()  # SANIFICARE
        if event == sg.WIN_CLOSED:
            break
        if event == 'Home':
            windowHome.UnHide()
            break
    windowProfile.close()
    windowHome.UnHide()


def patientResearch(codiceFiscale):
    pass

def healthFileResearch(codiceFiscale):
    pass

def confermaCure(paziente, cartella):
    pass
