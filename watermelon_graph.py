from matplotlib import pyplot as plt
import numpy as np
import tkinter as tk

root = tk.Tk()
root.title("Watermelon Graph")
entry = tk.Entry(root, width=50)
entry.pack(pady=20)
button = tk.Button(root, text="Render Watermelon Graph", command=lambda: render_graph())
button.pack(pady=20)

def render_graph():
    input_value = entry.get()
    avg_temps = np.array([float(f) for f in input_value.split(' ')])
    days = np.arange(1, len(avg_temps) + 1, 1)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.fill_between(days, avg_temps, alpha=0.3, color='red')
    ax.plot(days, avg_temps, marker='o', color='#2E7D32', linestyle='-', linewidth=15)
    
    # Add seeds (black dots) scattered inside the red filled area
    np.random.seed(123)
    num_seeds = 50
    seed_days = np.random.uniform(days.min(), days.max(), num_seeds)
    seed_temps = []
    
    # Generate random seeds within the filled area
    for day in seed_days:
        # Find position along the line
        idx = np.searchsorted(days, day)
        if idx >= len(avg_temps):
            idx = len(avg_temps) - 1
        if idx > 0:
            # Interpolate between points
            t = (day - days[idx-1]) / (days[idx] - days[idx-1]) if days[idx] != days[idx-1] else 0
            temp_at_day = avg_temps[idx-1] + t * (avg_temps[idx] - avg_temps[idx-1])
        else:
            temp_at_day = avg_temps[0]
        
        # Random height between 0 and the line value
        seed_temp = np.random.uniform(0, temp_at_day)
        seed_temps.append(seed_temp)
    
    ax.scatter(seed_days, seed_temps, color='black', s=30, marker='o', zorder=5, label='Seeds')
    
    ax.set_title("Average Monthly Temperatures in Ukraine (2023)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_xlabel("Day of Year")
    ax.legend(['Rind', 'Data'], loc='upper left')
    ax.grid()
    plt.show()

root.mainloop()
