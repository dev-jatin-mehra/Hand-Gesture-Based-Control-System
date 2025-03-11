from pynput.keyboard import Controller

keyboard = Controller()

def press_key(key):
    """Presses and holds a key."""
    keyboard.press(key)

def release_keys(keys):
    """Releases all keys that are not active."""
    for key in keys:
        keyboard.release(key)
