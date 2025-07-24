import tkinter as tk
from tkinter import messagebox, ttk
import os

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Priority To-Do List")
        self.root.geometry("450x550")
        self.root.configure(bg="#f5f5f5")

        self.tasks = []

        tk.Label(root, text="To-Do List", font=("Helvetica", 18, "bold"), bg="#f5f5f5").pack(pady=10)

        entry_frame = tk.Frame(root, bg="#f5f5f5")
        entry_frame.pack(pady=10, padx=20, fill=tk.X)

        self.task_entry = tk.Entry(entry_frame, font=("Helvetica", 14))
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.priority_var = tk.StringVar()
        self.priority_box = ttk.Combobox(entry_frame, textvariable=self.priority_var, values=["High", "Medium", "Low"], state="readonly", width=10)
        self.priority_box.current(1)
        self.priority_box.pack(side=tk.RIGHT)

        btn_frame = tk.Frame(root, bg="#f5f5f5")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="➕ Add", command=self.add_task, width=10, bg="#4caf50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑 Delete", command=self.delete_task, width=10, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✔ Done", command=self.mark_done, width=10, bg="#2196f3", fg="white").pack(side=tk.LEFT, padx=5)

        self.listbox = tk.Listbox(root, font=("Helvetica", 14), selectbackground="#ddd", activestyle="none")
        self.listbox.pack(padx=20, pady=10, expand=True, fill=tk.BOTH)

        tk.Button(root, text="🧹 Clear All", command=self.clear_all, bg="#9c27b0", fg="white", font=("Helvetica", 12)).pack(pady=5)

        self.load_tasks()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_task(self):
        task = self.task_entry.get().strip()
        priority = self.priority_var.get()
        if task == "":
            messagebox.showwarning("Empty Task", "Please enter a task.")
            return
        task_entry = f"[{priority}] {task}"
        self.tasks.append(task_entry)
        self.update_listbox()
        self.task_entry.delete(0, tk.END)

    def delete_task(self):
        try:
            selected = self.listbox.curselection()[0]
            self.tasks.pop(selected)
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to delete.")

    def mark_done(self):
        try:
            selected = self.listbox.curselection()[0]
            task = self.tasks[selected]
            if not task.startswith("✔ "):
                self.tasks[selected] = "✔ " + task
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to mark as done.")

    def clear_all(self):
        confirm = messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?")
        if confirm:
            self.tasks.clear()
            self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            color = "black"
            if "[High]" in task:
                color = "red"
            elif "[Medium]" in task:
                color = "orange"
            elif "[Low]" in task:
                color = "green"
            self.listbox.insert(tk.END, task)
            self.listbox.itemconfig(tk.END, fg=color)

    def save_tasks(self):
        with open("tasks.txt", "w", encoding="utf-8") as f:
            for task in self.tasks:
                f.write(task + "\n")

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r", encoding="utf-8") as f:
                self.tasks = [line.strip() for line in f if line.strip()]
                self.update_listbox()

    def on_closing(self):
        self.save_tasks()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
