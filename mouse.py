import pyautogui
import time
import random

start_time = time.time()
while True:
    # every 0.5 seconds, move mouse to a random location
    if time.time() - start_time > 0.5:
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
        pyautogui.moveTo(x, y)
        start_time = time.time()