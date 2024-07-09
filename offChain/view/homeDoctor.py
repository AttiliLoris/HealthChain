import PySimpleGUI as sg
from ..model.healthFile import HealthFile
def homeDoctor(doctor):
    sg.theme('DarkAmber')
    layoutHome = [[sg.Text('Inserire il codice fiscale di un paziente per vedere il suo fascicolo'), sg.InputText(key='cf')],
                [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Profilo')] ]


    windowHome = sg.Window('Home', layoutHome)

    while True:
        event, values = windowHome.read() #SANIFICARE
        cf=values['cf']
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Profilo':
            windowHome.Hide()
            doctorProfile(doctor, windowHome)
        if event == 'Ok':
            healthFile = healthFileResearch(cf)
            if healthFile:
                windowHome.Hide()
                patientHealthFile(healthFile, windowHome)

    windowHome.close()

def doctorProfile(doctor, windowHome):
    layoutProfile = [[sg.Text('Nome'), sg.InputText(doctor.name,key='name')],
                    [sg.Text('Cognome'), sg.InputText(doctor.surname,key='surname')],
                    [sg.Text('Codice fiscale'), sg.InputText(doctor.cf,key='cf')],
                    [sg.Button('Salva'), sg.Button('Home')],
                    [sg.Text('', size=(30, 1), key='-OUTPUT-')]]

    windowProfile = sg.Window('Profile', layoutProfile)

    while True:
        event, values = windowProfile.read()  # SANIFICARE
        if event == sg.WIN_CLOSED:
            break
        if event == 'Home':
            break
        if event == 'Salva':
            if checkValues(values):
        else:
            windowProfile['-OUTPUT-'].update('Invalid input', text_color='red')
            windowProfile['name']=doctor.name
            windowProfile['surname'] = doctor.surname
            windowProfile['cf'] = doctor.cf
    windowProfile.close()
    windowHome.UnHide()

def checkValues(values):
    for element in values:
        if values[element] == '':
            sg.popup_error('Uno dei campi è vuoto, inserire un input valido')
            return 0
    return 1

def healthFileResearch(codiceFiscale):
    pass

def patientHealthFile(healthFile, windowHome):
    layoutHealthFile = [[sg.Text('Nome: ' + healthFile.name), sg.Text('Cognome: '+ healthFile.surname), sg.Text('Codice fiscale: '+ healthFile.cf)],
                        [sg.Text('Storia clinica: '), sg.Text(healthFile.clinicHistory)],
                        [sg.Text('Prescrizioni: '), sg.Text(healthFile.prescriptions)],
                        [sg.Button('Home'), sg.Button('Modifica storia clinica'), sg.Button('Modifica prescrizioni')]]

    windowHealthFile = sg.Window('Fascicolo '+ healthFile.name +' '+  healthFile.surname, layoutHealthFile)

    while True:
        event, values = windowHealthFile.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Modifica storia clinica':
            windowHealthFile.Hide()
            modififyClinicHistory(healthFile, windowHealthFile)
        if event == 'Modifica prescrizioni':
            windowHealthFile.Hide()
            modifyPrescriptions(healthFile)
        if event == 'Home':
            windowHome.UnHide()
            break
    windowHealthFile.close()



def modififyClinicHistory(healthFile, windowHealthFile):
    layoutClinicHistory = [[sg.Text('Storia clinica: '), sg.InputText(healthFile.clinicHistory,key='clinicHistory')]
                            [sg.Button('Conferma'), Sg.Button('Indietro')]]
    windowClinicHistory = sg.Window('Dettaglio', layoutClinicHistory)

    while True:
        event, values = windowClinicHistory.read()
        text= values['clinicHistory']
        if event == sg.WIN_CLOSED:
            break
        if event == 'Conferma':
            if text =='':
                sg.popup_error('Il testo è vuoto, modifiche non valide')
            else:
                healthFile.clinicHistory(text)
                break
        if event == 'Indietro':
            break
    windowClinicHistory.close()
    windowHealthFile.UnHide()
def modifyPrescriptions(fascicolo):
    pass
