import tkinter as tk
from component_apis import *
from tkinter.constants import END

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
    
    if(safe.code_change_requested):
        if(val.isnumeric()):
            pin += val
            safe.timer.set_time(5, code_change_timeout)
            if(len(pin) > 3):
                safe.code.set_code(pin)
                safe.timer.set_time(5, safe_unlocked_timeout)
                pin = ""
                entrySuccess()
                safe.code_change_requested = False
            return
        else:
            code_change_timeout()
            safe.code_change_requested = False
            return
        
    
    if(not safe.door.locked):
        if(val == "#"):
            pin = ""
            safe.timer.set_time(5, code_change_timeout)
            safe.code_change_requested = True
            return
        else:
            entryFailure()
            return 
    
        
    safe.timer.set_time(200, key_entry_timeout)
    if(val.isnumeric()):
        pin += val
        print(pin)
        if(len(pin) == 4):
            if(safe.code.test(pin)):
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
    
    lock_state_text = "Locked" if safe.door.locked else "Unlocked"
    door_state_text = "Open" if safe.door.open else "Closed"
        
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

def create_entry(container):
    global entry_box

    frame = tk.Frame(container)
    entry_box = tk.Entry(frame, width=30)
    entry_box.grid(column=0, row=0)

    return frame

def main():
    global safe_state, door_state, pin
    
    # safe = Safe()

    root = tk.Tk()
    root.title=("Safe")
    root.geometry("800x600")
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=1)

    entry_frame = create_entry(root)
    entry_frame.grid(column=0, row= 0)

    keypad_frame = create_numpad(root)
    keypad_frame.grid(column=0, row =1)


    # Creates LED panel
    led_frame = tk.Frame(root)
    tk.Label(led_frame, text="LED: ").grid(column=0, row=0)
    led_state = tk.Canvas(led_frame, bg="green", height=15, width= 15)
    led_state.grid(column=1, row=0)
    led_frame.grid(column=0, row=2)

    # Create Testing panel
    def check_led():
        if(led_state['bg'] == "red"):
            led_state.configure(bg="green")
        else:
            led_state.configure(bg="red")

    testing_frame = tk.Frame(root)
    tk.Label(testing_frame, text="Testing Panel").grid(column=0, row=0)
    tk.Checkbutton(testing_frame, text="Low-Power", command=check_led).grid(column=0, row=1)
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
    return
def entryFailure():
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
