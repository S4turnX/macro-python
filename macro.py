import tkinter as tk
from tkinter import ttk, colorchooser
from pynput import keyboard
import time
import threading
import random

# Global variables
trigger_key = 'f'
action_key = 'e'
interval = 0.1
click_key = 'o'  # Default to 'O' key press

# Define the main application class
class AutoPressApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Saturn No Recoil")
        self.root.geometry("400x300")  # Smaller window size

        self.create_widgets()
        self.running = False

        # Initialize the floating balls
        self.balls = []
        self.create_balls()
        self.animate_balls()

    def create_widgets(self):
        # Set initial background color
        self.root.configure(bg='#34a4eb')  # Set background to blue color

        # Canvas for floating balls
        self.canvas = tk.Canvas(self.root, bg='#34a4eb', width=400, height=300, highlightthickness=0)
        self.canvas.grid(column=0, row=5, columnspan=2, padx=10, pady=10)

        # Style configuration for labels and entries
        style = ttk.Style()
        style.configure("TLabel", background='#34a4eb', foreground='white')
        style.configure("TEntry", fieldbackground='#34a4eb', background='#34a4eb', borderwidth=0, foreground='black')  # Transparent Entry

        # Trigger key
        ttk.Label(self.root, text="Trigger Key:", style="TLabel").grid(column=0, row=0, padx=10, pady=5, sticky='e')
        self.trigger_key_entry = ttk.Entry(self.root, width=2, style="TEntry")
        self.trigger_key_entry.insert(0, trigger_key)
        self.trigger_key_entry.grid(column=1, row=0, padx=10, pady=5)

        # Action key
        ttk.Label(self.root, text="Action Key:", style="TLabel").grid(column=0, row=1, padx=10, pady=5, sticky='e')
        self.action_key_entry = ttk.Entry(self.root, width=2, style="TEntry")
        self.action_key_entry.insert(0, action_key)
        self.action_key_entry.grid(column=1, row=1, padx=10, pady=5)

        # Interval
        ttk.Label(self.root, text="Interval (seconds):", style="TLabel").grid(column=0, row=2, padx=10, pady=5, sticky='e')
        self.interval_slider = ttk.Scale(self.root, from_=0.01, to=1.0, orient='horizontal', style="TScale")
        self.interval_slider.set(interval)
        self.interval_slider.grid(column=1, row=2, padx=10, pady=5)

        # Menu color change button
        ttk.Label(self.root, text="Menu Color:", style="TLabel").grid(column=0, row=3, padx=10, pady=5, sticky='e')
        self.menu_color_button = ttk.Button(self.root, text="Change Color", command=self.change_menu_color)
        self.menu_color_button.grid(column=1, row=3, padx=10, pady=5)

        # Start button
        self.start_button = ttk.Button(self.root, text="Start", command=self.start_script)
        self.start_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

    def create_balls(self):
        """Create mini floating balls and place them randomly on the canvas, covering the entire area."""
        for _ in range(15):  # Reduced number of balls for smaller window
            x = random.randint(0, 400)
            y = random.randint(0, 300)  # Randomly within the full height of the canvas
            size = random.randint(5, 10)  # Small balls
            ball = self.canvas.create_oval(x, y, x + size, y + size, fill='white', outline='white')
            self.balls.append((ball, x, y, size))

    def animate_balls(self):
        """Animate the floating balls."""
        for i, (ball, x, y, size) in enumerate(self.balls):
            dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
            dy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
            self.move_ball(ball, x, y, size, dx, dy)

    def move_ball(self, ball, x, y, size, dx, dy):
        """Move a ball around the canvas."""
        new_x = x + dx
        new_y = y + dy
        if new_x < 0 or new_x + size > 400:
            dx = -dx
        if new_y < 0 or new_y + size > 300:
            dy = -dy

        self.canvas.move(ball, dx, dy)
        self.root.after(10, self.move_ball, ball, new_x, new_y, size, dx, dy)

    def change_menu_color(self):
        """Change the menu background color using a color picker."""
        color = colorchooser.askcolor()[1]  # Get the hex color
        if color:
            self.root.configure(bg=color)
            self.canvas.configure(bg=color)
            style = ttk.Style()
            style.configure("TLabel", background=color)  # Update label background to match new color

    def start_script(self):
        self.trigger_key = self.trigger_key_entry.get()
        self.action_key = self.action_key_entry.get()
        self.interval = self.interval_slider.get()

        if not self.running:
            self.running = True
            threading.Thread(target=self.run_script, daemon=True).start()

    def run_script(self):
        def on_press(key):
            if hasattr(key, 'char') and key.char == self.trigger_key:
                self.running = True

        def on_release(key):
            if hasattr(key, 'char') and key.char == self.trigger_key:
                self.running = False

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            while True:
                if self.running:
                    keyboard.Controller().press(self.action_key)
                    keyboard.Controller().release(self.action_key)
                    keyboard.Controller().press(click_key)  # Default to 'O' key press
                    keyboard.Controller().release(click_key)
                    time.sleep(self.interval)
                else:
                    time.sleep(0.1)  # Reduce CPU usage

# Create the main window
root = tk.Tk()
app = AutoPressApp(root)
root.mainloop()

