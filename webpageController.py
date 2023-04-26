from selenium import webdriver
from abstractWebpageControl import AbstractWebpageControl
from youtubeWebpageControl import YoutubeWebpageControl
from webpageControlFactory import WebageControlFactory

class WebpageController():

    url: str = None
    webpageControl: AbstractWebpageControl = None

    def __init__(self, url: str) -> None:
        self.url = url
        self.webpageControl = WebageControlFactory.create(url)

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

    def zoomIn(self):
        self.webpageControl.zoomIn()
    
    def zoomOut(self):
        self.webpageControl.zoomOut()
    
    def resetZoom(self):
        self.webpageControl.resetZoom()
        
    def volumeUp(self):
        self.webpageControl.volumeUp()
    
    def volumeDown(self):
        self.webpageControl.volumeDown()