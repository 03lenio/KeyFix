import json

import time
import keyboard as win_kb


def handle_remap_combination(input_keys, target_key):
    for input_key in input_keys:
        win_kb.block_key(input_key)
    win_kb.press_and_release(target_key)
    time.sleep(5)
    for input_key in input_keys:
        win_kb.unblock_key(input_key)


def handle_remap(input_key, target_key):
    win_kb.block_key(input_key)
    win_kb.press_and_release(target_key)
    time.sleep(5)
    win_kb.unblock_key(input_key)


def manage_keys(p_config: dict):
    for key in p_config:
        if "+" in key:
            print("dead ass")
            win_kb.add_hotkey(key, lambda: handle_remap_combination(key.split("+"), p_config[key]))
        else:
            print("single mingle")
            win_kb.add_hotkey(key, lambda: handle_remap(key, p_config[key]))


def load_config():
    with open('config.json', "r") as config_file:
        local_config = json.load(config_file)
        return local_config



manage_keys(load_config())

win_kb.wait('esc')


"""
keyboard = Controller()

time.sleep(2)  # Gives you 2 seconds to focus a text field

keyboard.type(" ")
keyboard.press(Key.enter)  # Press Enter
keyboard.release('\n')"""
