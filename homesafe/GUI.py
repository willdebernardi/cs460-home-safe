import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry("800x600")

    numpad = NumPad(root)
    root.mainloop()

btn_list = [
    '7', '8', '9',
    '4', '5', '6',
    '1', '2', '3', 
    'Del', '0', '*'
]

class NumPad(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.grid()
        self.numpad_create()

    def handle_input(self):
        print(self)

    def numpad_create(self):
        r = 1
        c = 0
        for b in btn_list:
            cmd = lambda button=b: print(button)
            self.b = tk.Button(self, text=b, width=10, command=cmd).grid(row=r, column=c)
            c += 1
            if c > 2:
                c = 0
                r += 1

    

main()
