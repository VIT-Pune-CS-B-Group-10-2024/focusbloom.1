import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TodoFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.create_widgets()
        self.load_tasks()
    
    def create_widgets(self):
        # Add Task
        add_frame = ttk.Frame(self)
        add_frame.pack(pady=10)
        
        self.task_entry = ttk.Entry(add_frame, width=30)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        priority_label = ttk.Label(add_frame, text="Priority:")
        priority_label.pack(side=tk.LEFT, padx=5)
        
        self.priority_var = tk.StringVar()
        self.priority_combobox = ttk.Combobox(add_frame, 
                                            textvariable=self.priority_var,
                                            values=["High", "Medium", "Low"],
                                            state="readonly")
        self.priority_combobox.current(1)
        self.priority_combobox.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(add_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT, padx=5)
        
        # Task List
        self.tree = ttk.Treeview(self, columns=("Priority", "Status"), show="headings")
        self.tree.heading("#0", text="Task")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Progress
        self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(pady=10)
        
        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Mark Complete", command=self.mark_complete).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)
    
    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        
        if not task:
            messagebox.showwarning("Warning", "Please enter a task")
            return
        
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO todos (user_id, task, priority) VALUES (?, ?, ?)",
                 (self.controller.current_user, task, priority))
        conn.commit()
        conn.close()
        
        self.task_entry.delete(0, tk.END)
        self.load_tasks()
    
    def load_tasks(self):
        # Clear existing tasks
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("SELECT id, task, priority, completed FROM todos WHERE user_id=?",
                 (self.controller.current_user,))
        
        total = 0
        completed = 0
        
        for task in c.fetchall():
            status = "Complete" if task[3] else "Pending"
            self.tree.insert("", "end", text=task[1], values=(task[2], status))
            
            total += 1
            if task[3]:
                completed += 1
        
        conn.close()
        
        if total > 0:
            self.progress["value"] = (completed / total) * 100
        else:
            self.progress["value"] = 0
    
    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        task_text = self.tree.item(selected[0])["text"]
        
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("UPDATE todos SET completed=1 WHERE user_id=? AND task=?",
                 (self.controller.current_user, task_text))
        conn.commit()
        conn.close()
        
        self.load_tasks()
    
    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        task_text = self.tree.item(selected[0])["text"]
        
        conn = sqlite3.connect('mental_health_app.db')
        c = conn.cursor()
        c.execute("DELETE FROM todos WHERE user_id=? AND task=?",
                 (self.controller.current_user, task_text))
        conn.commit()
        conn.close()
        
        self.load_tasks()
