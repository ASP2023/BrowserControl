from selenium import webdriver
from webpageController import WebpageController
from PDFpageControl import PDFPageControl
import time
from gesture import GestureRecognizer
import cv2

if __name__ == "__main__":
    print("hello")
    PATH = "../chromedriver/chromedriver"
    driver = webdriver.Chrome(PATH)
    # pdf_path = 'docs/gpt-4.pdf'
    # url = pdf_path
    # url = f'file:///{pdf_path}'
    url = 'arxiv.org/pdf/2303.08774.pdf'
    # url = "https://www.youtube.com"
    driver.get(url)
    controller = PDFPageControl(driver)
    gesture_recognizer = GestureRecognizer()
    while (True):
        gesture_recognizer.run()
        command = gesture_recognizer.get_command()
        gesture_recognizer.clear_gesture_cache()
        # command = input("command:")
        print(command)
        if command == 'quick_scorll_up':
            controller.quickSCrollUp()
        elif command == 'quick_scorll_down':
            controller.quickSCrollDown()
        elif command == 'scroll_up':
            controller.scrollUp()
        elif command == 'scroll_down':
            controller.scrollDown()
        elif command == 'slow_scoll_up':
            controller.slowScrollUp()
        elif command == 'slow_scoll_down':
            controller.slowScrollDown()
        elif command == 'zoom_in':
            controller.zoomIn()
        elif command == 'zoom_out':
            controller.zoomOut()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        