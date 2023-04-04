import time
import random

import pyautogui

if __name__ == '__main__':
    for i in range(20):
        time.sleep(60 * 10)  # every 10th minute make a move
        x = random.randrange(1000)
        y = random.randrange(1000)
        pyautogui.moveTo(x, y, duration=1)
