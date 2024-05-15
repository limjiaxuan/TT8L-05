
import tkinter as tk
from tkinter import Toplevel, messagebox
from tkcalendar import Calendar
from tkinter.ttk import Spinbox

class TaskApp:
    def __init__(self, master):
        self.master = master
        self.tasks = []
        self.selected_datetime = None
        self.create_widgets()

    def create_widgets(self):
        # Sidebar
        sidebar_frame = tk.Frame(self.master, bg="lightgrey", width=200)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        sidebar_label = tk.Label(sidebar_frame, text="To Do List", font=("Helvetica", 14), bg="lightgrey")
        sidebar_label.pack(pady=10)

        btn_inbox = tk.Button(sidebar_frame, text="Inbox", width=20, highlightbackground="lightgrey")
        btn_inbox.pack(pady=5)

        btn_important = tk.Button(sidebar_frame, text="Important", width=20, highlightbackground="lightgrey")
        btn_important.pack(pady=5)

        btn_today = tk.Button(sidebar_frame, text="Today", width=20, highlightbackground="lightgrey")
        btn_today.pack(pady=5)

        btn_upcoming = tk.Button(sidebar_frame, text="Upcoming", width=20, highlightbackground="lightgrey")
        btn_upcoming.pack(pady=5)

        # Main Content
        main_frame = tk.Frame(self.master, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        label_title = tk.Label(main_frame, text="Task", font=("Helvetica", 16))
        label_title.pack(pady=10)

        self.task_list = tk.Frame(main_frame)
        self.task_list.pack(anchor="w")

        self.task_entry = tk.Entry(main_frame, width=50)
        self.task_entry.pack()

        self.calendar_button = tk.Button(main_frame, text="Select Date and Time", command=self.show_calendar)
        self.calendar_button.pack(pady=5)

        self.add_button = tk.Button(main_frame, text="Add Task", command=self.add_task)
        self.add_button.pack()

    def show_calendar(self):
        calendar_window = Toplevel(self.master)
        calendar_window.title("Select a Date and Time")
        calendar_window.grab_set() 
        calendar = Calendar(calendar_window, selectmode='day')
        calendar.pack(pady=20)

        hour_spin = Spinbox(calendar_window, from_=0, to=23, wrap=True, format='%02.0f', state="readonly")
        hour_spin.pack(side='left', padx=(10, 0))

        minute_spin = Spinbox(calendar_window, from_=0, to=59, wrap=True, format='%02.0f', state="readonly")
        minute_spin.pack(side='left', padx=(10, 0))

        def select_date_time():
            date = calendar.get_date()
            hour = hour_spin.get()
            minute = minute_spin.get()
            self.selected_datetime = f"{date} {hour}:{minute}"
            calendar_window.destroy()

        select_button = tk.Button(calendar_window, text="Select", command=select_date_time)
        select_button.pack(pady=10)

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text and self.selected_datetime:
            task_frame = tk.Frame(self.task_list)
            task_frame.pack(anchor="w", pady=5)

            task_check = tk.Checkbutton(task_frame, command=lambda: self.toggle_task(task_check))
            task_check.pack(side=tk.LEFT)

            task_label = tk.Label(task_frame, text=f"{task_text} (Due on {self.selected_datetime})", width=40, anchor="w")
            task_label.pack(side=tk.LEFT)

            # Three dots symbol for menu
            dots_label = tk.Label(task_frame, text="...", padx=10, cursor="hand2")
            dots_label.pack(side=tk.RIGHT)
            dots_label.bind("<Button-1>", lambda event, frame=task_frame: self.show_popup_menu(event, frame))

            self.tasks.append({"text": task_text, "frame": task_frame, "check": task_check})
            self.task_entry.delete(0, tk.END)
            self.selected_datetime = None
            self.tasks.append({"text": task_text, "frame": task_frame, "check": task_check})

        else:

            messagebox.showinfo("Incomplete Information", "Please enter a task and select a date and time.")           
    def toggle_task(self, task_check):
        for task in self.tasks:
            if task["check"] == task_check:
                if task_check.cget("background") == "":
                    task_check.configure(background="cyan")
                else:
                    task_check.configure(background="")
                break

    def show_popup_menu(self, event, task_frame):
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Edit", command=lambda frame=task_frame: self.edit_task(frame))
        menu.add_command(label="Delete", command=lambda frame=task_frame: self.delete_task(frame))
        menu.post(event.x_root, event.y_root)

    def edit_task(self, task_frame):
        task_label = task_frame.winfo_children()[1]  
        current_text = task_label.cget("text")

        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Task")

        edit_entry = tk.Entry(edit_window, width=40)
        edit_entry.insert(0, current_text)
        edit_entry.pack(padx=10, pady=10)

        save_button = tk.Button(edit_window, text="Save", command=lambda: self.save_task(task_frame, edit_window, edit_entry))
        save_button.pack()

    def save_task(self, task_frame, edit_window, edit_entry):
        new_text = edit_entry.get()
        task_label = task_frame.winfo_children()[1]  
        task_label.config(text=new_text)
        edit_window.destroy()  # Close the edit window after saving

    def delete_task(self, task_frame):
        task_frame.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("To Do List")
    root.geometry("800x700")
    app = TaskApp(root)
    root.mainloop()
