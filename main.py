import webview
import pygetwindow as gw
import time
import threading
import pystray
from PIL import Image, ImageDraw


class Api:
    def get_current_state(self):

        try:
            # Get the active window
            window = gw.getActiveWindow()
            if window:
                title = window.title.lower()
                
                if 'code' in title or 'studio' in title or 'py' in title:
                    return 'coding'  # State 1: Working hard
                elif 'spotify' in title or 'music' in title:
                    return 'music'   # State 2: Jamming
                elif 'chrome' in title or 'edge' in title or 'firefox' in title or 'brave' in title:
                    return 'browsing' # State 3: Internet
                
            return 'idle'
            
        except Exception as e:
            return 'idle'

def create_pet_window():
    api = Api()

    window = webview.create_window(
        'FocusPet', 
        'assets/index.html',
        js_api=api,
        transparent=True,
        frameless=True,      
        on_top=True,         
        width=200,           
        height=200,
    )
    webview.start()

def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

icon = pystray.Icon(
    'testname',
    icon=create_image(64, 64, 'black', 'white'))



if __name__ == '__main__':
    create_pet_window()
    icon.run()