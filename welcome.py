import tkinter as tk
from tkinter import messagebox

class WelcomeScreen:
    def __init__(self, username: str):
        self.root = tk.Tk()
        self.root.title(f"Welcome {username}")
        self.root.geometry("400x300")
        
        # Welcome message
        tk.Label(
            self.root,
            text=f"Welcome, {username}!",
            font=("Helvetica", 20)
        ).pack(pady=50)
        
        # Logout button
        tk.Button(
            self.root,
            text="Logout",
            command=self.root.destroy
        ).pack()
        
        self.root.mainloop()