import PySimpleGUI as sg

def homeInfermiere(infermiere):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Benvenuto {infermiere.nome} {infermiere.cognome}')],
        [sg.Text('Inserire il codice fiscale del paziente:'), sg.InputText(), sg.Button('Ok')],
        [ sg.Button('Indietro'), sg.Button('Profilo')]
    ]

    windowHome = sg.Window('Home', layout)

    while True:
        event, codiceFiscale = windowHome.read()

        if event == sg.WINDOW_CLOSED or event == 'Indietro':
            break
        elif event == 'Profilo':
            windowHome.Hide()
            profiloInfermiere(infermiere, windowHome)
        elif event == 'Ok':
            paziente = ricercaPaziente(codiceFiscale)
            cartella = ricercaCartella(codiceFiscale)
            if cartella:
                windowHome.Hide()
                cartellaPaziente(paziente, cartella, windowHome)
            break

    windowHome.close()

def cartellaPaziente(paziente, cartella, windowHome):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Cartella di {paziente.nome} {paziente.cognome}')],
        [sg.Text(f'Nome: {paziente.nome}')],
        [sg.Text(f'Cognome: {paziente.cognome}')],
        [sg.Text(f'Codice fiscale: {paziente.codiceFiscale}')],
        [sg.Text('Prescrizioni:')],
        [sg.Listbox(values=cartella.prescrizioni, size=(30, 5))],
        [sg.Text('Note:')],
        [sg.Listbox(values=cartella.note, size=(30, 5))],
        [sg.Button('Chiudi'), sg.Button('Aggiungi nota'), sg.Button('Conferma'), sg.Button('Home')]
    ]

    windowCartella = sg.Window('Cartella Paziente', layout)

    while True:
        event, values = windowCartella.read()

        if event == sg.WINDOW_CLOSED or event == 'Chiudi':
            break
        elif event == 'Conferma':
            confermaCure(paziente,cartella) #non so come ma conferma di aver adto le cure che il medico
                                            #ha scritto nelle prescrizioni
        elif event == 'Aggiungi':
            nota_inserita = values['nota_input']
            if nota_inserita:
                aggiungiNotaPaziente(paziente,cartella, windowCartella)

        elif event == 'Home':
            windowHome.UnHide()
            break

    windowCartella.close()

def aggiungiNotaPaziente(paziente,cartella, windowCartella):
    sg.theme('DarkAmber')

    layout = [
        [sg.Text(f'Aggiungi Nota per {paziente.nome} {paziente.cognome}')],
        [sg.Text('Nuova Nota:'), sg.InputText(key='nuova_nota')],
        [sg.Button('Aggiungi'), sg.Button('Annulla')]
    ]

    windowAggiungiNota = sg.Window('Aggiungi Nota', layout)

    while True:
        event, values = windowAggiungiNota.read()

        if event == sg.WINDOW_CLOSED or event == 'Annulla':
            break
        elif event == 'Aggiungi':
            nuova_nota = values['nuova_nota']
            if nuova_nota:
                conferma = sg.popup_ok_cancel(f'Confermi di voler aggiungere la nota?')
                if conferma == 'OK':
                    cartella.note.append(nuova_nota)
                    sg.popup(f'Nota aggiunta.')
                    break

    windowAggiungiNota.close()

def profiloInfermiere(infermiere, windowHome):
    layoutProfilo = [[sg.Text(f'Nome: {infermiere.nome}')],
        [sg.Text(f'Cognome: {infermiere.cognome}')],
        [sg.Text(f'Codice fiscale: {infermiere.codiceFiscale}')],
              [sg.Button('Home')]]

    windowProfilo = sg.Window('Home', layoutProfilo)

    while True:
        event, valoriInput = windowProfilo.read()  # SANIFICARE
        if event == sg.WIN_CLOSED:
            break
        if event == 'Home':
            windowHome.UnHide()
            break
    windowProfilo.close()
    windowHome.UnHide()


def ricercaPaziente(codiceFiscale):
    pass

def ricercaCartella(codiceFiscale):
    pass

def confermaCure(paziente, cartella):
    pass
