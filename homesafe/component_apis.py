from passlib.hash import pbkdf2_sha256 as encrypt
import threading

class Door:
    def __init__(self):
        self.open = False
        self.locked = True
        
    def lock(self):
        if(not self.open): # Only lock when the door is closed 
            self.locked = True
        
    def unlock(self):
        self.locked = False
        
    def open_door(self):
        return self.open
    
    def locked_door(self):
        return self.locked
    
    
class Timer:
    def __init__(self):
        self.timer = None
        
    def set_time(self, s, timeout_func, *args):
        if(self.timer != None):
            self.timer.cancel()
        self.timer = threading.Timer(s, timeout_func, args)
        self.timer.start()
        
    def reset(self):
        self.timer.cancel()
    
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