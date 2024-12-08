import keyboard
import time

start_time = time.time()

# Countdown
for i in range(5, 0, -1):
    print(i)
    time.sleep(1)

detected_keys = {'w': 0, 'a': 0, 's': 0, 'd': 0, }

# Key Detection Loop
while time.time() - start_time < 10:
    try:
        if keyboard.is_pressed('w'):
            detected_keys['w'] = 1
        else:
            detected_keys['w'] = 0

        if keyboard.is_pressed('a'):
            detected_keys['a'] = 1
        else:
            detected_keys['a'] = 0

        if keyboard.is_pressed('s'):
            detected_keys['s'] = 1
        else:
            detected_keys['s'] = 0

        if keyboard.is_pressed('d'):
            detected_keys['d'] = 1
        else:
            detected_keys['d'] = 0

        print(detected_keys)
        time.sleep(0.05)
        
    except:
        break


# Shows that script is finished
print("END OF SCRIPT")







# Original
##import win32api as wapi
##import time
##
##keyList = ["\b"]
##for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
##    keyList.append(char)
##
##def key_check():
##    keys = []
##    for key in keyList:
##        if wapi.GetAsyncKeyState(ord(key)):
##            keys.append(key)
##    return keys
