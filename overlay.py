import tkinter as tk
from tkinter import ttk
import threading
from modules.voice_engine import speak
from modules.recognizer import listen
from modules.window_tracker import get_active_window_title
from modules.system_control import *
from modules.gpt_agent import ask_gpt
from modules.screen_reader import read_screen
import pygetwindow as gw
import sv_ttk

class AssistantOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Assistant")
        sv_ttk.set_theme("dark")
        
        # Make window always on top and transparent
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)
        self.root.overrideredirect(True)
        
        # Position window in bottom right
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"300x400+{screen_width-320}+{screen_height-420}")
        
        self.create_widgets()
        self.listening = False
        self.thinking = False
        
        # Start the assistant thread
        self.assistant_thread = threading.Thread(target=self.run_assistant, daemon=True)
        self.assistant_thread.start()
        
    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Assistant status
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var, 
                                    font=('Helvetica', 12, 'bold'))
        self.status_label.pack(pady=10)
        
        # Visual feedback for listening
        self.canvas = tk.Canvas(self.main_frame, width=100, height=100, bg='#333333')
        self.canvas.pack(pady=20)
        self.circle = self.canvas.create_oval(20, 20, 80, 80, fill='gray')
        
        # Command history
        self.history_label = ttk.Label(self.main_frame, text="Command History:")
        self.history_label.pack(anchor='w', pady=(20,5))
        
        self.history_text = tk.Text(self.main_frame, height=8, width=30, 
                                  bg='#333333', fg='white', state=tk.DISABLED)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Close button
        self.close_btn = ttk.Button(self.main_frame, text="X", 
                                  command=self.root.destroy, width=2)
        self.close_btn.place(relx=1.0, rely=0.0, anchor='ne')
        
    def update_history(self, text):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, f"> {text}\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
        
    def set_status(self, status):
        self.status_var.set(status)
        color = {
            'Ready': 'green',
            'Listening...': 'blue',
            'Thinking...': 'yellow',
            'Speaking...': 'purple'
        }.get(status, 'gray')
        self.canvas.itemconfig(self.circle, fill=color)
        
    def run_assistant(self):
        while True:
            self.set_status("Ready")
            self.root.update()
            
            # Listen for activation phrase
            self.set_status("Listening...")
            command = listen()
            
            if not command:
                continue
                
            self.update_history(f"You: {command}")
            self.set_status("Thinking...")
            
            # Process command
            response = self.process_command(command)
            
            if response:
                self.update_history(f"Assistant: {response}")
                self.set_status("Speaking...")
                speak(response)
                
    def process_command(self, command):
        if "read screen" in command:
            text = read_screen()
            return "Here's what I found on the screen: " + text[:200]
            
        elif "open discord" in command:
            open_discord()
            return "Opening Discord."
            
        elif "stop" in command or "exit" in command:
            self.root.after(1000, self.root.destroy)
            return "Goodbye!"
            
        else:
            return ask_gpt(command)
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    from modules.elevate import run_as_admin
    run_as_admin()
    assistant = AssistantOverlay()
    assistant.run()