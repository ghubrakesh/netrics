import tkinter as tk
import psutil
import emoji
import winreg
import sys
import os
import ctypes

# Function to add the application to startup
def add_to_startup():
    # Get the path to the current script
    script_path = os.path.abspath(sys.argv[0])

    # Open the "Run" registry key
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS)

    # Add the application to the "Run" registry key
    winreg.SetValueEx(key, "Netrics", 0, winreg.REG_SZ, script_path)

    # Close the registry key
    winreg.CloseKey(key)

window = tk.Tk()
window.title("Netrics")
window.overrideredirect(1)  # Remove window decorations (minimize, maximize, close buttons)
window.attributes('-topmost', True)
window.configure(bg='#071013')  # Set background color of the window to black

# Define fonts
emoji_font = ("Segoe UI Emoji", 24, "bold")
speed_font = ("Roboto", 8, "bold")

download_label = tk.Label(window, text=emoji.emojize(":down_arrow:"), fg="yellow", bg='#1c2321', font=emoji_font)
upload_label = tk.Label(window, text=emoji.emojize(":up_arrow:"), fg="purple",bg='#7d98a4', font=emoji_font)

download_label.grid(row=0, column=0, sticky="w")
upload_label.grid(row=1, column=0, sticky="w")

last_download_bytes = psutil.net_io_counters().bytes_recv
last_upload_bytes = psutil.net_io_counters().bytes_sent

def format_speed(speed):
    if speed >= 1024:
        return f"{speed/1024:.2f} MB/s "
    else:
        return f"{speed:.2f} KB/s "

def update_speeds():
    global last_download_bytes, last_upload_bytes

    current_download_bytes = psutil.net_io_counters().bytes_recv
    current_upload_bytes = psutil.net_io_counters().bytes_sent

    download_speed = (current_download_bytes - last_download_bytes) / 1024
    upload_speed = (current_upload_bytes - last_upload_bytes) / 1024

    download_label.config(text=emoji.emojize(f":down_arrow:{format_speed(download_speed)}"), font=speed_font)
    upload_label.config(text=emoji.emojize(f":up_arrow:{format_speed(upload_speed)}"), font=speed_font)

    last_download_bytes = current_download_bytes
    last_upload_bytes = current_upload_bytes

    window.after(1000, update_speeds)

window.after(1000, update_speeds)  # Call update_speeds after 1 second

# Variables to store mouse drag start position
start_x = None
start_y = None

# Event handlers for mouse drag
def on_drag_start(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def on_drag_motion(event):
    global start_x, start_y
    x = window.winfo_x() + (event.x - start_x)
    y = window.winfo_y() + (event.y - start_y)
    window.geometry(f"+{x}+{y}")

def go_back():
    menu.unpost()  # Hide the option window

def close_window():
    window.destroy()  # Close the application window

def on_right_click(event):
    global menu
    # Create a right-click menu
    menu = tk.Menu(window, tearoff=0, bg="#333333", fg="white", borderwidth=1, relief="solid")  # Set border attributes
    menu.configure(activebackground="#555555", activeforeground="white")  # Set active colors
    menu.add_command(label="Go Back", command=go_back)
    menu.add_command(label="Close Meter", command=close_window)
    menu.post(event.x_root, event.y_root)

# Bind event handlers to window
window.bind("<ButtonPress-1>", on_drag_start)
window.bind("<B1-Motion>", on_drag_motion)
window.bind("<Button-3>", on_right_click)  # Right-click event

# Calculate the screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the position to place the window at the left middle side
x_position = 0
y_position = (screen_height - window.winfo_height()) // 2

window.geometry(f"+{x_position + 50}+{y_position+200}")

# Add application to startup
add_to_startup()

# Set the task manager application name
if sys.argv[0].endswith('.py'):
    sys.argv[0] = sys.argv[0].replace('.py', '.exe')

ctypes.windll.kernel32.SetConsoleTitleW("Netrics")

window.mainloop()
