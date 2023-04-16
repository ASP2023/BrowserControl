from abstractWebpageControl import AbstractWebpageControl
from selenium.webdriver.common.by import By

class GenericWebpageControl(AbstractWebpageControl):
    webdriver = None

    def __init__(self, webdriver) -> None:
        self.webdriver = webdriver

    def scrollUp(self):
        self.webdriver.execute_script("window.scrollBy(0,-500)")

    def scrollDown(self):
        self.webdriver.execute_script("window.scrollBy(0,500)")

    def moveForward(self):
        self.webdriver.forward()

    def moveBack(self):
        self.webdriver.back()

    def next(self):
        pass

    def prev(self):
        pass

    def playOrPause(self):
        pass