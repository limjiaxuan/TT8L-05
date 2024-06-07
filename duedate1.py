import tkinter as tk
from tkinter import Toplevel, Menu
from tkcalendar import Calendar
import calendar
import sqlite3
from datetime import datetime

class TaskApp:
    def __init__(self, master):
        self.master = master
        self.tasks = []
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.selected_datetime = ""

        # Initialize the database
        self.initialize_db()

        self.create_widgets()

        # Load tasks from the database
        self.load_tasks_from_db()

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

        self.no_tasks_label = tk.Label(self.main_frame, text="No matching tasks found.", font=("Helvetica", 14), fg="black")
        self.show_inbox()

    def initialize_db(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                due_date TEXT
            )
        ''')
        self.conn.commit()

    def load_tasks_from_db(self):
        self.cursor.execute("SELECT * FROM tasks")
        rows = self.cursor.fetchall()
        for row in rows:
            task = {"id": row[0], "name": row[1], "desc": row[2], "due_date": row[3]}
            self.tasks.append(task)
            self.display_task(task)

    def save_task_to_db(self, task):
        self.cursor.execute("INSERT INTO tasks (name, description, due_date) VALUES (?, ?, ?)",
                            (task["name"], task["desc"], task["due_date"]))
        self.conn.commit()
        task["id"] = self.cursor.lastrowid

    def update_task_in_db(self, task):
        self.cursor.execute("UPDATE tasks SET name = ?, description = ?, due_date = ? WHERE id = ?",
                            (task["name"], task["desc"], task["due_date"], task["id"]))
        self.conn.commit()

    def delete_task_from_db(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def show_todo_list(self):
        self.clear_main_frame()
        self.frames["task_list"].pack(fill=tk.BOTH, expand=True)

        label_title = tk.Label(self.frames["task_list"], text="Task", font=("Helvetica", 16))
        label_title.pack(pady=10)

        self.task_list = tk.Frame(self.frames["task_list"])
        self.task_list.pack(anchor="w")

        self.task_entry = tk.Entry(self.frames["task_list"], width=50)
        self.task_entry.pack()

        self.calendar_button = tk.Button(self.frames["task_list"], text="Select Date and Time", command=self.show_calendar_popup)
        self.calendar_button.pack(pady=5)

        self.add_button = tk.Button(self.frames["task_list"], text="Add Task", command=self.add_task)
        self.add_button.pack()

    def show_calendar_popup(self):
        calendar_window = Toplevel(self.master)
        calendar_window.title("Select a Date and Time")
        calendar_window.grab_set()
        calendar = Calendar(calendar_window, selectmode='day')
        calendar.pack(pady=20)

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


            def validate_number(P):
                if P.isdigit() or P == "":
                    return True
                return False

            vcmd = (calendar_window.register(validate_number), '%P')

            tk.Label(calendar_window, text="Hour (0-23)").pack(side='left', padx=(10, 0))
            hour_entry = tk.Entry(calendar_window, width=5, validate='key', validatecommand=vcmd)
            hour_entry.pack(side='left', padx=(10, 0))

            tk.Label(calendar_window, text="Minute (0-59)").pack(side='left', padx=(10, 0))
            minute_entry = tk.Entry(calendar_window, width=5, validate='key', validatecommand=vcmd)
            minute_entry.pack(side='left', padx=(10, 0))

            def set_due_date():
                due_date = calendar.get_date()
                hour = hour_entry.get()
                minute = minute_entry.get()
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

        for task in self.tasks:
            self.display_task(task, self.frames["task_list"])

    def show_today(self):
        self.show_frame("today")
        self.clear_frame(self.frames["today"])
        today = datetime.now().date()
        tasks_today = [task for task in self.tasks if task["due_date"] and datetime.strptime(task["due_date"], "%m/%d/%y %H:%M").date() == today]
        self.display_tasks(self.frames["today"], tasks_today, "Today's Tasks")

    def show_upcoming(self):
        self.show_frame("upcoming")
        self.clear_frame(self.frames["upcoming"])
        today = datetime.now().date()
        tasks_upcoming = [task for task in self.tasks if task["due_date"] and datetime.strptime(task["due_date"], "%m/%d/%y %H:%M").date() > today]
        self.display_tasks(self.frames["upcoming"], tasks_upcoming, "Upcoming Tasks")

    def add_task(self, task_name, task_desc, due_date, add_task_window):
        if task_name:
            task = {
                "id": None,
                "name": task_name,
                "desc": task_desc,
                "due_date": due_date,
                "frame": None,
                "check": None
            }
            self.tasks.append(task)
            self.save_task_to_db(task)
            add_task_window.destroy()
            self.show_inbox()

    def search_task(self):
        search_query = self.search_entry.get().lower()
        matching_tasks = [task for task in self.tasks if search_query in task["name"].lower()]
        self.show_search_results(matching_tasks)

        for task in self.tasks:
            task["frame"].pack_forget()

        if matching_tasks:
            self.no_tasks_label.pack_forget()
            for task in matching_tasks:
                task["frame"].pack(anchor="w", pady=5)
        else:
            self.no_tasks_label.pack()
            self.master.after(3000, self.no_tasks_label.pack_forget)


    def show_search_results(self, tasks):
        self.show_frame("task_list")
        self.clear_frame(self.frames["task_list"])

        for task in tasks:
            self.display_task(task, self.frames["task_list"])

    def display_tasks(self, frame, tasks, title):
        tk.Label(frame, text=title, font=("Helvetica", 16)).pack(pady=10)
        for task in tasks:
            self.display_task(task, frame)

    def display_task(self, task, frame=None):
        if frame is None:
            frame = self.frames["task_list"]

        task_frame = tk.Frame(frame)
        task_frame.pack(fill=tk.X, pady=5)

        task_text = f"{task['name']}: {task['desc']}"
        if task["due_date"]:
            task_text += f" (Due: {task['due_date']})"
        else:
            task_text += " (Due: Not set)"

        check = tk.Checkbutton(task_frame, text=task_text, font=("Helvetica", 14), anchor="w")
        check.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

    # Three-dot button for edit/delete
        options_button = tk.Menubutton(task_frame, text="⋮", relief=tk.FLAT)
        options_button.pack(side=tk.RIGHT, padx=10)
        options_menu = Menu(options_button, tearoff=0)
        options_button.config(menu=options_menu)
        options_menu.add_command(label="Edit", command=lambda t=task: self.edit_task(t))
        options_menu.add_command(label="Delete", command=lambda t=task: self.delete_task(t))

        task["frame"] = task_frame
        task["check"] = check

    def edit_task(self, task):
        edit_task_window = Toplevel(self.master)
        edit_task_window.title("Edit Task")

        tk.Label(edit_task_window, text="Task Name").pack(pady=5)
        task_name_entry = tk.Entry(edit_task_window, width=50)
        task_name_entry.insert(0, task["name"])
        task_name_entry.pack(pady=5)

        tk.Label(edit_task_window, text="Description").pack(pady=5)
        task_desc_entry = tk.Entry(edit_task_window, width=50)
        task_desc_entry.insert(0, task["desc"])
        task_desc_entry.pack(pady=5)

        tk.Label(edit_task_window, text="Due Date and Time").pack(pady=5)
        due_date_label = tk.Label(edit_task_window, text=task["due_date"], width=50, relief=tk.SUNKEN)
        due_date_label.pack(pady=5)

        def select_due_date():
            calendar_window = Toplevel(edit_task_window)
            calendar_window.title("Select Due Date and Time")
            calendar = Calendar(calendar_window, selectmode='day')
            calendar.pack(pady=20)

            def set_due_date():
                due_date = calendar.get_date()
                hour = hour_entry.get()
                minute = minute_entry.get()
                due_date_time = f"{due_date} {hour}:{minute}"
                due_date_label.config(text=due_date_time)
                calendar_window.destroy()

            def validate_number(P):
                if P.isdigit() or P == "":
                    return True
                return False

            vcmd = (calendar_window.register(validate_number), '%P')

            tk.Label(calendar_window, text="Hour (0-23)").pack(side='left', padx=(10, 0))
            hour_entry = tk.Entry(calendar_window, width=5, validate='key', validatecommand=vcmd)
            hour_entry.pack(side='left', padx=(10, 0))

            tk.Label(calendar_window, text="Minute (0-59)").pack(side='left', padx=(10, 0))
            minute_entry = tk.Entry(calendar_window, width=5, validate='key', validatecommand=vcmd)
            minute_entry.pack(side='left', padx=(10, 0))


            select_button = tk.Button(calendar_window, text="Select", command=set_due_date)
            select_button.pack(pady=10)

        select_due_date_button = tk.Button(edit_task_window, text="Select Due Date and Time", command=select_due_date)
        select_due_date_button.pack(pady=5)

        button_frame = tk.Frame(edit_task_window)
        button_frame.pack(pady=10)

        save_button = tk.Button(button_frame, text="Save", command=lambda: self.save_task_changes(task, task_name_entry.get(), task_desc_entry.get(), due_date_label.cget("text"), edit_task_window))
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=edit_task_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def save_task_changes(self, task, name, desc, due_date, window):
        task["name"] = name
        task["desc"] = desc
        task["due_date"] = due_date
        self.update_task_in_db(task)
        window.destroy()
        self.show_inbox()

    def delete_task(self, task):
        task["frame"].destroy()
        self.tasks.remove(task)
        self.delete_task_from_db(task["id"])

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill=tk.BOTH, expand=True)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()


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

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.show_calendar_content(self.current_year, self.current_month)

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.show_calendar_content(self.current_year, self.current_month)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("To Do List")
    root.geometry("800x600")

    app = TaskApp(root)

    root.mainloop() 
