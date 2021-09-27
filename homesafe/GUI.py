import tkinter as tk
from tkinter.constants import END

btn_list = [
    '1', '2', '3',
    '4', '5', '6',
    '7', '8', '9', 
    'Del', '0', '*'
]

entry_box = ""
safe_state = ""
door_state = ""

def handle_input(val):
    global entry_box, safe_state
    entry_box.insert(END, val)

    if(len(entry_box.get()) == 4):
        print("code entered")
        # HANDLE ENTRY LOGIC HERE
        safe_state.set("Safe is UNLOCKED")
        door_state.set("Door is OPEN")

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
    global safe_state, door_state

    root = tk.Tk()
    root.title=("Safe")
    root.geometry("800x600")
    root.columnconfigure(0, weight=1)
    # root.rowconfigure(0)
    # root.rowconfigure(1)
    # root.rowconfigure(2)

    entry_frame = create_entry(root)
    entry_frame.grid(column=0, row= 0)

    keypad_frame = create_numpad(root)
    keypad_frame.grid(column=0, row =1)

    safe_state = tk.StringVar();
    safe_state.set("Safe is LOCKED")
    tk.Label(root, textvariable=safe_state).grid(column=0, row=2)

    door_state = tk.StringVar();
    door_state.set("Door is CLOSED")
    tk.Label(root, textvariable=door_state).grid(column=0, row=3)


    
    root.mainloop()

main()
