try:
  import pyautogui
except:
  os.system("py -m pip install pyautogui")
  import pyautogui


# Inform the user to click on the console window
print("Click on the console window to get the cursor coordinates\n")

while True:
    # Get the coordinates of the mouse cursor
    x, y = pyautogui.position()

    # Print the coordinates to the console
    print(f"Cursor coordinates: ({x}, {y})")

