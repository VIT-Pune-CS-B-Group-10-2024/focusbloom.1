from auth import LoginApp
import tkinter as tk

if __name__ == "__main__":
    
    from database import initialize_db
    initialize_db()
    
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()