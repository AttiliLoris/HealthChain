import pyautogui

print("Move your mouse to the desired position and press Ctrl+C to get the coordinates.")
try:
    while True:
        x, y = pyautogui.position()
        print(f"Position: {x}, {y}", end="\r")
except KeyboardInterrupt:
    print("\nStopped.")