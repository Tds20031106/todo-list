import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import todo_list_window
# Database setup
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
''')
conn.commit()

# Declare global variables
new_username_entry = None
new_password_entry = None
login_window = None
signup_window=None
def open_login_window():
    login_window.deiconify()
def open_signup_window():
    login_window.withdraw()
    global new_username_entry, new_password_entry, bg_photo1  # Declare them as global
    signup_window = tk.Toplevel()
    signup_window.title("Signup")
    signup_window.geometry("500x400")
    signup_window.resizable(False, False) 
    bg_image1 = Image.open("bg2.jpg")
    bg_photo1 = ImageTk.PhotoImage(bg_image1)
    bg_label1 = tk.Label(signup_window, image=bg_photo1)
    bg_label1.place(relwidth=1, relheight=1)
    new_username_label = tk.Label(signup_window, text="New Username:",bg="#1B1035", fg="white")
    new_username_label.place(x=197,y=85)
    new_username_entry = tk.Entry(signup_window)
    new_username_entry.place(x=180,y=120)

    new_password_label = tk.Label(signup_window, text="New Password:",bg="#1B1035", fg="white")
    new_password_label.place(x=200,y=155)
    new_password_entry = tk.Entry(signup_window, show="*")
    new_password_entry.place(x=180,y=190)
    login_button = tk.Button(signup_window, text="Login", command=lambda: [open_login_window(), signup_window.withdraw()],bg="#160145", fg="white")
    login_button.place(x=223,y=285)
    login_label= tk.Label(signup_window, text="Already have an account ?",bg="#1B1035", fg="white")
    login_label.place(x=175,y=255)
    create_user_button = tk.Button(signup_window, text="Signup", command=create_user,bg="#1B1035", fg="white")
    create_user_button.place(x=220,y=225)
def create_user():
    global new_username_entry, new_password_entry  # Access them as global
    if new_username_entry and new_password_entry:
        username = new_username_entry.get()
        password = new_password_entry.get()
        if username.strip() == "" or password.strip() == "":
            messagebox.showerror("Error", "Please provide a valid username and password")
        else:
            try:
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                new_username_entry.delete(0, tk.END)
                new_password_entry.delete(0, tk.END)
                messagebox.showinfo("User Created", "User has been created successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists. Please choose a different username ")
def open_todo_list(user_id):
    login_window.withdraw()  # Hide the login window
    todo_list_window.open_todo_list_window(user_id)
def login():
    global username_entry, password_entry, login_window  # Access them as global
    username = username_entry.get()
    password = password_entry.get()
    if username.strip() == "" or password.strip() == "":
        messagebox.showerror("Error", "Please provide a valid username and password")
    else:
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()   
        if user:
            todo_list_window.open_todo_list_window(user[0])  # Pass the user ID to the to-do list window
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("500x400")
login_window.resizable(False, False) 
bg_image = Image.open("bg1.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(login_window, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)
username_label = tk.Label(login_window, text="Username:",bg="#371970", fg="white")
username_label.place(x=230,y=75)
username_entry = tk.Entry(login_window)
username_entry.place(x=200,y=100)
password_label = tk.Label(login_window, text="Password:",bg="#371970", fg="white")
password_label.place(x=230,y=125)
password_entry = tk.Entry(login_window, show="*")
password_entry.place(x=200,y=150)
login_button = tk.Button(login_window, text="Login", command=login,bg="#1F0954", fg="white")
login_button.place(x=240,y=175)
signup_label= tk.Label(login_window, text="Don't have a account ?",bg="#1F0954", fg="white")
signup_label.place(x=190,y=200)
signup_button = tk.Button(login_window, text="Signup", command=open_signup_window,bg="#1F0954", fg="white")
signup_button.place(x=235,y=225)
login_window.mainloop()
conn.close()
# ... (rest of your code)

