import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date

class HabitJournalFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.load_habits()
        self.load_journal()
        self.update_streak()

    def create_widgets(self):
        # Habit Log
        habit_frame = ttk.LabelFrame(self, text="Daily Habit Log")
        habit_frame.pack(fill="x", padx=10, pady=5)

        self.habit_entry = ttk.Entry(habit_frame, width=25)
        self.habit_entry.pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(habit_frame, text="Log Habit", command=self.log_habit).pack(side=tk.LEFT, padx=5)

        self.habit_list = tk.Listbox(habit_frame, height=3)
        self.habit_list.pack(side=tk.LEFT, padx=5, pady=5)

        # Streak Counter
        self.streak_label = ttk.Label(self, text="Current Streak: 0 days")
        self.streak_label.pack(pady=5)

        # Journal Entry
        journal_frame = ttk.LabelFrame(self, text="Journal Entry")
        journal_frame.pack(fill="x", padx=10, pady=5)

        self.journal_text = tk.Text(journal_frame, height=4, width=50)
        self.journal_text.pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(journal_frame, text="Save Entry", command=self.save_journal).pack(side=tk.LEFT, padx=5)

        # Journal History
        self.journal_history = tk.Listbox(self, height=6)
        self.journal_history.pack(fill="both", padx=10, pady=10, expand=True)

    def log_habit(self):
        habit = self.habit_entry.get()
        if not habit:
            messagebox.showwarning("Warning", "Enter a habit")
            return
        today = date.today().isoformat()
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO habits (user_id, habit, date, status) VALUES (?, ?, ?, ?)",
                  (self.controller.current_user, habit, today, 1))
        conn.commit()
        conn.close()
        self.habit_entry.delete(0, tk.END)
        self.load_habits()
        self.update_streak()

    def load_habits(self):
        self.habit_list.delete(0, tk.END)
        today = date.today().isoformat()
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT habit FROM habits WHERE user_id=? AND date=? AND status=1",
                  (self.controller.current_user, today))
        for row in c.fetchall():
            self.habit_list.insert(tk.END, row[0])
        conn.close()

    def save_journal(self):
        entry = self.journal_text.get("1.0", tk.END).strip()
        if not entry:
            messagebox.showwarning("Warning", "Journal entry cannot be empty")
            return
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO journal (user_id, entry) VALUES (?, ?)",
                  (self.controller.current_user, entry))
        conn.commit()
        conn.close()
        self.journal_text.delete("1.0", tk.END)
        self.load_journal()

    def load_journal(self):
        self.journal_history.delete(0, tk.END)
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT entry, created_at FROM journal WHERE user_id=? ORDER BY created_at DESC LIMIT 10",
                  (self.controller.current_user,))
        for row in c.fetchall():
            self.journal_history.insert(tk.END, f"{row[1][:10]}: {row[0]}")
        conn.close()

    def update_streak(self):
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT date FROM habits WHERE user_id=? AND status=1 ORDER BY date DESC",
                  (self.controller.current_user,))
        dates = [row[0] for row in c.fetchall()]
        streak = 0
        today = date.today()
        for i, d in enumerate(dates):
            if (today - datetime.strptime(d, "%Y-%m-%d").date()).days == i:
                streak += 1
            else:
                break
        self.streak_label.config(text=f"Current Streak: {streak} days")
        conn.close()
