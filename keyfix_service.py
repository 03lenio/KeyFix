import json
import time
from pynput import keyboard
from pynput.keyboard import Controller, Key
import keyboard as win_kb

pressed_keys = set()
handled_keys = set()
virtual_keyboard = Controller()

def load_config():
    with open("config.json", "r") as config_file:
        return json.load(config_file)


config = load_config()

def sanitize_key(key):
    try:
        return key.char
    except AttributeError:
        return str(key).replace("Key.", "")

def on_press(key):
    sanitized = sanitize_key(key)
    if sanitized is None:
        return
    if sanitized in handled_keys:
        return  # Ignore repeated key-down events, this also dramatically slows down typing speed, need to improve

    pressed_keys.add(sanitized)
    handled_keys.add(sanitized)
    sanitized_parts = set(sanitized.split("+"))
    if any(sanitized_parts.issubset(set(key.split("+"))) for key in config) and len(pressed_keys) != 1:
        win_kb.block_key(sanitized)
        print(f"Blocked: {sanitized}")


    # Single key
    if sanitized in config and "+" not in sanitized:
        virtual_keyboard.type(config[sanitized])
        return

    # Combo check
    for combo_str, output in config.items():
        combo = combo_str.split("+")
        if set(combo) == pressed_keys:
            win_kb.press_and_release(output)
        else:
            print(combo)
            print(pressed_keys)

def on_release(key):
    sanitized = sanitize_key(key)
    pressed_keys.discard(sanitized)
    handled_keys.discard(sanitized)

def start_listener():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    return listener

def block_all_configured_keys():
    for key_combo in config:
        for key in key_combo.split("+"):
            try:
                win_kb.block_key(key)
            except ValueError:
                pass


block_all_configured_keys()
start_listener()
win_kb.wait('esc')
