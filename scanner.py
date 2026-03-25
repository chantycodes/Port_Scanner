import socket
import threading
import tkinter as tk
from tkinter import messagebox

def scan_port(target, port):
    """Attempts to connect to a port and returns True if open."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    result = s.connect_ex((target, port))
    s.close()
    return result == 0

def scan_single_port(target, port):
    """Runs in a thread: scans one port and updates GUI."""
    if scan_port(target, port):
        output_box.insert(tk.END, f"Port {port} is OPEN\n", "open")
    else:
        output_box.insert(tk.END, f"Port {port} is CLOSED\n", "closed")

def start_scan():
    target = entry_target.get()

    try:
        start_port = int(entry_start.get())
        end_port = int(entry_end.get())
    except ValueError:
        messagebox.showerror("Error", "Port numbers must be integers")
        return

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Scanning {target}...\n", "info")

    # Launch a thread for each port
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_single_port, args=(target, port))
        thread.daemon = True
        thread.start()

# GUI Setup
root = tk.Tk()
root.title("Port Scanner")

tk.Label(root, text="Target IP:").grid(row=0, column=0)
entry_target = tk.Entry(root)
entry_target.grid(row=0, column=1)

tk.Label(root, text="Start Port:").grid(row=1, column=0)
entry_start = tk.Entry(root)
entry_start.grid(row=1, column=1)

tk.Label(root, text="End Port:").grid(row=2, column=0)
entry_end = tk.Entry(root)
entry_end.grid(row=2, column=1)

scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.grid(row=3, column=0, columnspan=2, pady=10)

output_box = tk.Text(root, height=15, width=45)
output_box.grid(row=4, column=0, columnspan=2)

# Text color tags
output_box.tag_config("open", foreground="green")
output_box.tag_config("closed", foreground="red")
output_box.tag_config("info", foreground="blue")

root.mainloop()
