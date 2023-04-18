from selenium import webdriver
from abstractWebpageControl import AbstractWebpageControl
from genericWebpageControl import GenericWebpageControl
from youtubeWebpageControl import YoutubeWebpageControl

PATH = "../chromedriver/chromedriver"

class WebageControlFactory():

    def create(url: str) -> AbstractWebpageControl:
        driver = webdriver.Chrome(PATH)
        driver.get(url)
        if ".youtube." in url:
            return YoutubeWebpageControl(driver)
        elif ".tiktok." in url:
            pass
        elif ".spotify." in url:
            pass
        else:
            pass