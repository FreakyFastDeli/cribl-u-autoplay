import time
from mss import mss
from PIL import Image, ImageChops
import numpy as np
import pyautogui
from pynput.keyboard import Key, Listener

# Screen capture region coordinates
x, y, width, height = 0, 1035, 40, 35  # Monitor mode

autoplay_enabled = False  # Initial state of autoplay
pressed_keys = set()      # To track the keys currently pressed

def capture_screen(region):
    with mss() as sct:
        screenshot = sct.grab(region)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img

def images_are_different(img1, img2):
    if img1 is None or img2 is None:
        return True
    diff = ImageChops.difference(img1, img2)
    return np.array(diff).sum() > 20  # Adjust threshold as needed

def on_press(key):
    global autoplay_enabled
    pressed_keys.add(key)
    # Check if the combination ctrl + alt + cmd is pressed.
    # Depending on your system, there might be left/right variants so we include them.
    ctrl_pressed = any(k in pressed_keys for k in [Key.ctrl, Key.ctrl_l, Key.ctrl_r])
    alt_pressed = any(k in pressed_keys for k in [Key.alt, Key.alt_l, Key.alt_r])
    cmd_pressed = any(k in pressed_keys for k in [Key.cmd, Key.cmd_l, Key.cmd_r])
    if ctrl_pressed and alt_pressed and cmd_pressed:
        autoplay_enabled = not autoplay_enabled
        print(f"Autoplay Enabled: {autoplay_enabled}")

def on_release(key):
    try:
        pressed_keys.remove(key)
    except KeyError:
        pass

# Start the listener for key presses
listener = Listener(on_press=on_press, on_release=on_release)
listener.start()

region = {"top": y, "left": x, "width": width, "height": height}
print("Capturing base image in 5 seconds")
time.sleep(5)
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
    time.sleep(1)  # Adjust timing as necessary
