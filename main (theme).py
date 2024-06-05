import tkinter as tk
from tkinter import ttk

class TaskApp:
    def __init__(self, master):
        self.master = master
        self.tasks = []
        self.themes = {
            'light': {
                'bg': 'white',
                'fg': 'black',
                'sidebar_bg': 'lightgrey',
                'sidebar_fg': 'black',
                'button_bg': 'lightgrey',
                'button_fg': 'black',
                'entry_bg': 'white',
                'entry_fg': 'black'
            },
            'dark': {
                'bg': 'black',
                'fg': 'white',
                'sidebar_bg': 'grey',
                'sidebar_fg': 'white',
                'button_bg': 'grey',
                'button_fg': 'white',
                'entry_bg': 'black',
                'entry_fg': 'white'
            },
            'pink': { 
                'bg': '#fddde6',
                'fg': 'black',
                'sidebar_bg': '#FFB6C1',
                'sidebar_fg': 'black',
                'button_bg': '#FF69B4',
                'button_fg': 'black',
                'entry_bg': '#fddde6',
                'entry_fg': 'black'
            },
            'blue': { 
                'bg': '#ace5ee',
                'fg': 'black',
                'sidebar_bg': '#87ceeb',
                'sidebar_fg': 'black',
                'button_bg': '#1e90ff',
                'button_fg': 'black',
                'entry_bg': '#ace5ee',
                'entry_fg': 'black'
            },
            'purple': { 
                'bg': '#dcd0ff',
                'fg': 'black',
                'sidebar_bg': '#b19cd9',
                'sidebar_fg': 'black',
                'button_bg': '#7851a9',
                'button_fg': 'black',
                'entry_bg': '#dcd0ff',
                'entry_fg': 'black'
            },

        }
        self.activity_icons = {
            'Saving': 'saving.png',
            'Homework': 'homework.png',
            'Exercise': 'exercise.png',
            'Shopping': 'shopping.png'
        }

        self.create_widgets()
        self.apply_theme('light')


def create_widgets(self):
        # Sidebar
        self.sidebar_frame = tk.Frame(self.master, width=200)
        self.sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        self.sidebar_label = tk.Label(self.sidebar_frame, text="To Do List", font=("Helvetica", 14))
        self.sidebar_label.pack(pady=10)

        self.btn_inbox = tk.Button(self.sidebar_frame, text="Inbox", width=20)
        self.btn_inbox.pack(pady=5)

        self.btn_important = tk.Button(self.sidebar_frame, text="Important", width=20)
        self.btn_important.pack(pady=5)

        self.btn_today = tk.Button(self.sidebar_frame, text="Today", width=20)
        self.btn_today.pack(pady=5)

        self.btn_upcoming = tk.Button(self.sidebar_frame, text="Upcoming", width=20)
        self.btn_upcoming.pack(pady=5)

        # Main Content
        self.main_frame = tk.Frame(self.master, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.label_title = tk.Label(self.main_frame, text="Task", font=("Helvetica", 16))
        self.label_title.pack(pady=10)

        self.task_list = tk.Frame(self.main_frame)
        self.task_list.pack(anchor="w")

        self.task_entry = tk.Entry(self.main_frame, width=50)
        self.task_entry.pack()

        self.add_button = tk.Button(self.main_frame, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.add_dropdown_menu(self.add_button)
    
        self.theme_var = tk.StringVar(value='light')
        self.theme_menu = ttk.OptionMenu(self.main_frame, self.theme_var, 'light', *self.themes.keys(), command=self.apply_theme)
        self.theme_menu.pack(pady=10)


def apply_theme(self, theme_name):
        theme = self.themes[theme_name]
        self.master.configure(bg=theme['bg'])
        self.sidebar_frame.configure(bg=theme['sidebar_bg'])
        self.sidebar_label.configure(bg=theme['sidebar_bg'], fg=theme['sidebar_fg'])
        self.btn_inbox.configure(bg=theme['button_bg'], fg=theme['button_fg'])
        self.btn_important.configure(bg=theme['button_bg'], fg=theme['button_fg'])
        self.btn_today.configure(bg=theme['button_bg'], fg=theme['button_fg'])
        self.btn_upcoming.configure(bg=theme['button_bg'], fg=theme['button_fg'])
        self.main_frame.configure(bg=theme['bg'])
        self.label_title.configure(bg=theme['bg'], fg=theme['fg'])
        self.task_entry.configure(bg=theme['entry_bg'], fg=theme['entry_fg'])
        self.add_button.configure(bg=theme['button_bg'], fg=theme['button_fg'])
        
        for task in self.tasks:
            task['check'].configure(bg=theme['bg'], fg=theme['fg'])
            task['label'].configure(bg=theme['bg'], fg=theme['fg'])
            task['dots'].configure(bg=theme['bg'], fg=theme['fg'])

def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            task_frame = tk.Frame(self.task_list, bg=self.master.cget("bg"))
            task_frame.pack(anchor="w", pady=5)

            task_check = tk.Checkbutton(task_frame, command=lambda: self.toggle_task(task_check), bg=self.master.cget("bg"))
            task_check.pack(side=tk.LEFT)

            task_label = tk.Label(task_frame, text=task_text, width=40, anchor="w", bg=self.master.cget("bg"), fg=self.master.cget("fg"))
            task_label.pack(side=tk.LEFT)

            dots_label = tk.Label(task_frame, text="...", padx=10, cursor="hand2", bg=self.master.cget("bg"), fg=self.master.cget("fg"))
            dots_label.pack(side=tk.RIGHT)
            dots_label.bind("<Button-1>", lambda event, frame=task_frame: self.show_popup_menu(event, frame))

            self.tasks.append({"text": task_text, "frame": task_frame, "check": task_check, "label": task_label, "dots": dots_label})
            self.task_entry.delete(0, tk.END)

def add_task_with_icon(self, activity):
        task_text = f"{activity}: {self.task_entry.get()}"
        if task_text:
            task_frame = tk.Frame(self.task_list, bg=self.master.cget("bg"))
            task_frame.pack(anchor="w", pady=5)

            task_check = tk.Checkbutton(task_frame, command=lambda: self.toggle_task(task_check), bg=self.master.cget("bg"))
            task_check.pack(side=tk.LEFT)

            task_label = tk.Label(task_frame, text=task_text, width=40, anchor="w", bg=self.master.cget("bg"), fg=self.master.cget("fg"))
            task_label.pack(side=tk.LEFT)

            dots_label = tk.Label(task_frame, text="...", padx=10, cursor="hand2", bg=self.master.cget("bg"), fg=self.master.cget("fg"))
            dots_label.pack(side=tk.RIGHT)
            dots_label.bind("<Button-1>", lambda event, frame=task_frame: self.show_popup_menu(event, frame))

            self.tasks.append({"text": task_text, "frame": task_frame, "check": task_check, "label": task_label, "dots": dots_label})
            self.task_entry.delete(0, tk.END)

def add_dropdown_menu(self, master):
        options_menu = tk.Menu(master, tearoff=0)
        for activity in self.activity_icons.keys():
            options_menu.add_command(label=activity, command=lambda act=activity: self.add_task_with_icon(act))
        
        master.config(menu=options_menu)

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
        self.tasks = [task for task in self.tasks if task["frame"] != task_frame]

if __name__ == "__main__":
    root = tk.Tk()
    root.title("To Do List")
    root.geometry("800x700")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (800/2)
    y = (screen_height/2) - (700/2)
    root.geometry(f'+{int(x)}+{int(y)}')
    
    app = TaskApp(root)
    root.mainloop()
