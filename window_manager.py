
class WindowsManager:
    def __init__(self):
        self.windows={}

    def add(self,name,window):
        self.windows[name]=window

    def get_window(self,name):
        return self.windows[name]
