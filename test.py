from selenium import webdriver
from webpageController import WebpageController
import time
from gesture import GestureRecognizer
import cv2

if __name__ == "__main__":
    print("hello")
    controller = WebpageController("https://www.youtube.com")
    gesture_recognizer = GestureRecognizer()
    while (True):
        gesture_recognizer.run()
        command = gesture_recognizer.get_command()
        # command = input("command:")
        print(command)
        if ("w" == command):
            controller.palmMoveDown()
        elif ("s" == command):
            controller.palmMoveUp()
        elif ("a" == command):
            controller.palmMoveRight()
        elif ("d" == command):
            controller.palmMoveLeft()
        elif ("q" == command):
            controller.pointToLeft()
        elif ("e" == command):
            controller.pointToRight()
        elif ("x" == command):
            controller.makeFist()
        cv2.waitKey(1)
