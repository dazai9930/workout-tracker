import customtkinter as ctk
from tkinter import messagebox
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_performance():
    # Always find the file relative to this script
    file_path = os.path.join(os.path.dirname(__file__), "performance.json")
    if not os.path.exists(file_path):
        messagebox.showinfo("No Data", "performance.json not found.")
        return

    with open(file_path, "r") as f:
        data = json.load(f)

    # Prepare data (only numeric values)
    exercises = []
    best_scores = []
    avg_scores = []

    for ex, stats in data.items():
        try:
            best = float(stats["best"])
            avg = float(stats["average"])
            exercises.append(ex)
            best_scores.append(best)
            avg_scores.append(avg)
        except (ValueError, TypeError):
            continue  # Skip non-numeric entries like "2 min"

    if not exercises:
        messagebox.showinfo("No Numeric Data", "No numeric performance data to display.")
        return

    win = ctk.CTkToplevel()
    win.geometry("700x500")
    win.title("📊 Performance Graph")

    ctk.CTkLabel(win, text="📈 Best vs Average", font=("Arial", 18, "bold")).pack(pady=10)

    # Plot
    fig, ax = plt.subplots(figsize=(7, 4))
    x = range(len(exercises))

    ax.bar([i - 0.2 for i in x], best_scores, width=0.4, label="Best", color="blue")
    ax.bar([i + 0.2 for i in x], avg_scores, width=0.4, label="Average", color="green")

    ax.set_xticks(list(x))
    ax.set_xticklabels(exercises, rotation=45)
    ax.set_ylabel("Reps")
    ax.set_title("Exercise Performance")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    win.mainloop()