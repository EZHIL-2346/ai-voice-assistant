import pygetwindow

def get_active_window_title():
    try:
        return pygetwindow.getActiveWindowTitle()
    except:
        return "Unknown"
