import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date
from tkcalendar import Calendar

class MoodReminderFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.load_moods()

    def create_widgets(self):
        # Mood Log
        mood_frame = ttk.LabelFrame(self, text="Daily Mood Log")
        mood_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(mood_frame, text="Mood (1-5):").pack(side=tk.LEFT, padx=5)
        self.mood_var = tk.IntVar(value=3)
        ttk.Spinbox(mood_frame, from_=1, to=5, textvariable=self.mood_var, width=5).pack(side=tk.LEFT, padx=5)
        self.notes_entry = ttk.Entry(mood_frame, width=30)
        self.notes_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(mood_frame, text="Log Mood", command=self.log_mood).pack(side=tk.LEFT, padx=5)

        # Calendar View
        cal_frame = ttk.LabelFrame(self, text="Mood Calendar")
        cal_frame.pack(fill="x", padx=10, pady=5)
        self.calendar = Calendar(cal_frame, selectmode='day')
        self.calendar.pack(pady=5)
        ttk.Button(cal_frame, text="Show Mood", command=self.show_mood_on_calendar).pack(pady=5)
        self.mood_label = ttk.Label(cal_frame, text="")
        self.mood_label.pack()

        # Reminders
        reminder_frame = ttk.LabelFrame(self, text="Reminders")
        reminder_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(reminder_frame, text="Set Break Reminder", command=self.set_reminder).pack(pady=5)

    def log_mood(self):
        score = self.mood_var.get()
        notes = self.notes_entry.get()
        today = date.today().isoformat()
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO mood (user_id, score, notes, created_at) VALUES (?, ?, ?, ?)",
                  (self.controller.current_user, score, notes, today))
        conn.commit()
        conn.close()
        self.notes_entry.delete(0, tk.END)
        self.load_moods()
        messagebox.showinfo("Mood", "Mood logged!")

    def load_moods(self):
        self.mood_data = {}
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT created_at, score FROM mood WHERE user_id=?", (self.controller.current_user,))
        for row in c.fetchall():
            self.mood_data[row[0]] = row[1]
        conn.close()

    def show_mood_on_calendar(self):
        sel_date = self.calendar.get_date()
        mood = self.mood_data.get(sel_date, "No entry")
        self.mood_label.config(text=f"Mood on {sel_date}: {mood}")

    def set_reminder(self):
        messagebox.showinfo("Reminder", "Don't forget to take a break and check in with yourself!")
