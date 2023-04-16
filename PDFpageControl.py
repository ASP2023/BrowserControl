from abstractWebpageControl import AbstractWebpageControl
from selenium.webdriver.common.by import By

class PDFPageControl():
    webdriver = None

    def __init__(self, webdriver) -> None:
        self.webdriver = webdriver

    def scrollUp(self):
        self.webdriver.execute_script("window.scrollBy(0,-500)")

    def scrollDown(self):
        self.webdriver.execute_script("window.scrollBy(0,500)")

    def quickSCrollUp(self):
        self.webdriver.execute_script("window.scrollBy(0,-1000)")

    def quickScrollDown(self):
        self.webdriver.execute_script("window.scrollBy(0,1000)")

    def slowScrollUp(self):
        self.webdriver.execute_script("window.scrollBy(0,-100)")

    def slowScrollDown(self):
        self.webdriver.execute_script("window.scrollBy(0,100)")

    def zoomIn(self):
        self.webdriver.execute_script("document.body.style.zoom = '150%'")

    def zoomOut(self):
        self.webdriver.execute_script("document.body.style.zoom = '50%'")