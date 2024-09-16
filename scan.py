import keyboard

def print_event(e):
    print(e)

keyboard.hook(print_event)
keyboard.wait('esc')  # Use the escape key or another key to stop the script
