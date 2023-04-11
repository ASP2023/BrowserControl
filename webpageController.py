from selenium import webdriver
from webpageControl import WebpageControl
from youtubeControl import YoutubeControl

PATH = "./chromedriver/chromedriver"

class WebpageController():

    url: str = None
    driver = None
    webpageControl: WebpageControl = None

    def __init__(self, url: str) -> None:
        self.url = url
        self.driver = webdriver.Chrome(PATH)
        self.driver.get(url)
        self.webpageControl = YoutubeControl(self.driver)

    def palmMoveUp(self):
        self.webpageControl.scrollDown()

    def palmMoveDown(self):
        self.webpageControl.scrollUp()

    def palmMoveLeft(self):
        self.webpageControl.moveForward()

    def palmMoveRight(self):
        self.webpageControl.moveBack()

    def pointToLeft(self):
        self.webpageControl.prev()

    def pointToRight(self):
        self.webpageControl.next()

    def makeFist(self):
        self.webpageControl.playOrPause()
