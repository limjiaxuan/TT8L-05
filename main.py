import tkinter as tk
<<<<<<< HEAD
<<<<<<< HEAD
from tkinter import ttk
import calendar
from datetime import datetime

class TaskApp:
    def __init__(self, master):
        self.master = master
        self.tasks = []
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

        btn_search = tk.Button(sidebar_frame, text="Search", width=20, highlightbackground="lightgrey", command=self.show_search)
        btn_search.pack(pady=5)

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
            "search": tk.Frame(self.main_frame),
            "today": tk.Frame(self.main_frame),
            "upcoming": tk.Frame(self.main_frame),
            "add_task": tk.Frame(self.main_frame)
        }

        self.show_inbox()

    def show_add_task_popup(self):
        add_task_window = tk.Toplevel(self.master)
        add_task_window.title("Add Task")

        tk.Label(add_task_window, text="Task Name").pack(pady=5)
        task_name_entry = tk.Entry(add_task_window, width=50)
        task_name_entry.pack(pady=5)

        tk.Label(add_task_window, text="Description").pack(pady=5)
        task_desc_entry = tk.Entry(add_task_window, width=50)
        task_desc_entry.pack(pady=5)

        button_frame = tk.Frame(add_task_window)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add Task", command=lambda: self.add_task(task_name_entry.get(), task_desc_entry.get(), add_task_window))
        add_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=add_task_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def show_search(self):
        self.show_frame("search")
        self.clear_frame(self.frames["search"])

        label_title = tk.Label(self.frames["search"], text="Search", font=("Helvetica", 16))
        label_title.pack(pady=10)

        self.search_entry = tk.Entry(self.frames["search"], width=50)
        self.search_entry.pack()

        self.search_button = tk.Button(self.frames["search"], text="Search", command=self.search_task)
        self.search_button.pack()

    def show_inbox(self):
        self.show_frame("task_list")
        self.clear_frame(self.frames["task_list"])

        label_title = tk.Label(self.frames["task_list"], text="Inbox", font=("Helvetica", 16))
        label_title.pack(pady=10)

        self.task_list = tk.Frame(self.frames["task_list"])
        self.task_list.pack(anchor="w")

        for task in self.tasks:
            self.display_task(task)

        self.task_entry = tk.Entry(self.frames["task_list"], width=50)
        self.task_entry.pack()

        self.add_button = tk.Button(self.frames["task_list"], text="Add Task", command=self.show_add_task_popup)
        self.add_button.pack()

    def show_today(self):
        self.show_frame("today")
        self.clear_frame(self.frames["today"])

        label_title = tk.Label(self.frames["today"], text="Today", font=("Helvetica", 16))
        label_title.pack(pady=10)

        today_date = datetime.now().strftime("%Y-%m-%d")
        today_tasks = [task for task in self.tasks if task.get("date") == today_date]

        for task in today_tasks:
            task_label = tk.Label(self.frames["today"], text=task["text"])
            task_label.pack(anchor="w")

    def show_upcoming(self):
        self.show_frame("upcoming")
        self.clear_frame(self.frames["upcoming"])

        label_title = tk.Label(self.frames["upcoming"], text="Upcoming", font=("Helvetica", 16))
        label_title.pack(pady=10)

        upcoming_tasks = sorted(self.tasks, key=lambda x: x.get("date", ""))

        for task in upcoming_tasks:
            task_label = tk.Label(self.frames["upcoming"], text=task["text"])
            task_label.pack(anchor="w")

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

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill=tk.BOTH, expand=True)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def add_task(self, task_name, task_desc, window):
        if task_name:
            task = {"name": task_name, "desc": task_desc}
            self.tasks.append(task)
            self.display_task(task)
            window.destroy()

    def display_task(self, task):
        task_frame = tk.Frame(self.task_list)
        task_frame.pack(anchor="w", pady=5)

        task_check = tk.Checkbutton(task_frame, command=lambda: self.toggle_task(task_check))
        task_check.pack(side=tk.LEFT)

        task_label = tk.Label(task_frame, text=f"{task['name']}: {task['desc']}", width=40, anchor="w")
        task_label.pack(side=tk.LEFT)

        dots_label = tk.Label(task_frame, text="...", padx=10, cursor="hand2")
        dots_label.pack(side=tk.RIGHT)
        dots_label.bind("<Button-1>", lambda event, frame=task_frame: self.show_popup_menu(event, frame))

        task["frame"] = task_frame
        task["check"] = task_check

    def search_task(self):
        search_text = self.search_entry.get()
        if search_text:
            self.show_frame("search")
            self.clear_frame(self.frames["search"])

            label_title = tk.Label(self.frames["search"], text="Search Results", font=("Helvetica", 16))
            label_title.pack(pady=10)

            for task in self.tasks:
                if search_text.lower() in task["name"].lower() or search_text.lower() in task["desc"].lower():
                    task_label = tk.Label(self.frames["search"], text=f"{task['name']}: {task['desc']}")
                    task_label.pack(anchor="w")

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
        task_name, task_desc = current_text.split(": ", 1)

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

        button_frame = tk.Frame(edit_window)
        button_frame.pack(pady=10)

        save_button = tk.Button(button_frame, text="Save", command=lambda: self.save_task(task_frame, edit_window, task_name_entry, task_desc_entry))
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=edit_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def save_task(self, task_frame, edit_window, task_name_entry, task_desc_entry):
        new_name = task_name_entry.get()
        new_desc = task_desc_entry.get()
        task_label = task_frame.winfo_children()[1]
        task_label.config(text=f"{new_name}: {new_desc}")
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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("To Do List")
    root.geometry("800x600")

    app = TaskApp(root)

    root.mainloop()
