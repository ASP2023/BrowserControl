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
        if ("scroll_up" == command):
            controller.palmMoveDown()
        elif ("scroll_down" == command):
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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
