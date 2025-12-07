import webview
import pygetwindow as gw
import time
import threading

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

if __name__ == '__main__':
    create_pet_window()