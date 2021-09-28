import tkinter as tk
from component_apis import *
from tkinter.constants import END
from playsound import playsound

btn_list = [
    '1', '2', '3',
    '4', '5', '6',
    '7', '8', '9', 
    'Del', '0', '#'
]
class Safe:
    def __init__(self):
        self.timer = Timer()
        self.door = Door()
        self.code = SafeCode()
        self.code_change_requested = False

entry_box = ""
safe_state = ""
door_state = ""
pin = ""
safe = Safe()

def key_entry_timeout():
    print("Key entry timeout called")
    global pin 
    
    pin = ""
    entryFailure()
    update_states()
    
def safe_unlocked_timeout():
    print("Safe unlocked timeout called")
    global safe
    
    safe.door.lock()
    safeLocked()
    entryFailure()
    update_states()
    
def code_change_timeout():
    global pin, safe
    safe.timer.set_time(60, safe_unlocked_timeout)
    pin = ""
    entryFailure()
    update_states()
    

def handle_input(val):
    global pin, safe
    
    # Resetting passcode
    if(safe.code_change_requested):
        if(val.isnumeric()):
            pin += val
            safe.timer.set_time(5, code_change_timeout)
            if(len(pin) > 3):
                safe.code.set_code(pin)
                safe.timer.set_time(60, safe_unlocked_timeout)
                pin = ""
                entrySuccess()
                safe.code_change_requested = False
            return
        else:
            code_change_timeout()
            safe.code_change_requested = False
            return
        
    # Allows password reset when the door is closed and safe unlocked
    if(not safe.door.locked and not safe.door.open):
        if(val == "#"): # Password reset key
            pin = ""
            safe.timer.set_time(5, code_change_timeout)
            safe.code_change_requested = True
            return
        else: # Ignore other keys
            entryFailure()
            return 
    
        
    safe.timer.set_time(5, key_entry_timeout)
    # Normal entry when safe is locked
    if(val.isnumeric()):
        pin += val
        print(pin)
        if(len(pin) == 4):
            if(safe.code.test(pin)):
                pin = ""
                entrySuccess()
                safe.door.unlock()
                safe.timer.set_time(60, safe_unlocked_timeout)
                update_states()
            else:
                print("Entry failed")
                safe.timer.reset()
                pin = ""
                entryFailure()
                update_states()
    else:
        key_entry_timeout()
    
    
def update_states():
    global safe_state, door_state
    
    lock_state_text = "LOCKED" if safe.door.locked else "UNLOCKED"
    door_state_text = "OPEN" if safe.door.open else "CLOSED"
        
    safe_state.set(f"Safe is {lock_state_text}")
    door_state.set(f"Door is {door_state_text}")

def create_numpad(container):
    frame = tk.Frame(container)

    r = 1
    c = 0
    for b in btn_list:
        cmd = lambda button=b: handle_input(button)
        b = tk.Button(frame, text=b, width=10, command=cmd).grid(row=r, column=c)
        c += 1
        if c > 2:
            c = 0
            r += 1

    return frame

def main():
    global safe_state, door_state, pin
    

    root = tk.Tk()
    root.title=("Safe")
    safe.timer.root = root
    # root.geometry("800x600")
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=1)

    keypad_frame = create_numpad(root)
    keypad_frame.grid(column=0, row =0)


    # Creates LED panel
    led_frame = tk.Frame(root)
    tk.Label(led_frame, text="LED: ").grid(column=0, row=0)
    led_state = tk.Canvas(led_frame, bg="green", height=15, width= 15)
    led_state.grid(column=1, row=0)
    led_frame.grid(column=0, row=1)

    # Create Testing panel
    def check_led():
        if(led_state['bg'] == "red"):
            led_state.configure(bg="green")
        else:
            led_state.configure(bg="red")

    def handle_door():
        if(safe.door.open == False and not safe.door.locked):
            safe.door.open = True
        elif safe.door.open and not safe.door.locked:
            safe.door.locked = True
            safe.door.open = False
            safeLocked()
            entrySuccess()
        else:
            safe.door.open = False
        update_states();

    testing_frame = tk.Frame(root)
    tk.Label(testing_frame, text="Testing Panel").grid(column=0, row=0)
    tk.Checkbutton(testing_frame, text="Low-Power", command=check_led).grid(column=0, row=1)
    tk.Button(testing_frame,text="Open/Close Door", command=handle_door).grid(column=0, row=2)
    testing_frame.grid(column=1, row=0)

    safe_state = tk.StringVar();
    safe_state.set("Safe is LOCKED")
    tk.Label(root, textvariable=safe_state).grid(column=0, row=3)

    door_state = tk.StringVar();
    door_state.set("Door is CLOSED")
    tk.Label(root, textvariable=door_state).grid(column=0, row=4)




    
    root.mainloop()
    

def entrySuccess():
    print("entry success called")
    playsound("beep.wav")
    return
def entryFailure():
    for _ in range(3):
        playsound("beep.wav")
    return
def batteryLow():
    return
def batteryFine():
    return
def safeUnlocked():
    print("safe unlocked notification called")
    return
def safeLocked():
    return

main()
