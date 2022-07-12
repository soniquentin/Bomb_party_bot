from tools import *
import pyautogui
import easyocr
import cv2
import numpy as np
import keyboard
import unidecode



####PARAMETRES#####
img_name = r"fig.png"
screenshot_name = r"screenshot.png"
template_name ="template.png"
###################


frenchdict = Lexique()
x0, y0, largeur, hauteur  = select_coord(img_name) #Demande à l'utilisateur dans quelle région sont affichés les mots
pyautogui.screenshot(img_name, region = (x0, y0, largeur, hauteur))
template = cv2.imread("template.png",0)
changed = False

while True :

    pyautogui.screenshot(screenshot_name)
    screenshot = cv2.imread(screenshot_name,0)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)



    if max_val >= 0.7 :
        if not(changed) :
            pyautogui.screenshot(img_name, region = (x0, y0, largeur, hauteur))
            reader = easyocr.Reader(['fr'], gpu = True)
            coord, substr, confidence = reader.readtext(img_name)[0]
            substr = substr.lower()
            word,secu = frenchdict.look_for(substr)
            word,secu = unidecode.unidecode( word ) , unidecode.unidecode( secu ) 
        else :
            word = secu
            pyautogui.typewrite(secu)
            pyautogui.typewrite('\n')
        pyautogui.typewrite(word)
        pyautogui.typewrite('\n')
        changed = True
    else :
        if changed :
            for c in word :
                frenchdict.letters_remaining[c] = 0
            frenchdict.reset_remaining()
            changed = False
