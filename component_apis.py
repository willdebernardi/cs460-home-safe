from passlib.hash import pbkdf2_sha256 as encrypt

class Door:
    def __init__(self):
        self.open = False
        self.locked = True
        
    def lock(self):
        if(not self.open): # Only lock when the door is closed 
            self.locked = True
        
    def unlock(self):
        self.locked = False
        
    # def open_door(self):
    #     return self.open
    
    # def locked_door(self):
    #     return self.locked
    
    
class Timer:
    def __init__(self):
        self.root = None
        self.ID = None
        
    def set_time(self, s, timeout_func, *args):
        if(self.ID != None):
            self.root.after_cancel(self.ID)
        self.ID = self.root.after(s * 1000, timeout_func)
        
    def reset(self):
        self.root.after_cancel(self.ID)
    
    
class SafeCode:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.pwd = encrypt.hash("0000")
    
    def test(self, pin):
        return encrypt.verify(pin, self.pwd)
    
    def set_code(self, pin):
        if len(pin) > 4:
            raise AttributeError("PIN too long") 
        if len(pin) < 1:
            raise AttributeError("PIN to short")
        self.pwd = encrypt.hash(pin)
        
        
    
# def notifications():