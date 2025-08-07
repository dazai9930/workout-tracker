import customtkinter as ctk
from tkinter import messagebox
import json
import os
from dashboard import launch_dashboard

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def show_login_page():
    def login_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        users = load_users()
        if username in users and users[username] == password:
            login_win.destroy()
            launch_dashboard(username)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def register_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
        users = load_users()
        if username in users:
            messagebox.showerror("Error", "User already exists")
        else:
            users[username] = password
            save_users(users)
            messagebox.showinfo("Success", "User registered. You can now log in.")

    login_win = ctk.CTk()
    login_win.geometry("400x300")
    login_win.title("Login")

    ctk.CTkLabel(login_win, text="Username").pack(pady=5)
    username_entry = ctk.CTkEntry(login_win)
    username_entry.pack()

    ctk.CTkLabel(login_win, text="Password").pack(pady=5)
    password_entry = ctk.CTkEntry(login_win, show="*")
    password_entry.pack()

    ctk.CTkButton(login_win, text="Login", command=login_user).pack(pady=10)
    ctk.CTkButton(login_win, text="Register", command=register_user).pack(pady=5)

    login_win.mainloop()
