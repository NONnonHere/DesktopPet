import sys
import threading
import random
import psutil
import pygetwindow as gw
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot, QTimer
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

class Backend(QObject):
    stateChanged = Signal(str)
    cpuUpdated = Signal(float)
    movePet = Signal(int, int)
    requestPosition = Signal()
    isMoving = Signal(bool)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_system)
        self.timer.start(1000)

        self.home_x = 100
        self.home_y = 100
        self.screen_width = 1920
        self.screen_height = 1080
        self.is_roaming = False
        self.is_dragging = False

    def update_screen_size(self):
        screen = QGuiApplication.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()

    @Slot(int, int)
    def set_home_location(self, x, y):
        self.home_x = x
        self.home_y = y
        print(f"New Home Set: {x}, {y}")

  
    @Slot()
    def start_drag(self):
        self.is_dragging = True 
        self.isMoving.emit(False) 
        print("Dragging started - Logic paused")

    @Slot()
    def end_drag(self):
        self.is_dragging = False
        print("Dragging ended - Logic resumed")

    def check_system(self):
       
        if self.is_dragging:
            return

        self.update_screen_size()
        
      
        try:
            cpu = psutil.cpu_percent()
            if cpu > 80:
                self.stateChanged.emit("stressed")
                return
        except: pass


        state = "idle"
        try:
            window = gw.getActiveWindow()
            if window:
                title = window.title.lower()
                
                if "focuspet" in title:
                    pass 
                elif 'code' in title or 'visual studio' in title or title.endswith('.py'):
                    state = "coding"
                elif 'spotify' in title or 'music' in title:
                    state = "music"
                elif 'browser' in title or 'chrome' in title or 'brave' in title:
                    state = "browse"
                elif 'SOLIDWORKS' in title or 'fusion' in title or 'Part1' in title:
                    state = 'Design'
        except: pass

        self.stateChanged.emit(state)

        if state in ["coding", "browse", "stressed"]:

            self.movePet.emit(self.home_x, self.home_y)
            self.isMoving.emit(True)
            self.is_roaming = False
    
        elif state == "idle":
            if random.random() < 0.1: 

                new_x = random.randint(0, self.screen_width - 200)
                new_y = random.randint(0, self.screen_height - 200)
                self.movePet.emit(new_x, new_y)
                self.isMoving.emit(True)
                self.is_roaming = True
            elif self.is_roaming:

                pass
            else:
                self.isMoving.emit(False)


def create_image():
    width = 64
    height = 64
    color1 = "blue"
    color2 = "white"
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return image

def setup_tray(app_instance, backend_ref):
    def set_home_action(icon, item):
        backend_ref.requestPosition.emit()

    def quit_app(icon, item):
        icon.stop()
        app_instance.quit()

    menu = (item('Set Home Here', set_home_action), item('Exit', quit_app))
    icon = pystray.Icon("FocusPet", create_image(), "FocusPet", menu)
    icon.run()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    engine = QQmlApplicationEngine()
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)
    engine.load("main.qml")
    if not engine.rootObjects(): sys.exit(-1)
    tray_thread = threading.Thread(target=setup_tray, args=(app, backend), daemon=True)
    tray_thread.start()
    sys.exit(app.exec())