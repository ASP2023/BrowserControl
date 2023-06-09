from selenium import webdriver
from webpageController import WebpageController
import time
from gesture import GestureRecognizer
import cv2
# import pygetwindow as gw
import pyautogui


# def move_and_resize_window(title, x, y, width, height):
#     try:
#         window = gw.getWindowsWithTitle(title)[0]
#         window.moveTo(x, y)
#         window.resizeTo(width, height)
#     except IndexError:
#         print(f'Window with title "{title}" not found.')


def main():
    print("hello")
    gesture_recognizer = GestureRecognizer()
    # initilize camera first
    gesture_recognizer.run()    
    # controller = WebpageController("https://www.youtube.com")
    video_page = (
        "https://www.youtube.com/watch?v=PrOPRJ8K0fU&list=RDPrOPRJ8K0fU&start_radio=1"
    )
    controller = WebpageController(video_page)
    start_time = time.time()
    while True:
        gesture_recognizer.run()
        command = gesture_recognizer.get_command()
        # controller.volumeDown()
        # controller.makeFist()
        print(command)
        gesture_recognizer.clear_gesture_cache()
        # command = input("command:")
        if "w" == command:
            controller.palmMoveDown()
        elif "s" == command:
            controller.palmMoveUp()
        elif "a" == command:
            continue
            # controller.palmMoveRight()
        elif "d" == command:
            continue
            # controller.palmMoveLeft()
        elif "pause" == command:
            if time.time() - start_time > 1:
                controller.makeFist()
                start_time = time.time()
        elif "play" == command:
            if time.time() - start_time > 1:
                controller.makeFist()
                start_time = time.time()
        elif "playorpause" == command:
            if time.time() - start_time > 1:
                controller.makeFist()
                start_time = time.time()
        elif "x" == command:
            controller.makeFist()
        # Zoom In and Zoom Out: TBD
        elif "zoom_in" == command:
            controller.zoomIn()
        elif "zoom_out" == command:
            controller.zoomOut()
        elif "reset_zoom" == command:
            controller.resetZoom()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

if __name__ == "__main__":
    main()
