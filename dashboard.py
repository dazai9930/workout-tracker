import customtkinter as ctk
from tkinter import ttk, messagebox, Menu
import pandas as pd
import os
import copy
from performance import show_performance
from utils import speak

EXERCISE_OPTIONS = ["Push Ups", "Squats", "Sit Ups", "Chest", "Plank"]
SETS_OPTIONS = [1, 2, 3, 4, 5]
REPS_OPTIONS = [5, 10, 12, 15, 20, 25, 30, 60]

FILE = None
workouts = []
backup_workouts = []

def load_data():
    if os.path.exists(FILE):
        return pd.read_excel(FILE).to_dict(orient="records")
    return []

def save_data():
    pd.DataFrame(workouts).to_excel(FILE, index=False)

def launch_dashboard(username):
    global FILE, workouts, root, sets_dropdown, reps_dropdown, checkbox_vars, treebox, backup_workouts

    FILE = f"user_data/{username}_workouts.xlsx"
    os.makedirs("user_data", exist_ok=True)
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
            if messagebox.askyesno("Confirm Delete", "Delete selected workout?"):
                workouts.pop(int(selected[0]))
                save_data()
                refresh()

    def delete_all_workouts():
        global backup_workouts
        if messagebox.askyesno("Delete All", "Clear all workouts?"):
            backup_workouts = copy.deepcopy(workouts)
            workouts.clear()
            save_data()
            refresh()

    def undo_delete_all():
        global backup_workouts
        if backup_workouts:
            workouts.extend(backup_workouts)
            save_data()
            refresh()
            backup_workouts = []

    def refresh():
        treebox.delete(*treebox.get_children())
        for i, w in enumerate(workouts):
            treebox.insert("", "end", iid=i, values=(w.get("day", ""), w["name"], w["sets"], w["reps"]))

    def voice_announce_workouts():
        if not workouts:
            speak("No workouts found.")
        else:
            speak(f"You have {len(workouts)} workouts.")
            for i, w in enumerate(workouts):
                speak(f"{i+1}: {w['sets']} sets of {w['reps']} {w['name']}")

    def show_context_menu(event):
        selected = treebox.identify_row(event.y)
        if selected:
            treebox.selection_set(selected)
            context_menu.post(event.x_root, event.y_root)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    root.geometry("600x800")
    root.title(f"{username}'s Workout Tracker")

    menubar = Menu(root)
    perf_menu = Menu(menubar, tearoff=0)
    perf_menu.add_command(label="View Performance", command=show_performance)
    menubar.add_cascade(label="Performance", menu=perf_menu)
    root.config(menu=menubar)

    title = ctk.CTkLabel(root, text="🏋️ Daily Workout Dashboard", font=("Arial", 24, "bold"))
    title.pack(pady=10)

    checkbox_frame = ctk.CTkFrame(root)
    checkbox_frame.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(checkbox_frame, text="✅ Select Exercises", font=("Arial", 16)).pack(pady=5)

    checkbox_vars = []
    for name in EXERCISE_OPTIONS:
        var = ctk.BooleanVar()
        cb = ctk.CTkCheckBox(checkbox_frame, text=name, variable=var)
        cb.pack(anchor="w", padx=20)
        checkbox_vars.append((var, name))

    selector = ctk.CTkFrame(checkbox_frame)
    selector.pack(pady=10)
    ctk.CTkLabel(selector, text="Sets").grid(row=0, column=0)
    sets_dropdown = ctk.CTkOptionMenu(selector, values=[str(s) for s in SETS_OPTIONS])
    sets_dropdown.set("3")
    sets_dropdown.grid(row=0, column=1)

    ctk.CTkLabel(selector, text="Reps").grid(row=1, column=0)
    reps_dropdown = ctk.CTkOptionMenu(selector, values=[str(r) for r in REPS_OPTIONS])
    reps_dropdown.set("12")
    reps_dropdown.grid(row=1, column=1)

    ctk.CTkButton(checkbox_frame, text="➕ Add", command=add_selected_checkboxes).pack(pady=5)
    ctk.CTkButton(checkbox_frame, text="🔊 Speak", command=voice_announce_workouts).pack()

    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

    treebox = ttk.Treeview(tree_frame, columns=("Day", "Exercise", "Sets", "Reps"), show="headings")
    for col in ("Day", "Exercise", "Sets", "Reps"):
        treebox.heading(col, text=col)
        treebox.column(col, width=100, anchor="center")
    treebox.pack(expand=True, fill="both", padx=10, pady=10)

    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="Delete", command=delete_workout)
    treebox.bind("<Button-3>", show_context_menu)

    btn_frame = ctk.CTkFrame(root)
    btn_frame.pack(pady=10)
    ctk.CTkButton(btn_frame, text="❌ Delete", command=delete_workout).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="🩹 Clear All", command=delete_all_workouts).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="↩️ Undo", command=undo_delete_all).pack(side="left", padx=5)

    refresh()
    root.mainloop()
