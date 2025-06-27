import json

from pynput.keyboard import Controller, Key
import time
from pynput import keyboard
import keyboard as win_kb

pressed_keys = set()

def start_listener():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    return listener


def on_press(key):
    pressed_keys.add(key)
    combo = {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char('c')}

    # Example: detect Ctrl + C
    if combo.issubset(pressed_keys):
        print("Detected: Ctrl + C")

    try:
        print(f"\nKey pressed: {key.char}")
    except AttributeError:
        print(f"\nSpecial key pressed: {key}")
    print(pressed_keys)


def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)

    if key == keyboard.Key.esc:
        print("Exiting...")
        return False

def block_keys():
    with open("config.json", "r") as f:
        config_data = json.load(f)
        for key in config_data:
            win_kb.block_key(key)

block_keys()
start_listener()

win_kb.wait('esc')


"""
keyboard = Controller()

time.sleep(2)  # Gives you 2 seconds to focus a text field

keyboard.type(" ")
keyboard.press(Key.enter)  # Press Enter
keyboard.release('\n')"""
