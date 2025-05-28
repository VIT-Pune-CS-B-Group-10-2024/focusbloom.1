import tkinter as tk
from tkinter import ttk
import random

class WelcomeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.quote = random.choice([
            "You are capable of amazing things",
            "Progress, not perfection",
            "Small steps lead to big changes",
            "Your mental health matters"
        ])
        
        self.create_widgets()
    
    def create_widgets(self):
        # Welcome message
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE id=?", (self.controller.current_user,))
        username = c.fetchone()[0]
        conn.close()
        
        ttk.Label(self, text=f"Welcome, {username}!").pack(pady=10)
        ttk.Label(self, text=self.quote, wraplength=400).pack(pady=5)
        
        # Navigation buttons
        nav_frame = ttk.Frame(self)
        nav_frame.pack(pady=20)
        
        buttons = [
            ("To-Do List", "TodoFrame"),
            ("Habit Tracker", "HabitJournalFrame"),
            ("Productivity Tools", "ProductivityFrame"),
            ("Mood Tracker", "MoodReminderFrame"),
            ("Music & Meditation", "MusicMotivationFrame")
        ]
        
        for text, frame in buttons:
            ttk.Button(nav_frame, text=text, 
                      command=lambda f=frame: self.controller.show_frame(f)).pack(pady=5)
