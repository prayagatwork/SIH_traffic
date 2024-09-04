import tkinter as tk
import time
from threading import Thread

# Global variables for light control
current_green = 0  # Start with the first light
min_green_time = 3  # Minimum green light time for each lane
lights = []  # Store the traffic light labels
timers = []  # Store the timer labels
root = None  # Global reference to the main Tkinter window
entries = []  # Store the Entry widgets for vehicle counts
max_t=30

# Function to read vehicle counts from the Entry widgets
def detect_vehicles():
    vehicle_counts = []
    for entry in entries:
        count = int(entry.get())
        vehicle_counts.append(count)
    return vehicle_counts

# Function to change the light color for the given index
def change_light(index, color):
    for i in range(4):
        lights[i].config(bg='red' if i != index else color)

# Function to update the timer label for the current green light
def update_timer_label(index, time_left):
    timers[index].config(text=f"Time left: {time_left}s")

# Main function to handle the traffic light cycles
def start_cycle():
    global current_green,max_t

    while True:
        vehicle_counts = detect_vehicles()  # Get vehicle counts from the Entry widgets
        print("Vehicle counts:", vehicle_counts)  # Print vehicle counts

        # total_vehicles = sum(vehicle_counts)
        
        # Calculate green time for each lane based on its vehicle count
        green_time = min(max_t, vehicle_counts[current_green]+2)

        # Cycle through each lane
        change_light(current_green, 'green')
        for t in range(green_time, 0, -1):
            update_timer_label(current_green, t)
            root.update()
            time.sleep(1)
        change_light(current_green, 'red')
        update_timer_label(current_green, 0)
        current_green = (current_green + 1) % 4  # Move to the next road

# Main function to set up the GUI and start the traffic system
def main():
    global lights, root, entries, timers

    # Create main Tkinter window
    root = tk.Tk()
    root.title("AI Traffic Management System")
    root.geometry("800x400")

    # Create labels representing traffic lights
    lights = [
        tk.Label(root, width=10, height=5, bg='red'),
        tk.Label(root, width=10, height=5, bg='red'),
        tk.Label(root, width=10, height=5, bg='red'),
        tk.Label(root, width=10, height=5, bg='red')
    ]

    # Create labels for the timers
    timers = [
        tk.Label(root, text="Time left: 0s"),
        tk.Label(root, text="Time left: 0s"),
        tk.Label(root, text="Time left: 0s"),
        tk.Label(root, text="Time left: 0s")
    ]

    # Position the lights and timers in a 2x2 grid
    for i in range(4):
        lights[i].place(x=50 + i * 200, y=50)
        timers[i].place(x=50 + i * 200, y=150)

    # Create Entry widgets for vehicle counts
    for i in range(4):
        entry = tk.Entry(root)
        entry.place(x=50 + i * 200, y=200)
        entry.insert(0, "0")  # Default value
        entries.append(entry)

    # Start the cycle in a separate thread
    cycle_thread = Thread(target=start_cycle)
    cycle_thread.daemon = True
    cycle_thread.start()

    # Run the Tkinter event loop
    root.mainloop()

# Start the traffic management system
main()
