import time
from mss import mss
from PIL import Image, ImageChops
import numpy as np
import pyautogui
import keyboard  # for listening to key presses


# 
#   activate the venv with `source venv/bin/activate`
#   program needs to be run with `sudo` to capture the screen
# 



# Screen capture region coordinates
# x, y, width, height = 0, 520, 40, 35  # Small mode
x, y, width, height = 0, 790, 40, 35 # Large mode


autoplay_enabled = False  # Initial state of autoplay

def capture_screen(region):
    with mss() as sct:
        screenshot = sct.grab(region)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img

def images_are_different(img1, img2):
    if img1 is None or img2 is None:
        return True
    diff = ImageChops.difference(img1, img2)
    return np.array(diff).sum() > 20  # how different the images are, no idea how "difference" is calculated

def toggle_autoplay(e):
    global autoplay_enabled
    autoplay_enabled = not autoplay_enabled
    print(f"Autoplay Enabled: {autoplay_enabled}")

# Set up a listener for the toggle key
keyboard.on_press_key(50, toggle_autoplay) 

region = {"top": y, "left": x, "width": width, "height": height}
print("Capturing base image in 10 seconds")
time.sleep(10)
playing_img = capture_screen(region)
print("Base image captured")

while True:
    if autoplay_enabled:
        print("Capturing")
        time.sleep(0.25)
        current_img = capture_screen(region)
        if images_are_different(playing_img, current_img):
            print("Change detected, simulating hotkey")
            pyautogui.hotkey('ctrl', 'alt', '.')
            time.sleep(5)
        else:
            print("No significant change detected.")
    else:
        print("Autoplay is currently disabled.")
        while not autoplay_enabled:
            time.sleep(1)
         

    time.sleep(1)  # Adjust based on timing
