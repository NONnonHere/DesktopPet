import webview
import threading
import time

def create_pet_window():
    window = webview.create_window(
        'DesktopPet', 
        'assets/index.html',
        transparent=True,   
        frameless=True,      
        on_top=True,         
        width=200,          
        height=200,
        background_color='#00000000' 
    )
    
    webview.start()

if __name__ == '__main__':
    create_pet_window()