=======
from tkinter import messagebox
from datetime import datetime, timedelta
=======
>>>>>>> 215b430 (Add sidebar, edit and delete)

class TaskApp:
    def __init__(self, master):
        self.master = master
        self.tasks = []
        self.create_widgets()

    def create_widgets(self):
        # Sidebar
        sidebar_frame = tk.Frame(self.master, bg="lightgrey", width=200)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        sidebar_label = tk.Label(sidebar_frame, text="To Do List", font=("Helvetica", 14), bg="lightgrey")
        sidebar_label.pack(pady=10)

        btn_inbox = tk.Button(sidebar_frame, text="Inbox", width=20, highlightbackground="lightgrey", highlightcolor="lightgrey")
        btn_inbox.pack(pady=5)

        btn_important = tk.Button(sidebar_frame, text="Important", width=20, highlightbackground="lightgrey", highlightcolor="lightgrey")
        btn_important.pack(pady=5)

        btn_today = tk.Button(sidebar_frame, text="Today", width=20, highlightbackground="lightgrey", highlightcolor="lightgrey")
        btn_today.pack(pady=5)

        btn_upcoming = tk.Button(sidebar_frame, text="Upcoming", width=20, highlightbackground="lightgrey", highlightcolor="lightgrey")
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

        self.add_button = tk.Button(main_frame, text="Add Task", command=self.add_task)
        self.add_button.pack()

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            task_frame = tk.Frame(self.task_list)
            task_frame.pack(anchor="w", pady=5)

            task_check = tk.Checkbutton(task_frame, command=lambda: self.toggle_task(task_check))
            task_check.pack(side=tk.LEFT)

            task_label = tk.Label(task_frame, text=task_text, width=40, anchor="w")
            task_label.pack(side=tk.LEFT)

            # Three dots symbol for menu
            dots_label = tk.Label(task_frame, text="...", padx=10, cursor="hand2")
            dots_label.pack(side=tk.RIGHT)
            dots_label.bind("<Button-1>", lambda event, frame=task_frame: self.show_popup_menu(event, frame))

<<<<<<< HEAD
root.mainloop()
>>>>>>> 0575657 (modify GUI element)
=======
            self.tasks.append({"text": task_text, "frame": task_frame, "check": task_check})
            self.task_entry.delete(0, tk.END)

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
    root.geometry("800x500")  

    app = TaskApp(root)

    root.mainloop()
>>>>>>> 215b430 (Add sidebar, edit and delete)
