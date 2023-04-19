from selenium import webdriver
from webpageController import WebpageController
import time
from gesture import GestureRecognizer
import cv2

def main():
    print("hello")
    # controller = WebpageController("https://www.youtube.com")
    video_page = 'https://www.youtube.com/watch?v=PrOPRJ8K0fU&list=RDPrOPRJ8K0fU&start_radio=1'
    controller = WebpageController(video_page)
    gesture_recognizer = GestureRecognizer()
    start_time = time.time()
    while (True):
        gesture_recognizer.run()
        command = gesture_recognizer.get_command()
        gesture_recognizer.clear_gesture_cache()
        # command = input("command:")
        print(command)
        if ("scroll_up" == command):
            controller.palmMoveDown()
        elif ("scroll_down" == command):
            controller.palmMoveUp()
        elif ("a" == command):
            controller.palmMoveRight()
        elif ("d" == command):
            controller.palmMoveLeft()
        elif ("pause" == command):
            if time.time() - start_time > 1:
                controller.makeFist()
                start_time = time.time()
        elif ("play" == command):
            if time.time() - start_time > 1:
                controller.makeFist()
                start_time = time.time()
            controller.makeFist()
        elif ("x" == command):
            controller.makeFist()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()