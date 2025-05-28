import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class AuthFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.create_widgets()
    
    def create_widgets(self):
        # Username
        ttk.Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Password
        ttk.Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Login", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Sign Up", command=self.signup).pack(side=tk.LEFT, padx=5)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            self.controller.current_user = user[0]
            self.controller.show_frame("WelcomeFrame")
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "All fields required")
            return
        
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Account created! Please login")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()
