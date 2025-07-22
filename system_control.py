import os
import subprocess
import webbrowser

def open_app(app_name):
    """Universal app opener"""
    try:
        if os.name == 'nt':  # Windows
            os.system(f'start {app_name}')
        else:  # Mac/Linux
            os.system(f'open {app_name}' if sys.platform == 'darwin' else f'xdg-open {app_name}')
    except Exception as e:
        print(f"Error opening {app_name}: {e}")

# Example usage:
def open_discord():
    open_app("discord")

def open_chrome():
    open_app("chrome")

# ... keep other functions but use open_app where possible