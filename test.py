import keyboard
import pyautogui as pag
import time

lst = []



while True:
    if keyboard.is_pressed('shift'):
        lst.append(tuple(pag.position()))
        time.sleep(0.5)    
        print(lst, len(lst))
