
"""
Build Dynamic Timer for 3 minutes in the form of Pomodoro Technique
Use Tkinter for GUI
ToDo 1: create Tkinter GUI window using the pomodoro.png image as a background
ToDo 2: create a timer label and update it every second and the timer scoreboard should be displayed in the format of:
minutes:seconds
ToDo 3: create a start button that starts the timer and disables the start button
ToDo 4: create a reset button that resets the timer and scoreboard
ToDo 5: create a pause button that pauses the timer and disables the start and reset buttons
ToDo 6: create a save button that saves the current session's time and score
ToDo 7: create a load button that loads previous sessions and displays their times and scores
"""

import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

# CONSTANTS:
PINK = "#f7f5f7" # Grey background color
RED = "#f54254"
GREEN = "#fdfcff" # for the timer label
YELLOW = "#fdfcff" # Dark background color - for the Score label
FONT_NAME = "Arial"
WORK_MIN = 15 * 60  # 15 minutes in seconds
SHORT_BREAK_MIN = 5 * 60  # 5 minutes in seconds
LONG_BREAK_MIN = 10 * 60  # 10 minutes in seconds

class PomodoroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer for My Working Time")
        self.master.geometry("600x600")  # Set window size to match image size

        # Load background image
        self.bg_image = tk.PhotoImage(file="pomodoro.png")
        
        # Create canvas with background image
        self.canvas = tk.Canvas(master, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Timer label
        self.timer_label = self.canvas.create_text(330, 270, text="25:00", fill=GREEN, font=(FONT_NAME, 50, "bold"))

        # Scoreboard label
        self.scoreboard_label = self.canvas.create_text(330, 350, text="Score: 0", fill=YELLOW, font=(FONT_NAME, 30, "bold"))

        # Start button
        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button_window = self.canvas.create_window(200, 400, window=self.start_button)

        # Reset button
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer)
        self.reset_button_window = self.canvas.create_window(300, 400, window=self.reset_button)

        # Pause button
        self.pause_button = tk.Button(master, text="Pause", command=self.pause_timer, state=tk.DISABLED)
        self.pause_button_window = self.canvas.create_window(400, 400, window=self.pause_button)

        # Save button
        self.save_button = tk.Button(master, text="Save", command=self.save_session)
        self.save_button_window = self.canvas.create_window(250, 450, window=self.save_button)

        # Load button
        self.load_button = tk.Button(master, text="Load", command=self.load_sessions)
        self.load_button_window = self.canvas.create_window(350, 450, window=self.load_button)

        self.timer = None
        self.time_left = WORK_MIN
        self.is_paused = False
        self.score = 0

    def start_timer(self):
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.countdown()

    def reset_timer(self):
        if self.timer:
            self.master.after_cancel(self.timer)
        self.time_left = WORK_MIN
        self.score = 0
        self.update_timer_display()
        self.update_scoreboard()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def pause_timer(self):
        if self.is_paused:
            self.is_paused = False
            self.pause_button.config(text="Pause")
            self.countdown()
        else:
            self.is_paused = True
            self.pause_button.config(text="Resume")
            if self.timer:
                self.master.after_cancel(self.timer)

    def countdown(self):
        if not self.is_paused:
            if self.time_left > 0:
                self.time_left -= 1
                self.update_timer_display()
                self.timer = self.master.after(1000, self.countdown)
            else:
                self.score += 1
                self.update_scoreboard()
                messagebox.showinfo("Time's up!", "Take a break!")
                self.reset_timer()

    def update_timer_display(self):
        minutes, seconds = divmod(self.time_left, 60)
        self.canvas.itemconfig(self.timer_label, text=f"{minutes:02d}:{seconds:02d}")

    def update_scoreboard(self):
        self.canvas.itemconfig(self.scoreboard_label, text=f"Score: {self.score}")

    def save_session(self):
        session = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "time": self.time_left,
            "score": self.score
        }
        try:
            with open("pomodoro_sessions.json", "r") as file:
                sessions = json.load(file)
        except FileNotFoundError:
            sessions = []
        
        sessions.append(session)
        
        with open("pomodoro_sessions.json", "w") as file:
            json.dump(sessions, file)
        
        messagebox.showinfo("Session Saved", "Your current session has been saved.")

    def load_sessions(self):
        try:
            with open("pomodoro_sessions.json", "r") as file:
                sessions = json.load(file)
            
            sessions_info = "\n".join([f"Date: {s['date']}, Time: {s['time']}, Score: {s['score']}" for s in sessions])
            messagebox.showinfo("Previous Sessions", sessions_info)
        except FileNotFoundError:
            messagebox.showinfo("No Sessions", "No previous sessions found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
