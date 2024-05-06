import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

tasks = []

def add_task():
    task_name = entry_task.get()
    due_date = entry_due_date.get()
    if task_name:
        task = {"name": task_name, "due_date": due_date, "completed": False}
        tasks.append(task)
        update_task_list()
        entry_task.delete(0, tk.END)
        entry_due_date.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task name.")

def edit_task():
    try:
        index = listbox_tasks.curselection()[0]
        task = tasks[index]
        new_name = entry_task.get()
        new_due_date = entry_due_date.get()
        if new_name:
            task["name"] = new_name
            task["due_date"] = new_due_date
            update_task_list()
            entry_task.delete(0, tk.END)
            entry_due_date.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task name.")
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to edit.")

def delete_task():
    try:
        index = listbox_tasks.curselection()[0]
        del tasks[index]
        update_task_list()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete.")

def toggle_complete():
    try:
        index = listbox_tasks.curselection()[0]
        task = tasks[index]
        task["completed"] = not task["completed"]
        update_task_list()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task.")

def update_task_list():
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        status = "✔" if task["completed"] else "✖️"
        due_date = task["due_date"] if task["due_date"] else "No due date"
        listbox_tasks.insert(tk.END, f"{status} {task['name']} - Due: {due_date}")


root = tk.Tk()
root.title("To Do List App")

#GUI elements
label_title = tk.Label(root, text="To Do List", font=("Helvetica", 16))
label_title.pack(pady=10)

entry_task = tk.Entry(root, width=50)
entry_task.pack()

entry_due_date = tk.Entry(root, width=50)
entry_due_date.pack()

btn_add_task = tk.Button(root, text="Add Task", width=20, command=add_task)
btn_add_task.pack(pady=5)

btn_edit_task = tk.Button(root, text="Edit Task", width=20, command=edit_task)
btn_edit_task.pack()

btn_delete_task = tk.Button(root, text="Delete Task", width=20, command=delete_task)
btn_delete_task.pack()

btn_complete = tk.Button(root, text="Complete", width=20, command=toggle_complete)
btn_complete.pack()

listbox_tasks = tk.Listbox(root, width=50)
listbox_tasks.pack(pady=10)

root.mainloop()
