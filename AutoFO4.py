#-----------------------------------------------#
# Author: Truong Nguyen Quoc                    #
# version: v1.0                                 #
#-----------------------------------------------#

import os
import argparse
import time
import keyboard
import pyautogui
from PIL import Image, ImageChops

CURRENT_DIR = os.getcwd()
TEN_MIN = 600
DEFAULT_INTERVAL = 2
GLXH_MAIN_SCENE = {"x": 345, "y": 345}
GLXH = {"x": 1530, "y": 900}
CTN = {"x": 1530, "y": 975}

scenes = { 
          'GLXH' : (1450, 890, 1610, 914), 
          'CTN' : (1450, 960, 1610, 984),
          'S' : (1784, 961, 1805, 976), 
          'ESC' : (1528, 952, 1553, 970), 
          'SPACE' : (915, 176, 1245, 241), 
          'CTN1' : (1450, 960, 1610, 984), 
          'CONFIRM' : (1450, 960, 1610, 984), 
          'ON_MATCH' : (580, 103, 591, 107)
         }


tempScenePath = os.path.join(CURRENT_DIR, 'img', 'tempScene.png')

def sceneCompare(sceneName, area):
    tempScene = Image.open(tempScenePath)
    refScene = Image.open(os.path.join(CURRENT_DIR, 'img', f'{sceneName}.png'))
    tempCropped  = tempScene.crop(area)
    refCropped  = refScene.crop(area)    
    diff = ImageChops.difference(tempCropped, refCropped)
    if diff.getbbox() is None:
        return True
    else:
        return False
                
class Camera:
    def __init__(self, interval):
        self.interval = interval
    def sceneShot(self):
        refScene = pyautogui.screenshot()
        refScene.save(tempScenePath)
    def sleep(self):    
        self.interval = TEN_MIN    

class AutoMouse:
    def startGLXHMode(self):
        pyautogui.click(GLXH_MAIN_SCENE["x"], GLXH_MAIN_SCENE["y"])

    def pressGLXH(self):
        pyautogui.click(GLXH["x"], GLXH["y"])

    def pressCTN(self):
        pyautogui.click(CTN["x"], CTN["y"])
        
    def pressKey(self, key):
        pyautogui.click(1553, 970)
        keyboard.press(key)
        return True
    

if __name__ == "__main__":
    autoMouse = AutoMouse()
    camera = Camera(DEFAULT_INTERVAL) 
       
    parser = argparse.ArgumentParser(description="Automate the game")
    parser.add_argument("--matches", type=int, default=30, help="Number of matches to process")
    args = parser.parse_args()
    
    numOfMatch = 0

    while numOfMatch < args.matches: 
        try:
            if numOfMatch == 0:
                autoMouse.startGLXHMode()
                numOfMatch += 1
                       
            camera.sceneShot()
                            
            for sceneName, area in scenes.items():
                if sceneCompare(sceneName, area):
                    if sceneName == "GLXH": 
                        autoMouse.pressGLXH()
                        continue
                    elif sceneName in ["CTN", "CTN1", "CONFIRM"]:
                        autoMouse.pressCTN()
                        continue
                    elif sceneName in ["S", "ESC", "SPACE"]:
                        isPressed = False
                        while isPressed is False:
                            isPressed = autoMouse.pressKey(sceneName.lower())
                        continue
                    elif sceneName == "ON_MATCH":
                        camera.sleep()
                        continue
                
            time.sleep(camera.interval)
            
            if(camera.interval == TEN_MIN):
                camera.interval = DEFAULT_INTERVAL

        except Exception as e:
            print("Exception:", e)

