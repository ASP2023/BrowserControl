from selenium import webdriver
from webpageController import WebpageController
import time

PATH = "./chromedriver/chromedriver"

def ___main___():
    controller = WebpageController(PATH)
    controller.palmMoveUp()