from webpageControl import WebpageControl
from selenium.webdriver.common.by import By

class YoutubeControl(WebpageControl):
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