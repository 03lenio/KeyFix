import json
import msvcrt
import os.path
import time
from json import JSONDecodeError

from pynput import keyboard

pressed_keys = set()


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def start_listener():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    return listener


def register_issues():
    print("Please press and hold until the process is done the key that you need fixed:")
    listener = start_listener()
    while listener.is_alive():
        if len(pressed_keys) != 0:
            time.sleep(0.1)
            listener.stop()
    keys_as_string = ""
    for key in pressed_keys:
        try:
            keys_as_string += key.char + ","
        except AttributeError:
            keys_as_string += str(key).replace("Key.", "") + ","
    print(f"\nThanks! The keys that actually were fired seem to be: {keys_as_string}")
    flush_input()
    confirm = input("Do you want to rebind this key/combination to a different input? [y/n]\n> ")
    if confirm.lower().startswith('y'):
        return pressed_keys
    else:
        print(confirm)
        print("Fine but don't ask me for help again!")


def rebind_keys(keys: set):
    keys_as_string = ""
    keys_config_format = ""
    for key in pressed_keys:
        try:
            keys_as_string += key.char + "+"
        except AttributeError:
            keys_as_string += str(key).replace("Key.", "") + "+"
    keys_as_string = keys_as_string.strip("+")
    flush_input()
    target_key = input("Please enter the key that should be fired instead in plain text\n")
    confirm = input(f"You chose {target_key}! Is this key correct? [y/n]\n> ")
    if confirm.lower().startswith('y'):
        if not os.path.exists("config.json"):
            open("config.json", "w").write("{}")
        with open("config.json", "r+") as config_file:
            try:
                config_data = json.load(config_file)
                print(config_data)
            except JSONDecodeError:
                print("unsupported operation")
                config_data = {}
            config_data[keys_as_string] = target_key
            config_file.seek(0)
            config_file.truncate()
            config_file.write(json.dumps(config_data, indent=2))
    else:
        rebind_keys(keys)


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


keys_to_fix = register_issues()
rebind_keys(keys_to_fix)