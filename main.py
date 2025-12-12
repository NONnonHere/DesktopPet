import sys
import threading
import time
import psutil
import pygetwindow as gw
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, QTimer, Qt
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

class Backend(QObject):
    
    stateChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_system)
        self.timer.start(1000)

    def check_system(self):
        # 1. Check Hardware (Stressed?)
        try:
            cpu = psutil.cpu_percent()
            if cpu > 80:
                self.stateChanged.emit("stressed")
                return
        except:
            pass # Ignore psutil errors if any

        # 2. Check Active Window
        try:
            window = gw.getActiveWindow()
            if window:
                title = window.title.lower()
                if 'code' in title or 'py' in title or '':
                    self.stateChanged.emit("coding")
                elif 'spotify' in title or 'music' in title:
                    self.stateChanged.emit("music")
                elif 'browser' in title or 'brave' in title or 'chrome' in title:
                    self.stateChanged.emit("browse")
                else:
                    self.stateChanged.emit("idle")
            else:
                self.stateChanged.emit("idle")
        except:
            self.stateChanged.emit("idle")

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

def setup_tray(app_instance):
    def quit_app(icon, item):
        icon.stop() 
        #Stop the PySide6 Application (Thread-safe quit)
        app_instance.quit()

    
    menu = (
        item('Show/Hide', lambda icon, item: print("Toggle Visibility Code Here")),
        item('Exit FocusPet', quit_app)
    )

    
    icon = pystray.Icon("FocusPet", create_image(), "FocusPet", menu)
    icon.run()


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    engine = QQmlApplicationEngine()
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)
    

    tray_thread = threading.Thread(target=setup_tray, args=(app,), daemon=True)
    tray_thread.start()

    sys.exit(app.exec())