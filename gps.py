import tkinter as tk
from tkinter import ttk
import serial
import threading
import re
import math

# Set up the serial line
ser = serial.Serial('COM5', 9600)
ser.flushInput()

# Define the tkinter window
root = tk.Tk()
root.title("GPS and Magnetometer Data")

# Define tkinter variables
location = tk.StringVar()
dateTime = tk.StringVar()
heading = tk.DoubleVar()

# Create labels
ttk.Label(root, text="Location:").grid(column=0, row=0, sticky='W')
ttk.Label(root, text="Date/Time:").grid(column=0, row=1, sticky='W')

# Create the text fields
ttk.Label(root, textvariable=location).grid(column=1, row=0, sticky='W')
ttk.Label(root, textvariable=dateTime).grid(column=1, row=1, sticky='W')

# Create a canvas for the compass
compass_canvas = tk.Canvas(root, width=300, height=300)
compass_canvas.grid(column=0, row=2, columnspan=2)

# Draw the compass circle
compass_canvas.create_oval(50, 50, 250, 250, width=2)

# Draw the cardinal direction labels
compass_canvas.create_text(150, 30, text="N", font=("Arial", 14, "bold"))
compass_canvas.create_text(150, 270, text="S", font=("Arial", 14, "bold"))
compass_canvas.create_text(30, 150, text="W", font=("Arial", 14, "bold"))
compass_canvas.create_text(270, 150, text="E", font=("Arial", 14, "bold"))

# Create a text label for the heading
heading_label = ttk.Label(root, textvariable=heading, font=("Arial", 24))
heading_label.grid(column=0, row=3, columnspan=2)

# Function to update the compass
def update_compass(heading_deg):
    # Convert heading from degrees to radians
    heading_rad = math.radians(heading_deg)

    # Calculate the center and radius of the compass
    cx = 150
    cy = 150
    radius = 100

    # Calculate the position of the needle
    x_end = cx + radius * math.sin(heading_rad)
    y_end = cy - radius * math.cos(heading_rad)
    
    # Update the needle
    compass_canvas.delete("needle")
    compass_canvas.create_line(cx, cy, x_end, y_end, fill="red", width=2, tags="needle")

    # Update the heading label
    heading.set(f"{heading_deg:.1f}°")

# Function to read serial data
def readSerial():
    global stop_thread
    while True:
        if stop_thread:
            break
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            data = re.split(r'\s{2,}', line)
            
            if len(data) == 4: # Here, we expect four sets of data - Location, DateTime, and Filtered Magnetometer Data
                location.set(data[0].split(': ')[1])
                dateTime.set(data[1].split(': ')[1])
                
                magnetometer_data = list(map(float, data[3].split(': ')[1].split(','))) # Here, we read the filtered magnetometer data
                heading_rad = math.atan2(magnetometer_data[1], magnetometer_data[0])
                heading_deg = math.degrees(heading_rad)

                if heading_deg < 0:
                    heading_deg += 360
                
                heading.set(f"{heading_deg:.1f}°")
                update_compass(heading_deg)

# Start a thread to read the serial data
serial_thread = threading.Thread(target=readSerial)
serial_thread.start()

# Try to ensure graceful exit
try:
    root.mainloop()
except KeyboardInterrupt:
    stop_thread = True  # Set flag to stop thread
    serial_thread.join()  # Wait for thread to finish
    ser.close()  # Close the serial connection
    root.destroy()  # Close the GUI
