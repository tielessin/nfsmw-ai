import keyboard
import time


# Countdown
def countdown():
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)


# Key Detection
def key_check():

    detected_keys = [0, 0, 0, 0] # [W, A, S, D]
    
    try:
        if keyboard.is_pressed('w'):
            detected_keys[0] = 1
        else:
            detected_keys[0] = 0

        if keyboard.is_pressed('a'):
            detected_keys[1] = 1
        else:
            detected_keys[1] = 0

        if keyboard.is_pressed('s'):
            detected_keys[2] = 1
        else:
            detected_keys[2] = 0

        if keyboard.is_pressed('d'):
            detected_keys[3] = 1
        else:
            detected_keys[3] = 0
    except:
        print("We shouldn't be here, my friend...")
    
    return detected_keys


def key_check_with_nitro():

    detected_keys = [0, 0, 0, 0, 0] # [W, A, S, D, shift]
    
    try:
        if keyboard.is_pressed('w'):
            detected_keys[0] = 1
        else:
            detected_keys[0] = 0

        if keyboard.is_pressed('a'):
            detected_keys[1] = 1
        else:
            detected_keys[1] = 0

        if keyboard.is_pressed('s'):
            detected_keys[2] = 1
        else:
            detected_keys[2] = 0

        if keyboard.is_pressed('d'):
            detected_keys[3] = 1
        else:
            detected_keys[3] = 0

        if keyboard.is_pressed('shift'):
            detected_keys[4] = 1
        else:
            detected_keys[4] = 0

    except:
        print("We shouldn't be here, my friend...")
    
    return detected_keys



def key_check_loop():
    countdown()
    while True:
        print(key_check())
        if keyboard.is_pressed('q'):
            break
    print("Keycheck Stopped")
    print("END OF SCRIPT")




