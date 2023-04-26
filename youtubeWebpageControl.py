from abstractWebpageControl import AbstractWebpageControl
from selenium.webdriver.common.by import By

class YoutubeWebpageControl(AbstractWebpageControl):
    webdriver = None

    def __init__(self, webdriver) -> None:
        self.webdriver = webdriver
        self.zoom = 100
        
    def scrollUp(self):
        self.webdriver.execute_script("window.scrollBy(0,-500)")

    def scrollDown(self):
        self.webdriver.execute_script("window.scrollBy(0,500)")

    def moveForward(self):
        self.webdriver.forward()

    def moveBack(self):
        self.webdriver.back()

    def next(self):
        try:
            nextButton = self.webdriver.find_element(By.XPATH, "//a[@class='ytp-next-button ytp-button']")
            nextButton.click()
        except:
            print("nextButton not found")

    def prev(self):
        try:
            prevButton = self.webdriver.find_element(By.XPATH, "//a[@class='ytp-prev-button ytp-button']")
            prevButton.click()
        except:
            print("prevButton not found")

    def playOrPause(self):
        try:
            playButton = self.webdriver.find_element(By.XPATH, "//button[contains(@class, 'ytp-play-button ytp-button')]")
            playButton.click()
        except:
            print("playButton not found")
            
    def zoomIn(self):
        # increase zoom by 20%
        if self.zoom >= 200:
            return
        self.zoom += 20
        self.webdriver.execute_script("document.body.style.zoom='{}%'".format(self.zoom))

    def zoomOut(self):
        if self.zoom <= 20:
            return
        self.zoom -= 20
        self.webdriver.execute_script("document.body.style.zoom='{}%'".format(self.zoom))