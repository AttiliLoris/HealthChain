import PySimpleGUI as sg
def homePaziente(paziente):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Benvenuto {paziente.nome} {paziente.cognome}')],
        [sg.Button('Visualizza cartella clinica'), sg.Button('Modifica profilo')]
    ]

    windowHomePaziente = sg.Window('Home Paziente', layout)

    while True:
        event, values = windowHomePaziente.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Visualizza cartella clinica':
            cartella = ricercaCartella(paziente.codiceFiscale)
            visualizzaCartellaClinica(paziente, cartella)
        elif event == 'Modifica profilo':
            modificaProfilo(paziente)

    windowHomePaziente.close()

def visualizzaCartellaClinica(paziente):
    sg.theme('DarkAmber')
    cartella = ricercaCartella(paziente.codiceFiscale)
    layout = [
        [sg.Text(f'Cartella di {paziente.nome} {paziente.cognome}')],
        [sg.Text(f'Nome: {paziente.nome}')],
        [sg.Text(f'Cognome: {paziente.cognome}')],
        [sg.Text(f'Codice fiscale: {paziente.codiceFiscale}')],
        [sg.Text('Prescrizioni:')],
        [sg.Listbox(values=cartella.prescrizioni, size=(30, 5))],
        [sg.Text('Note:')],
        [sg.Listbox(values=cartella.note, size=(30, 5))],
        [sg.Button('Chiudi')]
    ]

    windowCartellaClinica = sg.Window('Cartella Clinica', layout)

    while True:
        event, values = windowCartellaClinica.read()

        if event == sg.WINDOW_CLOSED or event == 'Chiudi':
            break

    windowCartellaClinica.close()

def modificaProfilo(paziente):
    pass

def ricercaCartella(codiceFiscale):
    pass