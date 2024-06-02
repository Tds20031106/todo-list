import tkinter as tk
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry
import datetime
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        task_name TEXT,
        due_date DATE,
        completed INTEGER
    )
''')
conn.commit()

# Declare global variables
task_list = None
task_entry = None
due_date_entry = None
background_photo = None
def logout(app):
    app.destroy()  # Close the current window
    

def open_todo_list_window(user_id):
    global task_list, task_entry, due_date_entry ,background_image
    def update_task_list():
        task_list.delete(0, tk.END)
        cursor.execute('SELECT * FROM tasks WHERE user_id=?',(user_id,))
        tasks = cursor.fetchall()
        for task in tasks:
            task_id = task[0]
            task_name = task[2]
            due_date = datetime.datetime.strptime(task[3], "%m/%d/%y").date()  # Convert to datetime.date
            completed = task[4]
            status = "Upcoming"
            if completed:
                status = "Completed"
            elif due_date < datetime.datetime.now().date():
                status = "Pending"
            task_list.insert(tk.END, f"{task_id} - {task_name} - Due: {due_date} - Status: {status}")
    def add_task():
        task = task_entry.get()
        due_date = due_date_entry.get()
        cursor.execute('INSERT INTO tasks (user_id, task_name, due_date, completed) VALUES (?, ?, ?, ?)',
                       (user_id, task, due_date, 0))
        conn.commit()
        update_task_list()
    def mark_completed():
        selected_indices =task_list.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_task_id = task_list.get(selected_index).split('-')[0].strip()
            cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (selected_task_id,))
            conn.commit()
            update_task_list()
    def remove_task():
        selected_indices =task_list.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_task_id = task_list.get(selected_index).split('-')[0].strip()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (selected_task_id,))
            conn.commit()
            update_task_list()
    app = tk.Toplevel()
    app.title("To-Do List Application")
    app.geometry("700x500+0+0")
    app.resizable(False, False) 
    heading=tk.Label(app,text="TO DO LIST",font=("Arial", 25))
    heading.place(x=440,y=0)
    task_label = tk.Label(app, text="Task:")
    task_label.place(x=520,y=60)
    task_entry = tk.Entry(app)
    task_entry.place(x=475,y=85)
    due_date_label = tk.Label(app, text="Due Date:")
    due_date_label.place(x=510,y=110)
    due_date_entry = DateEntry(app, width= 16, background= "magenta3", foreground= "white",bd=2)
    due_date_entry.place(x=475,y=135)
    add_button = tk.Button(app, text="Add Task", command=add_task)
    add_button.place(x=510,y=160)
    task_list = tk.Listbox(app,height=12, width=50)
    task_list.place(x=400,y=195)
    remove_button = tk.Button(app, text="Remove Task", command=remove_task)
    remove_button.place(x=440, y=420)
    mark_completed_button = tk.Button(app, text="Mark Completed", command=mark_completed)
    mark_completed_button.place(x=535,y=420)
    logout_button = tk.Button(app, text="Logout", command=lambda: logout(app))
    logout_button.place(x=520, y=460)
    background_image = Image.open("background.jpeg")
    background_image = background_image.resize((300, 600))
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(app, image=background_photo)
    background_label.place(x=0, y=0)
    app.mainloop()
    return app
