import pyautogui
import time

# Funzione per aspettare che un'immagine specifica sia visibile e fare click su di essa
def click_image(image_path, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)
        if location is not None:
            pyautogui.click(location)
            return True
        time.sleep(1)
    return False

# Attendi qualche secondo per assicurarti che la finestra sia visibile
time.sleep(5)

# Clicca sulla casella di controllo "I accept the terms in the License Agreement"
if not click_image('acceptButton.png'):  # Immagine della casella di controllo
    print("Failed to click accept button")
    exit(1)

# Clicca sul pulsante "Ok"
if not click_image('okButton.png'):  # Immagine del pulsante Ok
    print("Failed to click Ok button")
    exit(1)

# Attendi la schermata "Final Step"
time.sleep(2)  # Assicurati che la nuova finestra sia caricata

# Inserisci il codice della licenza nel campo di testo
license_key = "YOUR_LICENSE_KEY"  # Sostituisci con il tuo codice della licenza
pyautogui.write(license_key)

# Clicca sul pulsante "Ok"
if not click_image('okButton.png'):  # Immagine del pulsante Ok nella schermata finale
    print("Failed to click final Ok button")
    exit(1)

# Attendi la schermata "Trial Period Started"
if not click_image('okButton.png'):  # Immagine del pulsante Ok nella schermata di trial
    print("Failed to click Ok button on trial screen")
    exit(1)

print("Licenza accettata automaticamente")
