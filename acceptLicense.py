import pyautogui
import time
from PIL import Image

# Funzione per trovare un'immagine sullo schermo e cliccare su di essa
def click_image(image_path, confidence=0.8):
    location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    print(location)
    if location:
        pyautogui.click(location)
    else:
        print(f"Immagine {image_path} non trovata")

# Funzione per scrivere il codice nella seconda schermata
def paste_code(code):
    pyautogui.typewrite(code)

# Funzione per automatizzare la prima schermata
def automate_first_screen():
    # Aspetta che la finestra sia visibile
    time.sleep(2)
    # Seleziona la checkbox
    click_image('check.png')  # Cambia con il percorso dell'immagine della checkbox
    # Clicca su OK

    click_image('ok.png')  # Cambia con il percorso dell'immagine del pulsante OK

# Funzione per automatizzare la seconda schermata
def automate_second_screen(code):
    # Aspetta che la finestra sia visibile
    time.sleep(2)
    # Incolla il codice
    paste_code(code)
    # Clicca su OK
    click_image('ok.png')  # Cambia con il percorso dell'immagine del pulsante OK

# Funzione per automatizzare la terza schermata
def automate_third_screen():
    # Aspetta che la finestra sia visibile
    time.sleep(2)
    # Clicca su OK
    click_image('ok.png')  # Cambia con il percorso dell'immagine del pulsante OK

# Esegui le funzioni in sequenza
def main():
    code = 'eNy7JsMVa9W8NDlLbInkNHlEV2Hrl4wrZtSXIP6jIhkrRslkdNmNV8s2bG3ABqlrcZiCI4swIdk9xUp6YJ2LV3uXcW2ZVDJURGCZIH6YMtTcckyJMMD5QNzTMaztcO1tNCyAwHiZT7GNlfjpZIWR5iz9ZRUDRwlnc6G6xiv1eBWT1glAbXn2R3WBZkX0J9zeagW79QuYI1jkoyxvLbC4JwOvYZWO1UlWROm5l5y7cq34QKi9O0ieJ5Mtbs3JJrp8cyyEIysNIDkD5hhLbGWIVDM3YcXRNU0DIDjwoailQoX4Rz0SavWnxnpUIjicwSiyQI2k9sttcSGDFAu9eRSVIU6xIli7IUsaIZkiNp1mcl3uRevjbaWlVkyKSRUMQHisOsiDIZynOqToMtxKM6CZIpsvIhkFRkhLdYGhVeJ7cB3nNY1eZKWZQoi0OJidI4wYNbya8dwlOvC38Sy4MlDdIi0LI1irwXiORgGVFs0LZDUYV84ocuG7lpyeZQX4Mui5OniUIfwONqyA8twFOUCr8kyMMaDgIA1GIrikwhiaRgWw1rhlanWtxmBBZHGCRFyiZ1XDNSzMIdjtoqi6YGXzR00waKW9xopibtGP90yFauXfNqA2Zc2v1Ph9aSW1wWufYr2A9NtBI3izw6iXS0V1BHBKZQGhREyZZ7X3NPzFI7jzogi6MBTDk0zTLtjvIGwfNqSB4Ux9MJzmEYuOMAi0JM9z7023c23057830616dc5989b62ba3e6a5c9ea03b47e8c882f873270737e38ff44618c3644262be9e7f2e38fd961ea5ae8a857de50b60aca39a92d323a5d3fc608fd60b6f55df569f5d7e345d9733838b8cc3cbfae2cc8c0d6f7b496a791687ca6511940d6f5df3d93aa6ebe177477b5629c2fb008cdd81f6e19503067661d290998cc824345bb59d7039f7b64ac5029ffce411d299346bbe029f491730e3a1ed940e55cdcf6f4021f52060013ee24e6e58265f331b7e9a17d2774f6938d85e3e18f857153075d59bdf14e90ffc635352908d5172650365999fd9d7a9aea2e72f0ccab94cb971bcf833a7aafa92c83c57b3d53e8562d4e2132dee239bffde3a66d82d02e674b72746029089b17bc29890a37d31622d1d07bfc4b4fb821d988f0431066fdabcef20dcce41a713a279ca764283db1331d61f234b3e58d6b134d31680fa73ec4715f8ec891a3ae7ceb1b1b5c647aa9ab8f278cd6fe401fbb799bc6bf0f897d4930abbac3c8a3b87f23fd937d308eb0e99e8a89b6526803f374514bbbdc6c485a5fb6be91a6daf42ecf9022c6b2eb038b183f2fe220790541306fd5ca20fb52a2d0071e6b69a64626a5c777aa126ad4550c75e2db2e9b6714834e5d7353ab5635dd7e1a8eb2b8df71c23b00fc518f04f8df7b0239f51d3d2d9644e659d8074796691678d04902817db65aa9ee4ecee0d16629ffe42899b1ba1bdb0cee'  # Inserisci qui il tuo codice
    print('CIAOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
    automate_first_screen()
    time.sleep(2)
    automate_second_screen(code)
    time.sleep(2)
    automate_third_screen()

if __name__ == '__main__':
    main()
