from webpageControl import WebpageControl

class YoutubeControl(WebpageControl):
    webdriver = None

    def __init__(self, webdriver: webdriver) -> None:
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
        nextButton = self.webdriver.find_element_by_class_name("ytp-next-button ytp-button")
        if (nextButton):
            nextButton.click()
        else:
            print("nextButton not found")

    def prev(self):
        prevButton = self.webdriver.find_element_by_class_name("ytp-prev-button ytp-button")
        if (prevButton):
            prevButton.click()
        else:
            print("nextButton not found")

    def pause(self):
        pass