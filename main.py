
from matplotlib import pyplot as plt
import numpy as np
import tkinter as tk

root = tk.Tk()
root.title("User Input Graph")
entry = tk.Entry(root, width=50)
entry.pack(pady=20)
button = tk.Button(root, text="Render Graph", command=lambda: render_graph())
button.pack(pady=20)

def render_graph():
    input_value = entry.get()
    avg_temps = np.array([float(f) for f in input_value.split(' ')])  # Parse comma-separated values
    days = np.arange(1, len(avg_temps) + 1, 1)
    plt.figure(figsize=(10, 5))
    plt.fill_between(days, avg_temps, alpha=0.3, color='lightblue')
    plt.plot(days, avg_temps, marker='o', color='blue', linestyle='-')
    plt.title("Average Monthly Temperatures in Ukraine (2023)")
    plt.ylabel("Temperature (°C)")
    plt.xlabel("Day of Year")
    plt.grid()

    plt.show()

root.mainloop()


# Generate 100 random data points along 3 dimensions
x, y, scale = np.random.randn(1, 100)
fig, ax = plt.subplots()

# Map each onto a scatterplot we'll create with Matplotlib
ax.scatter(x=x, y=y, c=scale, s=np.abs(scale)*500)
ax.set(title="Some random data, created with JupyterLab!")

# build a simple line graph 
x = np.linspace(0, 2, 10)  # Sample data.
# ya zdyvovanyi
plt.figure(figsize=(5, 2.7), layout='constrained')
plt.plot(x, x, label='linear')  # Plot some data on the (implicit) Axes.
plt.plot(x, x**2, label='quadratic')  # etc.
plt.plot(x, x**3, label='cubic')
plt.plot(x, x**2, label='parabola', color='purple')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Simple Plot")
plt.legend()


# add input for user to enter data
# render graph in the tkinter window 

import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Simple Tkinter App")
# ya dobryi

#message box must display user input
def show_message():
    user_input = entry.get()
    messagebox.showinfo("Message", f"{user_input}")
#end of message box display

button = tk.Button(root, text="Click Me", command=show_message)
button.pack(pady=100)

#add user input 
entry = tk.Entry(root, width=50)
entry.pack(pady=20)
#end of user input

# Center the window on the screen
window_width = 900
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2)) 
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
#end of centering window

root.mainloop()






























