import PySimpleGUI as sg
import Logica

def homeMedico(medico):
    sg.theme('DarkAmber')
    layoutHome = [[sg.Text('Inserire il codice fiscale di un paziente per vedere il suo fascicolo'), sg.InputText()],
                [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Profilo')] ]


    windowHome = sg.Window('Home', layoutHome)

    while True:
        event, codiceFiscale = windowHome.read() #SANIFICARE
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Profilo':
            windowHome.Hide()
            profiloMedico(medico, windowHome)
        if event == 'Ok':
            paziente = ricercaPaziente(codiceFiscale)
            fascicolo = ricercaFascicolo(codiceFiscale)
            if fascicoloPaziente:
                windowHome.Hide()
                fascicoloPaziente(paziente, fascicolo, windowHome)

    windowHome.close()

def profiloMedico(medico, windowHome):
    layoutProfilo = [[sg.Text('Nome'), sg.InputText(medico.nome)],
              [sg.Text('Cognome'), sg.InputText(medico.cognome)],
              [sg.Text('Codice fiscale'), sg.InputText(medico.codiceFiscale)],
              [sg.Button('Salva'), sg.Button('Home')]]

    windowProfilo = sg.Window('Home', layoutProfilo)

    while True:
        event, valoriInput = windowProfilo.read()  # SANIFICARE
        if event == sg.WIN_CLOSED:
            break
        if event == 'Home':
            break
        if event == 'Salva':
            if controllaValori(valoriInput):
                pass
            else:
                break
    windowProfilo.close()
    windowHome.UnHide()

def controllaValori(valoriInput):
    for elemento in valoriInput:
        if valoriInput[elemento] == '':
            sg.popup_error('Uno dei campi è vuoto, inserire un input valido')
            return 1
    medico.salva(valoriInput)

medico = Medico.Medico('Loris', 'Attili', 'CF1')
homeMedico(medico)


def ricercaPaziente(codiceFiscale):
    pass
def ricercaFascicolo(codiceFiscale):
    pass

def fascicoloPaziente(paziente, fascicolo, windowHome):
    layoutFascicolo = [[sg.Text('Nome: ' + paziente.nome), sg.Text('Cognome: '+ paziente.cognome), sg.Text('Codice fiscale: '+ paziente.codiceFiscale)],
                        [sg.Text('Storia clinica: '), sg.Text(fascicolo.storiaClinica)],
                        [sg.Text('Prescrizioni: '), sg.Text(fascicolo.prescrizioni)],
                        [sg.Button('Home'), sg.Button('Modifica storia clinica'), sg.Button('Modifica prescrizioni')]]

    windowFascicolo = sg.Window('Fascicolo '+ paziente.nome +' '+  paziente.cognome, layoutFascicolo)

    while True:
        event, values = windowFascicolo.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Modifica storia clinica':
            windowFascicolo.Hide()
            modificaStoriaClinica(fascicolo, windowFascicolo)
        if event == 'Modifica prescrizioni':
            windowFascicolo.Hide()
            modificaPrescrizioni(fascicolo)
        if event == 'Home':
            windowHome.UnHide()
            break
    windowFascicolo.close()



def modificaStoriaClinica(fascicolo, windowFascicolo):
    layoutModificaStoria = [[sg.Text('Storia clinica: '), sg.InputText(fascicolo.storiaClinica)]
                            [sg.Button('Conferma'), Sg.Button('Indietro')]]
    windowModificaStoria = sg.Window('Dettaglio', layoutModificaStoria)

    while True:
        event, testo = windowModificaStoria.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Conferma':
            if testo =='':
                sg.popup_error('Il testo è vuoto, modifiche non valide')
            else:
                fascicolo.storiaClinica(testo)
                break
        if event == 'Indietro':
            break
    windowModificaStoria.close()
    windowFascicolo.UnHide()
def modificaPrescrizioni(fascicolo):
    pass