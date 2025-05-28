import tkinter as tk
from tkinter import ttk
from auth.auth import AuthFrame
from auth.welcome import WelcomeFrame
from todo.todo import TodoFrame
from habit_journal.habit_journal import HabitJournalFrame
from productivity.productivity import ProductivityFrame
from mood_reminder.mood_reminder import MoodReminderFrame
from music_motivation.music_motivation import MusicMotivationFrame
from db import init_db

class MentalHealthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mental Health App")
        self.geometry("1000x700")
        self.current_user = None
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Initialize database
        init_db()
        
        # Create container
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.show_frame("AuthFrame")
    
    def show_frame(self, frame_name):
        for widget in self.container.winfo_children():
            widget.destroy()
            
        frames = {
            "AuthFrame": AuthFrame,
            "WelcomeFrame": WelcomeFrame,
            "TodoFrame": TodoFrame,
            "HabitJournalFrame": HabitJournalFrame,
            "ProductivityFrame": ProductivityFrame,
            "MoodReminderFrame": MoodReminderFrame,
            "MusicMotivationFrame": MusicMotivationFrame
        }
        
        frame_class = frames[frame_name]
        frame = frame_class(self.container, self)
        frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MentalHealthApp()
    app.mainloop()
