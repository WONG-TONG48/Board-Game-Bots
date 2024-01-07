import pyautogui as pag
import keyboard
import time

while True:

    if keyboard.is_pressed('shift'):
        pag.screenshot().show()

    