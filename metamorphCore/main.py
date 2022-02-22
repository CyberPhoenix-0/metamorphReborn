from pynput import keyboard

def on_press(key):
    try:
        if key == "Key.enter":
            print()
            return key
        return key
    except AttributeError:
        print('special key pressed: {0}'.format(key))
        return key

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released


def main():
    key = ''
    command = ""
    sig = False
    while command != "exit" and command != "quit":
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            m = listener.join()
            print(m)


if __name__ == '__main__':
    main()