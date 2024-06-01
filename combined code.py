
import tkinter as tk
from tkinter import Toplevel
from tkcalendar import Calendar
from tkinter.ttk import Spinbox
import calendar
from datetime import datetime

class TaskApp:
    def __init__(self, master):
        self.master = master
        self.tasks = []
        self.selected_datetime = None
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.create_widgets()

    def create_widgets(self):
        # Sidebar
        sidebar_frame = tk.Frame(self.master, bg="lightgrey", width=200)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        # Add buttons to sidebar
        btn_add_task = tk.Button(sidebar_frame, text="Add Task", width=20, highlightbackground="lightgrey", command=self.show_add_task_popup)
        btn_add_task.pack(pady=5)

        btn_inbox = tk.Button(sidebar_frame, text="Inbox", width=20, highlightbackground="lightgrey", command=self.show_inbox)
        btn_inbox.pack(pady=5)

        btn_today = tk.Button(sidebar_frame, text="Today", width=20, highlightbackground="lightgrey", command=self.show_today)
        btn_today.pack(pady=5)

        btn_upcoming = tk.Button(sidebar_frame, text="Upcoming", width=20, highlightbackground="lightgrey", command=self.show_upcoming)
        btn_upcoming.pack(pady=5)

        btn_calendar = tk.Button(sidebar_frame, text="Calendar", width=20, highlightbackground="lightgrey", command=self.show_calendar)
        btn_calendar.pack(pady=5)

        # Main Content
        self.main_frame = tk.Frame(self.master, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.frames = {
            "task_list": tk.Frame(self.main_frame),
            "calendar": tk.Frame(self.main_frame),
            "today": tk.Frame(self.main_frame),
            "upcoming": tk.Frame(self.main_frame),
            "add_task": tk.Frame(self.main_frame)
        }
        # Search bar and button
        search_frame = tk.Frame(self.master, padx=20, pady=10)
        search_frame.pack(fill=tk.X)

        self.search_entry = tk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))

        search_button = tk.Button(search_frame, text="Search", command=self.search_task)
        search_button.pack(side=tk.LEFT)

        self.task_list_frame = tk.Frame(self.main_frame)
        self.calendar_frame = tk.Frame(self.main_frame)

        self.no_tasks_label = tk.Label(self.main_frame, text="No matching tasks found.", font=("Helvetica", 14), fg="black")
        self.show_inbox()

    def show_todo_list(self):
        self.clear_main_frame()
        self.task_list_frame.pack(fill=tk.BOTH, expand=True)

        label_title = tk.Label(self.task_list_frame, text="Task", font=("Helvetica", 16))
        label_title.pack(pady=10)

        self.task_list = tk.Frame(self.task_list_frame)
        self.task_list.pack(anchor="w")

        self.task_entry = tk.Entry(self.task_list_frame, width=50)
        self.task_entry.pack()

        self.calendar_button = tk.Button(self.task_list_frame, text="Select Date and Time", command=self.show_calendar_popup)
        self.calendar_button.pack(pady=5)

        self.add_button = tk.Button(self.task_list_frame, text="Add Task", command=self.add_task)
        self.add_button.pack()

    def show_calendar_popup(self):
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
    
    def show_calendar(self):
        self.show_frame("calendar")
        self.clear_frame(self.frames["calendar"])

        header_frame = tk.Frame(self.frames["calendar"])
        header_frame.pack(fill=tk.X)

        self.prev_button = tk.Button(header_frame, text="<", command=self.prev_month)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(header_frame, text=">", command=self.next_month)
        self.next_button.pack(side=tk.RIGHT, padx=10)

        self.month_label = tk.Label(header_frame, text="", font=("Helvetica", 16))
        self.month_label.pack(side=tk.LEFT, expand=True)

        self.calendar_content_frame = tk.Frame(self.frames["calendar"])
        self.calendar_content_frame.pack(fill=tk.BOTH, expand=True)

        self.show_calendar_content(self.current_year, self.current_month)
    
    def show_add_task_popup(self):
        add_task_window = tk.Toplevel(self.master)
        add_task_window.title("Add Task")

        tk.Label(add_task_window, text="Task Name").pack(pady=5)
        task_name_entry = tk.Entry(add_task_window, width=50)
        task_name_entry.pack(pady=5)

        tk.Label(add_task_window, text="Description").pack(pady=5)
        task_desc_entry = tk.Entry(add_task_window, width=50)
        task_desc_entry.pack(pady=5)

        tk.Label(add_task_window, text="Due Date and Time").pack(pady=5)
        due_date_label = tk.Label(add_task_window, text="Not set", width=50, relief=tk.SUNKEN)
        due_date_label.pack(pady=5)

        def select_due_date():
            calendar_window = Toplevel(add_task_window)
            calendar_window.title("Select Due Date and Time")
            calendar = Calendar(calendar_window, selectmode='day')
            calendar.pack(pady=20)

            hour_spin = Spinbox(calendar_window, from_=0, to=23, wrap=True, format='%02.0f', state="readonly")
            hour_spin.pack(side='left', padx=(10, 0))

            minute_spin = Spinbox(calendar_window, from_=0, to=59, wrap=True, format='%02.0f', state="readonly")
            minute_spin.pack(side='left', padx=(10, 0))

            def set_due_date():
                due_date = calendar.get_date()
                hour = hour_spin.get()
                minute = minute_spin.get()
                due_date_time = f"{due_date} {hour}:{minute}"
                due_date_label.config(text=due_date_time)
                calendar_window.destroy()

            select_button = tk.Button(calendar_window, text="Select", command=set_due_date)
            select_button.pack(pady=10)

        select_due_date_button = tk.Button(add_task_window, text="Select Due Date and Time", command=select_due_date)
        select_due_date_button.pack(pady=5)

        button_frame = tk.Frame(add_task_window)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add Task", command=lambda: self.add_task(task_name_entry.get(), task_desc_entry.get(), due_date_label.cget("text"), add_task_window))
        add_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=add_task_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def show_inbox(self):
        self.show_frame("task_list")
        self.clear_frame(self.frames["task_list"])

        label_title = tk.Label(self.frames["task_list"], text="Inbox", font=("Helvetica", 16))
        label_title.pack(pady=10)

        self.task_list = tk.Frame(self.frames["task_list"])
        self.task_list.pack(anchor="w")

  
    def show_today(self):
        self.show_frame("today")
        self.clear_frame(self.frames["today"])

        label_title = tk.Label(self.frames["today"], text="Today", font=("Helvetica", 16))
        label_title.pack(pady=10)

        today_date = datetime.now().strftime("%Y-%m-%d")
        today_tasks = [task for task in self.tasks if task.get("due_date", "").startswith(today_date)]

        for task in today_tasks:
            task_label = tk.Label(self.frames["today"], text=f"{task['name']}: {task['desc']} (Due: {task['due_date']})")
            task_label.pack(anchor="w")

    def show_upcoming(self):
        self.show_frame("upcoming")
        self.clear_frame(self.frames["upcoming"])

        label_title = tk.Label(self.frames["upcoming"], text="Upcoming", font=("Helvetica", 16))
        label_title.pack(pady=10)

        upcoming_tasks = sorted(self.tasks, key=lambda x: x.get("due_date", ""))

        for task in upcoming_tasks:
            task_label = tk.Label(self.frames["upcoming"], text=f"{task['name']}: {task['desc']} (Due: {task['due_date']})")
            task_label.pack(anchor="w")

    def show_calendar_content(self, year, month):
        self.clear_frame(self.calendar_content_frame)

        cal = calendar.Calendar()
        month_days = cal.monthdayscalendar(year, month)

        self.month_label.config(text=f"{calendar.month_name[month]} {year}")

        days_header = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days_header):
            day_label = tk.Label(self.calendar_content_frame, text=day, padx=10, pady=5)
            day_label.grid(row=0, column=col)

        for row, week in enumerate(month_days):
            for col, day in enumerate(week):
                day_label = tk.Label(self.calendar_content_frame, text=str(day) if day else "", padx=10, pady=5)
                day_label.grid(row=row + 1, column=col)

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill=tk.BOTH, expand=True)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    def add_task(self, task_name, task_desc, due_date, window):
        if task_name:
            task = {"name": task_name, "desc": task_desc, "due_date": due_date}
            self.tasks.append(task)
            self.display_task(task)
            window.destroy()

    def display_task(self, task):
        task_frame = tk.Frame(self.task_list)
        task_frame.pack(anchor="w", pady=5)

        task_check = tk.Checkbutton(task_frame, command=lambda: self.toggle_task(task_check))
        task_check.pack(side=tk.LEFT)

        task_label = tk.Label(task_frame, text=f"{task['name']}: {task['desc']} (Due: {task['due_date']})", width=40, anchor="w")
        task_label.pack(side=tk.LEFT)

        dots_label = tk.Label(task_frame, text="...", padx=10, cursor="hand2")
        dots_label.pack(side=tk.RIGHT)
        dots_label.bind("<Button-1>", lambda event, frame=task_frame: self.show_popup_menu(event, frame))

        task["frame"] = task_frame
        task["check"] = task_check

    def toggle_task(self, task_check):
        for task in self.tasks:
            if task["check"] == task_check:
                current_bg = task_check.cget("background")
                task_check.configure(background="cyan" if not current_bg else "")
                break

    def show_popup_menu(self, event, task_frame):
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Edit", command=lambda frame=task_frame: self.edit_task(frame))
        menu.add_command(label="Delete", command=lambda frame=task_frame: self.delete_task(frame))
        menu.post(event.x_root, event.y_root)

    def edit_task(self, task_frame):
        task_label = task_frame.winfo_children()[1]
        current_text = task_label.cget("text")
        task_name, task_desc_due = current_text.split(": ", 1)
        task_desc, task_due = task_desc_due.rsplit(" (Due: ", 1)
        task_due = task_due[:-1]  # remove the closing parenthesis

        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Task")

        tk.Label(edit_window, text="Task Name").pack(pady=5)
        task_name_entry = tk.Entry(edit_window, width=50)
        task_name_entry.insert(0, task_name)
        task_name_entry.pack(pady=5)

        tk.Label(edit_window, text="Description").pack(pady=5)
        task_desc_entry = tk.Entry(edit_window, width=50)
        task_desc_entry.insert(0, task_desc)
        task_desc_entry.pack(pady=5)

        tk.Label(edit_window, text="Due Date and Time").pack(pady=5)
        task_due_label = tk.Label(edit_window, text=task_due, width=50, relief=tk.SUNKEN)
        task_due_label.pack(pady=5)

        def select_due_date():
            calendar_window = Toplevel(edit_window)
            calendar_window.title("Select Due Date and Time")
            calendar = Calendar(calendar_window, selectmode='day')
            calendar.pack(pady=20)

            hour_spin = Spinbox(calendar_window, from_=0, to=23, wrap=True, format='%02.0f', state="readonly")
            hour_spin.pack(side='left', padx=(10, 0))

            minute_spin = Spinbox(calendar_window, from_=0, to=59, wrap=True, format='%02.0f', state="readonly")
            minute_spin.pack(side='left', padx=(10, 0))

            def set_due_date():
                due_date = calendar.get_date()
                hour = hour_spin.get()
                minute = minute_spin.get()
                due_date_time = f"{due_date} {hour}:{minute}"
                task_due_label.config(text=due_date_time)
                calendar_window.destroy()

            select_button = tk.Button(calendar_window, text="Select", command=set_due_date)
            select_button.pack(pady=10)

        select_due_date_button = tk.Button(edit_window, text="Select Due Date and Time", command=select_due_date)
        select_due_date_button.pack(pady=5)

        button_frame = tk.Frame(edit_window)
        button_frame.pack(pady=10)

        save_button = tk.Button(button_frame, text="Save", command=lambda: self.save_task(task_frame, edit_window, task_name_entry, task_desc_entry, task_due_label.cget("text")))
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=edit_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def save_task(self, task_frame, edit_window, task_name_entry, task_desc_entry, task_due):
        new_name = task_name_entry.get()
        new_desc = task_desc_entry.get()
        task_label = task_frame.winfo_children()[1]
        task_label.config(text=f"{new_name}: {new_desc} (Due: {task_due})")
        edit_window.destroy()

    def delete_task(self, task_frame):
        for i, task in enumerate(self.tasks):
            if task["frame"] == task_frame:
                task_frame.destroy()
                del self.tasks[i]
                break

    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.show_calendar_content(self.current_year, self.current_month)

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.show_calendar_content(self.current_year, self.current_month)
        
    def search_task(self):
        search_query = self.search_entry.get().lower()
        matching_tasks = [task for task in self.tasks if search_query in task["name"].lower()]

        for task in self.tasks:
            task["frame"].pack_forget()

        if matching_tasks:
            self.no_tasks_label.pack_forget()
            for task in matching_tasks:
                task["frame"].pack(anchor="w", pady=5)
        else:
            self.no_tasks_label.pack()
            self.master.after(3000, self.no_tasks_label.pack_forget)
    def hide_no_tasks_label(self):
        self.no_tasks_label.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("To Do List")
    root.geometry("800x600")

    app = TaskApp(root)

    root.mainloop()
