import os
import platform
import tkinter as tk
from tkinter import Toplevel, Menu, messagebox
from tkcalendar import Calendar, DateEntry
import calendar
import sqlite3
from datetime import datetime
from tkinter import PhotoImage, Button
from plyer import notification 

COLOR_THEMES = {
    "Light Theme": {"bg": "#fdf5e6", "fg": "black"},
    "Dark Theme": {"bg": "#555555", "fg": "white"},
    "Blue Theme": {"bg": "#add8e6", "fg": "black"}
}

class TaskApp:
    def __init__(self, master):
        self.master = master
        self.tasks = []
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.selected_datetime = ""
        self.current_user = None  

        # Initialize the database
        self.initialize_db()

        self.create_widgets()

        # Load tasks from the database
        self.load_tasks_from_db()

        # Start checking for reminders
        self.check_reminders()

        # Minimize to system tray
        self.window_closed = False
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.icon = None

    def show_theme_selection(self):
        theme_window = tk.Toplevel(self.master)
        theme_window.title("Select Theme")

        theme_label = tk.Label(theme_window, text="Select a Theme:", font=("Helvetica", 16))
        theme_label.pack(pady=10)

        for theme_name in COLOR_THEMES:
            theme_button = tk.Button(theme_window, text=theme_name, width=20, command=lambda name=theme_name: self.apply_theme(name))
            theme_button.pack(pady=5)

    def apply_theme(self, theme_name):
        if theme_name in COLOR_THEMES:
            theme_colors = COLOR_THEMES[theme_name]
            bg_color = theme_colors["bg"]
            fg_color = theme_colors.get("fg", "black") 
            self.master.configure(bg=bg_color) 
            self.apply_theme_to_widgets(self.master, bg_color, fg_color)

    def apply_theme_to_widgets(self, parent, bg_color, fg_color):
        for widget in parent.winfo_children():
            widget.configure(bg=bg_color)
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Checkbutton)):
                widget.configure(fg=fg_color)
            if isinstance(widget, (tk.Frame, tk.Button, tk.LabelFrame)):
                self.apply_theme_to_widgets(widget, bg_color, fg_color)

    def create_widgets(self):
        # Sidebar
        sidebar_frame = tk.Frame(self.master, bg="lightgrey", width=200)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        # Add buttons to sidebar
        btn_user = tk.Button(sidebar_frame, text="User", width=20, highlightbackground="lightgrey", command=self.show_user_options)
        btn_user.pack(pady=5)
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

        btn_theme = tk.Button(sidebar_frame, text="Theme", width=20, highlightbackground="lightgrey", command=self.show_theme_selection)
        btn_theme.pack(pady=5)

        # Main Content
        self.main_frame = tk.Frame(self.master, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.frames = {
            "task_list": tk.Frame(self.main_frame),
            "calendar": tk.Frame(self.main_frame),
            "today": tk.Frame(self.main_frame),
            "upcoming": tk.Frame(self.main_frame),
            "add_task": tk.Frame(self.main_frame),
            "selected_day_tasks": tk.Frame(self.main_frame),
            "search_results": tk.Frame(self.main_frame),
            "user": tk.Frame(self.main_frame)
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
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                icon_path TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def load_tasks_from_db(self):
        self.tasks.clear()
        if self.current_user:
            self.cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (self.current_user["id"],))
            rows = self.cursor.fetchall()
            for row in rows:
                task = {"id": row[0], "name": row[1], "desc": row[2], "due_date": row[3], "icon_path": row[4]}
                self.tasks.append(task)
                self.display_task(task)

    def save_task_to_db(self, task):
        self.cursor.execute("INSERT INTO tasks (name, description, due_date, icon_path, user_id) VALUES (?, ?, ?, ?, ?)",
                            (task["name"], task["desc"], task["due_date"], task["icon_path"], self.current_user["id"]))
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

        self.date_entry = DateEntry(header_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(side=tk.LEFT, padx=10)
        self.date_entry.bind("<<DateEntrySelected>>", self.on_date_select)

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
                if day:
                    day_button = tk.Button(self.calendar_content_frame, text=str(day), padx=10, pady=5, command=lambda d=day: self.show_tasks_for_day(year, month, d))
                    day_button.grid(row=row + 1, column=col)
                else:
                    day_label = tk.Label(self.calendar_content_frame, text="", padx=10, pady=5)
                    day_label.grid(row=row + 1, column=col) 

    def on_date_select(self, event):
        selected_date = self.date_entry.get_date()
        self.show_tasks_for_day(selected_date.year, selected_date.month, selected_date.day)

    def show_tasks_for_day(self, year, month, day):
        selected_date = datetime(year, month, day).strftime("%m/%d/%y")
        tasks_for_day = [task for task in self.tasks if task["due_date"] and datetime.strptime(task["due_date"], "%m/%d/%y %H:%M").strftime("%m/%d/%y") == selected_date]

        self.show_frame("selected_day_tasks")
        self.clear_frame(self.frames["selected_day_tasks"])

        tk.Label(self.frames["selected_day_tasks"], text=f"Tasks for {selected_date}", font=("Helvetica", 16)).pack(pady=10)
        
        back_button = tk.Button(self.frames["selected_day_tasks"], text="Back to Calendar", command=self.show_calendar)
        back_button.pack(pady=10)
        back_button.pack(side=tk.RIGHT)

        if tasks_for_day:
            for task in tasks_for_day:
                self.display_task(task, self.frames["selected_day_tasks"])
        else:
            tk.Label(self.frames["selected_day_tasks"], text="No tasks for this day.", font=("Helvetica", 14)).pack(pady=10)

    def show_add_task_popup(self):
        if not self.current_user:
            messagebox.showerror("Error", "Please login first.")
            return

        add_task_window = Toplevel(self.master)
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

        tk.Label(add_task_window, text="Icon").pack(pady=5)
        icon_label = tk.Label(add_task_window, text="Not selected", width=50, relief=tk.SUNKEN)
        icon_label.pack(pady=5)

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
                hour = hour_entry.get() or "00"
                minute = minute_entry.get() or "00"
                due_date_time = f"{due_date} {hour}:{minute}"
                due_date_label.config(text=due_date_time)
                calendar_window.destroy()

            select_button = tk.Button(calendar_window, text="Select", command=set_due_date)
            select_button.pack(pady=10)

        select_due_date_button = tk.Button(add_task_window, text="Select Due Date and Time", command=select_due_date)
        select_due_date_button.pack(pady=5)

        button_frame = tk.Frame(add_task_window)
        button_frame.pack(pady=10)

        def select_icon():
            icon_window = Toplevel(add_task_window)
            icon_window.title("Select Icon")

            def select_and_close(icon_path):
                nonlocal selected_icon
                selected_icon = icon_path
                icon_label.config(text=icon_path)
                icon_window.destroy()

            icon_paths = [
                "icon/excercise.png",
                "icon/face-mask.png",
                "icon/homework.png",
                "icon/cleaning-products.png",
                "icon/laundry-machine.png",
                "icon/online-training.png",
                "icon/pets.png",
                "icon/piggy-bank.png",
                "icon/shopping-cart.png",
                "icon/sleep.png",
                "icon/study.png",
                "icon/medicine.png"
            ]

            num_rows = (len(icon_paths) + 3 - 1) // 3  # Ceiling division for rows
            num_columns = 3  # 3 columns

            for idx, icon_path in enumerate(icon_paths):
                icon_image = PhotoImage(file=icon_path)
                resized_icon = icon_image.subsample(6)
                icon_button = Button(icon_window, image=resized_icon, command=lambda path=icon_path: select_and_close(path))
                icon_button.image = resized_icon  # Keep a reference to prevent garbage collection
                row = idx // num_columns
                col = idx % num_columns
                icon_button.grid(row=row, column=col, padx=4, pady=4)  # Use grid layout

            icon_window.grab_set()
            selected_icon = None
            icon_window.wait_window()

            add_button = tk.Button(button_frame, text="Add Task", command=lambda: self.add_task(task_name_entry.get(), task_desc_entry.get(), due_date_label.cget("text"), selected_icon, add_task_window))

        select_icon_button = tk.Button(add_task_window, text="Select Icon", command=select_icon)
        select_icon_button.pack(pady=5)

        button_frame = tk.Frame(add_task_window)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add Task", command=lambda: self.add_task(task_name_entry.get(), task_desc_entry.get(), due_date_label.cget("text"),icon_label.cget("text"), add_task_window))
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

    def add_task(self, task_name, task_desc, due_date, icon_path, add_task_window):
        if not due_date or due_date == "Not set":
            messagebox.showerror("Error", "Please select a due date and time.")
            return    
        if task_name:
            task = {
                "id": None,
                "name": task_name,
                "desc": task_desc,
                "due_date": due_date,
                "icon_path": icon_path,
                "frame": None,
                "check": None
            }
            self.tasks.append(task)
            self.save_task_to_db(task)
            add_task_window.destroy()
            self.show_inbox()

    def save_task_changes(self, task, name, desc, due_date, icon_path, window):
        task["name"] = name
        task["desc"] = desc
        task["due_date"] = due_date
        task["icon_path"] = icon_path
        self.update_task_in_db(task)
        window.destroy()
        self.show_inbox()

    def search_task(self):
        search_query = self.search_entry.get().lower()
        matching_tasks = [task for task in self.tasks if search_query in task["name"].lower()]
        self.show_search_results(matching_tasks)

    def show_search_results(self, tasks):
        self.show_frame("search_results")
        self.clear_frame(self.frames["search_results"])

        tk.Label(self.frames["search_results"], text="Search Results", font=("Helvetica", 16)).pack(pady=10)
        
        back_button = tk.Button(self.frames["search_results"], text="Back", command=self.show_inbox)
        back_button.pack(pady=10)
        back_button.pack(side=tk.LEFT)

        if tasks:
            for task in tasks:
                self.display_task(task, self.frames["search_results"])
        else:
            tk.Label(self.frames["search_results"], text="No matching tasks found.", font=("Helvetica", 14)).pack(pady=10)

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

        if task["icon_path"] and task["icon_path"] != "Not selected":
            icon_image = PhotoImage(file=task["icon_path"])
            resized_icon = icon_image.subsample(6)  # Adjust the subsample factor to resize
            icon_label = tk.Label(task_frame, image=resized_icon)
            icon_label.image = resized_icon  # Keep a reference to prevent garbage collection
            icon_label.pack(side=tk.LEFT, padx=10)

        check = tk.Checkbutton(task_frame, text=task_text, font=("Helvetica", 14), anchor="w")
        check.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Three-dot button for edit/delete
        options_button = tk.Menubutton(task_frame, text="...", relief=tk.FLAT)
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

        tk.Label(edit_task_window, text="Icon").pack(pady=5)
        icon_label = tk.Label(edit_task_window, text=task["icon_path"] if task["icon_path"] else "Not selected", width=50, relief=tk.SUNKEN)
        icon_label.pack(pady=5)

        def select_due_date():
            calendar_window = Toplevel(edit_task_window)
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
                hour = hour_entry.get() or "00"
                minute = minute_entry.get() or "00"
                due_date_time = f"{due_date} {hour}:{minute}"
                due_date_label.config(text=due_date_time)
                calendar_window.destroy()

            select_button = tk.Button(calendar_window, text="Select", command=set_due_date)
            select_button.pack(pady=10)

        select_due_date_button = tk.Button(edit_task_window, text="Select Due Date and Time", command=select_due_date)
        select_due_date_button.pack(pady=5)

        def select_icon():
            icon_window = Toplevel(edit_task_window)
            icon_window.title("Select Icon")

            def select_and_close(icon_path):
                nonlocal selected_icon
                selected_icon = icon_path
                icon_label.config(text=icon_path)
                icon_window.destroy()

            icon_paths = [
                "icon/excercise.png",
                "icon/face-mask.png",
                "icon/homework.png",
                "icon/cleaning-products.png",
                "icon/laundry-machine.png",
                "icon/online-training.png",
                "icon/pets.png",
                "icon/piggy-bank.png",
                "icon/shopping-cart.png",
                "icon/sleep.png",
                "icon/study.png",
                "icon/medicine.png"
            ]

            num_rows = (len(icon_paths) + 3 - 1) // 3  # Ceiling division for rows
            num_columns = 3  # 3 columns

            for idx, icon_path in enumerate(icon_paths):
                icon_image = PhotoImage(file=icon_path)
                resized_icon = icon_image.subsample(6)
                icon_button = Button(icon_window, image=resized_icon, command=lambda path=icon_path: select_and_close(path))
                icon_button.image = resized_icon  # Keep a reference to prevent garbage collection
                row = idx // num_columns
                col = idx % num_columns
                icon_button.grid(row=row, column=col, padx=4, pady=4)  # Use grid layout
                
            icon_window.grab_set()
            selected_icon = None
            icon_window.wait_window()

        select_icon_button = tk.Button(edit_task_window, text="Select Icon", command=select_icon)
        select_icon_button.pack(pady=5)

        button_frame = tk.Frame(edit_task_window)
        button_frame.pack(pady=10)

        save_button = tk.Button(button_frame, text="Save", command=lambda: self.save_task_changes(task, task_name_entry.get(), task_desc_entry.get(), due_date_label.cget("text"), edit_task_window))
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=edit_task_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def save_task_changes(self, task, name, desc, due_date, window):
        if not due_date or due_date == "Not set":
            messagebox.showerror("Error", "Please select a due date and time.")
            return   
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

    # notification and reminder
    def macos_notify(self, title, message):
        os.system(f'''osascript -e 'display notification "{message}" with title "{title}"' ''')

    def notify(self, title, message):
        if platform.system() == "Darwin":  # macOS
            self.macos_notify(title, message)
        else:  # Windows and other platforms
            notification.notify(
                title=title,
                message=message,
                timeout=10
            )

    def check_reminders(self):
        now = datetime.now()
        now_str = now.strftime("%m/%d/%y %H:%M")
        for task in self.tasks:
            if task["due_date"]:
                due_date = datetime.strptime(task["due_date"], "%m/%d/%y %H:%M")
                due_date_str = due_date.strftime("%m/%d/%y %H:%M")
                if now_str == due_date_str:
                    self.notify(
                        title="Task Reminder",
                        message=f"{task['name']}, {task['desc']}, due at {task['due_date']}"
                    )
                    self.show_reminder_popup(task)
        self.master.after(10000, self.check_reminders) 

    def on_close(self):
        self.window_closed = True
        self.conn.commit()
        self.conn.close()
        self.master.destroy()

    # User management functions
    def show_user_options(self):
        self.show_frame("user")
        self.clear_frame(self.frames["user"])

        if self.current_user:
            tk.Label(self.frames["user"], text=f"Logged in as: {self.current_user['username']}", font=("Helvetica", 14)).pack(pady=10)
            tk.Button(self.frames["user"], text="Logout", command=self.logout_user).pack(pady=10)
        else:
            tk.Button(self.frames["user"], text="Register", command=self.show_register_popup).pack(pady=10)
            tk.Button(self.frames["user"], text="Login", command=self.show_login_popup).pack(pady=10)

    def show_login_popup(self):
        login_window = Toplevel(self.master)
        login_window.title("Login")

        tk.Label(login_window, text="Username").pack(pady=5)
        username_entry = tk.Entry(login_window, width=50)
        username_entry.pack(pady=5)

        tk.Label(login_window, text="Password").pack(pady=5)
        password_entry = tk.Entry(login_window, width=50, show='*')
        password_entry.pack(pady=5)

        button_frame = tk.Frame(login_window)
        button_frame.pack(pady=10)

        login_button = tk.Button(button_frame, text="Login", command=lambda: self.login_user(username_entry.get(), password_entry.get(), login_window))
        login_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=login_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def show_register_popup(self):
        register_window = Toplevel(self.master)
        register_window.title("Register")

        tk.Label(register_window, text="Username").pack(pady=5)
        username_entry = tk.Entry(register_window, width=50)
        username_entry.pack(pady=5)

        tk.Label(register_window, text="Password").pack(pady=5)
        password_entry = tk.Entry(register_window, width=50, show='*')
        password_entry.pack(pady=5)

        button_frame = tk.Frame(register_window)
        button_frame.pack(pady=10)

        register_button = tk.Button(button_frame, text="Register", command=lambda: self.register_user(username_entry.get(), password_entry.get(), register_window))
        register_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=register_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def register_user(self, username, password, window):
        if username and password:
            try:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                self.conn.commit()
                messagebox.showinfo("Success", "User registered successfully!")
                window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")
        else:
            messagebox.showerror("Error", "Please fill out all fields.")

    def login_user(self, username, password, window):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()
        if user:
            self.current_user = {"id": user[0], "username": user[1]}
            messagebox.showinfo("Success", "Login successful!")
            window.destroy()
            self.load_tasks_from_db()
            self.show_inbox()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def logout_user(self):
        self.current_user = None
        self.tasks.clear()
        self.show_inbox()
        messagebox.showinfo("Success", "Logout successful!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("To Do List")
    root.geometry("800x600")

    app = TaskApp(root)

    root.mainloop()
    