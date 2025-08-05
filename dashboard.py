import customtkinter as ctk
from tkinter import messagebox, ttk
import os
import pandas as pd
import pyttsx3

FILE = None
EXERCISE_OPTIONS = ["Push Ups", "Squats", "Sit Ups", "Lunges", "Plank"]
SETS_OPTIONS = [1, 2, 3, 4, 5]
REPS_OPTIONS = [5, 10, 12, 15, 20, 25, 30, 60]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def load_data():
    if os.path.exists(FILE):
        return pd.read_excel(FILE).to_dict(orient="records")
    return []

def save_data():
    pd.DataFrame(workouts).to_excel(FILE, index=False)

def launch_dashboard(username):
    global FILE, workouts, root, sets_dropdown, reps_dropdown, checkbox_vars, treebox
    FILE = f"user_data/{username}_workouts.xlsx"
    if not os.path.exists("user_data"):
        os.makedirs("user_data")
    workouts = load_data()

    def add_selected_checkboxes():
        for var, name in checkbox_vars:
            if var.get():
                workouts.append({
                    "day": pd.Timestamp.now().strftime("%A"),
                    "name": name,
                    "sets": int(sets_dropdown.get()),
                    "reps": int(reps_dropdown.get())
                })
        save_data()
        refresh()

    def delete_workout():
        selected = treebox.selection()
        if selected:
            idx = int(selected[0])
            workouts.pop(idx)
            save_data()
            refresh()

    def delete_all_workouts():
        if messagebox.askyesno("Delete All", "Are you sure you want to delete all workouts?"):
            workouts.clear()
            save_data()
            refresh()

    def refresh():
        treebox.delete(*treebox.get_children())
        for i, w in enumerate(workouts):
            treebox.insert("", "end", iid=i, values=(w.get("day", ""), w["name"], w["sets"], w["reps"]))

    def voice_announce_workouts():
        if not workouts:
            speak("No workouts found.")
        else:
            speak(f"You have {len(workouts)} workouts scheduled today.")
            for i, w in enumerate(workouts):
                speak(f"{i+1}. {w['sets']} sets of {w['reps']} reps of {w['name']}")

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title(f"{username}'s Workout Tracker")
    root.geometry("500x700")

    checkbox_frame = ctk.CTkFrame(root)
    checkbox_frame.pack(padx=10, pady=10, fill="both")
    ctk.CTkLabel(checkbox_frame, text="Today’s Workout To-Do List:").pack(pady=5)

    checkbox_vars = []
    for name in EXERCISE_OPTIONS:
        var = ctk.BooleanVar()
        cb = ctk.CTkCheckBox(checkbox_frame, text=name, variable=var)
        cb.pack(anchor="w")
        checkbox_vars.append((var, name))

    selector_frame = ctk.CTkFrame(checkbox_frame)
    selector_frame.pack(pady=10)

    ctk.CTkLabel(selector_frame, text="Select Sets:").grid(row=0, column=0, padx=5, pady=5)
    sets_dropdown = ctk.CTkOptionMenu(selector_frame, values=[str(s) for s in SETS_OPTIONS])
    sets_dropdown.set("3")
    sets_dropdown.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(selector_frame, text="Select Reps:").grid(row=1, column=0, padx=5, pady=5)
    reps_dropdown = ctk.CTkOptionMenu(selector_frame, values=[str(r) for r in REPS_OPTIONS])
    reps_dropdown.set("12")
    reps_dropdown.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkButton(checkbox_frame, text="Add Selected Exercises", command=add_selected_checkboxes).pack(pady=5)
    ctk.CTkButton(checkbox_frame, text="🔣 Announce Workouts", command=voice_announce_workouts).pack(pady=5)

    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25,
                    fieldbackground="#343638", bordercolor="#343638", borderwidth=0)
    style.map('Treeview', background=[('selected', '#22559b')])

    treebox = ttk.Treeview(tree_frame, columns=("Day", "Exercise", "Sets", "Reps"), show="headings")
    treebox.heading("Day", text="Day")
    treebox.heading("Exercise", text="Exercise")
    treebox.heading("Sets", text="Sets")
    treebox.heading("Reps", text="Reps")
    treebox.pack(fill="both", expand=True)

    ctk.CTkButton(root, text="Delete Workout", command=delete_workout).pack(pady=5)
    ctk.CTkButton(root, text="Delete All Workouts", command=delete_all_workouts).pack(pady=5)

    refresh()
    root.mainloop()
