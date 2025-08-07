import customtkinter as ctk
from auth import show_login_page

def show_welcome_page():
    welcome_win = ctk.CTk()
    welcome_win.geometry("500x400")
    welcome_win.title("Welcome")

    ctk.CTkLabel(welcome_win, text="🏋️‍♂️ Welcome to Your Fitness Assistant", font=("Arial", 20, "bold")).pack(pady=40)
    ctk.CTkLabel(welcome_win, text="Track your daily exercises\nand stay healthy!", font=("Arial", 16)).pack(pady=20)
    ctk.CTkButton(welcome_win, text="👉 Continue to Login", font=("Arial", 14), command=lambda: [welcome_win.destroy(), show_login_page()]).pack(pady=30)

    welcome_win.mainloop()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    show_welcome_page()
