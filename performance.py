import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import webbrowser

def show_performance():
    # Always find the file relative to this script
    file_path = os.path.join(os.path.dirname(__file__), "performance.json")
    if not os.path.exists(file_path):
        messagebox.showinfo("File Not Found", "performance.json file not found in the app directory.")
        return

    with open(file_path, "r") as f:
        data = json.load(f)

    # Separate numeric and time-based data
    numeric_exercises = []
    best_numeric = []
    avg_numeric = []

    time_exercises = []
    best_time = []
    avg_time = []

    def parse_time(value):
        if isinstance(value, str) and 'min' in value:
            try:
                return float(value.lower().replace('min', '').strip())
            except:
                return None
        try:
            return float(value)
        except:
            return None

    for ex, stats in data.items():
        best = parse_time(stats["best"])
        avg = parse_time(stats["average"])

        if best is not None and avg is not None:
            if isinstance(stats["best"], str) and 'min' in stats["best"].lower():
                time_exercises.append(ex)
                best_time.append(best)
                avg_time.append(avg)
            else:
                numeric_exercises.append(ex)
                best_numeric.append(best)
                avg_numeric.append(avg)

    if not numeric_exercises and not time_exercises:
        messagebox.showinfo("No Data", "No valid performance data to display.")
        return

    win = ctk.CTkToplevel()
    win.geometry("800x700")
    win.title("📊 Performance Graphs")

    ctk.CTkLabel(win, text="📈 Best vs Average", font=("Arial", 18, "bold")).pack(pady=10)

    fig, axs = plt.subplots(2, 1, figsize=(8, 6))

    # First graph: Numeric
    if numeric_exercises:
        x1 = range(len(numeric_exercises))
        axs[0].bar([i - 0.2 for i in x1], best_numeric, width=0.4, label="Best", color="blue")
        axs[0].bar([i + 0.2 for i in x1], avg_numeric, width=0.4, label="Average", color="green")
        axs[0].set_xticks(list(x1))
        axs[0].set_xticklabels(numeric_exercises, rotation=45)
        axs[0].set_ylabel("Reps")
        axs[0].set_title("Repetition-Based Performance")
        axs[0].legend()
        axs[0].grid(True, linestyle="--", alpha=0.5)

    # Second graph: Time
    if time_exercises:
        x2 = range(len(time_exercises))
        axs[1].clear()
        axs[1].plot(x2, best_time, color='purple', linestyle='-', marker='o', label='Best')
        axs[1].plot(x2, avg_time, color='orange', linestyle='-', marker='x', label='Average')
        axs[1].set_xticks(list(x2))
        axs[1].set_xticklabels(time_exercises, rotation=45)
        axs[1].set_ylabel("Minutes")
        axs[1].set_title("Time-Based Performance (Line Graph)")
        axs[1].legend()
        axs[1].grid(True, linestyle="--", alpha=0.5)

    # Add line graphs on top of bar charts
    if numeric_exercises:
        axs[0].plot(x1, best_numeric, color='black', linestyle='--', marker='o', label='Best (Line)')
        axs[0].plot(x1, avg_numeric, color='darkgreen', linestyle='--', marker='x', label='Avg (Line)')

    if time_exercises:
        axs[1].plot(x2, best_time, color='black', linestyle='--', marker='o', label='Best (Line)')
        axs[1].plot(x2, avg_time, color='darkorange', linestyle='--', marker='x', label='Avg (Line)')

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def save_chart():
        # Use timestamp and file dialog to save
        default_name = f"performance_chart_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
        save_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=default_name,
                                                 filetypes=[("PNG files", "*.png")])
        if save_path:
            fig.savefig(save_path)
            messagebox.showinfo("Saved", f"Chart saved to: {save_path}")
            try:
                webbrowser.open(save_path)
            except:
                pass

    ctk.CTkButton(win, text="💾 Save as Image", command=save_chart).pack(pady=10)

    win.mainloop()
