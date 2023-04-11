from selenium import webdriver
from webpageController import WebpageController
import time

if __name__ == "__main__":
    print("hello")
    controller = WebpageController("https://www.youtube.com")
    while (True):
        command = input("command:")
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