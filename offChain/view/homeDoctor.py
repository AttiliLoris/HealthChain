import PySimpleGUI as sg
from ..model.healthFile import HealthFile
from..model.doctor import Doctor
def homeDoctor(doctor,doctorContracts,healthFileContracts, private_key):
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
            doctorProfile(doctor, windowHome,doctorContracts,private_key)
        if event == 'Ok':
            healthFile = healthFileResearch(cf,healthFileContracts)
            if healthFile:
                windowHome.Hide()
                patientHealthFile(healthFile, windowHome, healthFileContracts,private_key)

    windowHome.close()

def doctorProfile(doctor, windowHome,doctorContracts,private_key):
    layoutProfile = [[sg.Text('Nome'), sg.InputText(doctor.name,key='name')],
                    [sg.Text('Cognome'), sg.InputText(doctor.surname,key='surname')],
                    [sg.Text('Codice fiscale'), sg.Text(doctor.cf,key='cf')],
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
                doctorContracts.update_doctor(doctor.cf,private_key,values['name'],values['surname'])
                windowProfile['-OUTPUT-'].update('Modifiche registrate', text_color='green')
                doctor.name = values['name']
                doctor.surname = values['surname']

            else:
                windowProfile['-OUTPUT-'].update('Modifiche non valide', text_color='red')
                windowProfile['name'].update(doctor.name)
                windowProfile['surname'].update(doctor.surname)
                windowProfile['cf'].update(doctor.cf)
    windowProfile.close()
    windowHome.UnHide()

def checkValues(values):
    if values['name'] == '' or values['surname'] == '':
        sg.popup_error('Uno dei campi è vuoto, inserire un input valido')
        return 0
    return 1

def healthFileResearch(cf,healthFileContracts):
    try:
        healthFile = healthFileContracts.get_healthFile(cf)
        if healthFile:
            return healthFile
    except ValueError as e:
        return None
    return None

def patientHealthFile(healthFile, windowHome, healthFileContracts, private_key):
    layoutHealthFile = [[sg.Text('Nome: ' + healthFile.name), sg.Text('Cognome: '+ healthFile.surname), sg.Text('Codice fiscale: '+ healthFile.cf)],
                        [sg.Text('Storia clinica: '), sg.Text(healthFile.clinicHistory)],
                        [sg.Text('Prescrizioni: '), sg.Text(healthFile.prescriptions)],
                        [sg.Text('Trattamenti: '), sg.Text(healthFile.treatmentPlan)], #è un vettore non so se si fa così
                        [sg.Button('Home'), sg.Button('Aggiorna storia clinica'), sg.Button('Modifica prescrizioni'), sg.Button('Aggiungi trattamento')]]

    windowHealthFile = sg.Window('Fascicolo '+ healthFile.name +' '+  healthFile.surname, layoutHealthFile)

    while True:
        event, values = windowHealthFile.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Aggiorna storia clinica':
            windowHealthFile.Hide()
            modififyClinicHistory(healthFile, windowHealthFile,healthFileContracts, private_key)
        if event == 'Modifica prescrizioni':
            windowHealthFile.Hide()
            modifyPrescriptions(healthFile, windowHealthFile, healthFileContracts,private_key)
        if event == 'Home':
            windowHome.UnHide()
        if event == 'Aggiungi trattamento':
            windowHealthFile.hide()
            addTreatmentPlan(healthFile, windowHealthFile,healthFileContracts,private_key) #cosa è private_key??
            break
    windowHealthFile.close()



def modififyClinicHistory(healthFile, windowHealthFile, healthFileContracts, private_key):
    layoutClinicHistory = [[sg.Text('Storia clinica: '), sg.InputText(healthFile.clinicHistory,key='clinicHistory')],
                            [sg.Button('Conferma'), sg.Button('Indietro')]]
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
                healthFileContracts.update_healthFile(cf, private_key, name, surname)#vanno aggiunti gli attributi
                healthFile.clinicHistory=text
                break
        if event == 'Indietro':
            break
    windowClinicHistory.close()
    windowHealthFile.UnHide()
def modifyPrescriptions(healthFile, windowHealthFile, healthFileContracts,private_key):
    layoutPrescription = [[sg.Text('Prescrizioni: '), sg.InputText(healthFile.prescriptions, key='prescriptions')],
                           [sg.Button('Conferma'), sg.Button('Indietro')]]
    windowPrescription = sg.Window('Dettaglio', layoutPrescription)

    while True:
        event, values = windowPrescription.read()
        text = values['prescriptions']
        if event == sg.WIN_CLOSED:
            break
        if event == 'Conferma':
            if text == '':
                sg.popup_error('Il testo è vuoto, modifiche non valide')
            else:
                healthFileContracts.update_healthFile(cf, private_key, name, surname)  # vanno aggiunti gli attributi
                healthFile.prescriptions = text
                break
        if event == 'Indietro':
            break
    windowPrescription.close()
    windowHealthFile.UnHide()

#non ho capito come funziona private_key, cioè se in caregiver le note le ho potute aggiungere così: perchè non posso
#farlo anche per i trattamenti e di base anche per la storia clinica ad esempio??
def addTreatmentPlan(healthFile, windowHealthFile):
    sg.theme('DarkAmber')

    layoutTreatmentPlan= [[sg.Text('Trattamenti: '), sg.InputText(healthFile.treatmentPlan, key='treatmentPlan')],
                          [sg.Button('Conferma'), sg.Button('Indietro')]]
    windowTreatmentPlan = sg.Window('Dettaglio', layoutTreatmentPlan)

    while True:
        event, values = windowTreatmentPlan.read()

        if event == sg.WINDOW_CLOSED or event == 'Annulla':
            break
        elif event == 'Aggiungi':
            newTreatmentPlan = values['treatmentPlan']
            if newTreatmentPlan:
                conferma = sg.popup_ok_cancel(f'Confermi di voler aggiungere il trattamento?')
                if conferma == 'OK':
                    healthFile.treatmentPlan.append(newTreatmentPlan)
                    sg.popup(f'trattamento aggiunto.')
                    break

    windowTreatmentPlan.close()
    windowHealthFile.UnHide()
