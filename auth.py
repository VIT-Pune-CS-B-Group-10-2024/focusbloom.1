import sqlite3
from database import hash_password
import tkinter as tk
from tkinter import messagebox
from welcome import WelcomeScreen

class AuthSystem:
    def __init__(self):
        self.conn = sqlite3.connect('mentalhealth.db')
        
    def register_user(self, username: str, password: str) -> bool:
        """Register a new user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hash_password(password))
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def login_user(self, username: str, password: str) -> bool:
        """Authenticate a user"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hash_password(password))
        )
        return cursor.fetchone() is not None
    
    def __del__(self):
        """Clean up database connection"""
        self.conn.close()

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")
        
        self.auth = AuthSystem()
        
        # Username label and entry
        tk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)
        
        # Password label and entry
        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)
        
        # Login button
        tk.Button(root, text="Login", command=self.login).pack(pady=10)
        
        # Register button
        tk.Button(root, text="Register", command=self.register).pack(pady=10)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.auth.login_user(username, password):
            self.root.destroy()
            WelcomeScreen(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.auth.register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Username already exists")