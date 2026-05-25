import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Load Data
data_path = "career_stats.xlsx"
career_stats = pd.read_excel(data_path, sheet_name="Sheet1")

# Tkinter GUI
root = tk.Tk()
root.title("Toni Kroos Career Dashboard")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Plot Career Goals
figure = Figure(figsize=(8, 5), dpi=100)
ax = figure.add_subplot(111)
ax.plot(career_stats['Season'], career_stats['Goals'], marker='o', label="Goals")
ax.set_title("Goals by Season")
ax.set_xlabel("Season")
ax.set_ylabel("Goals")
ax.legend()

canvas = FigureCanvasTkAgg(figure, master=frame)
canvas.get_tk_widget().grid(row=0, column=0)

# Run Tkinter Event Loop
root.mainloop()
