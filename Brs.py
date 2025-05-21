import tkinter as tk
import time
import subprocess
import threading


def get_process_list():
    result = subprocess.run(['tasklist'], capture_output=True, text=True)
    processes = result.stdout.splitlines()
    process_dict = {}
    for process in processes[3:]:  # Skip the header lines
        if process.strip():
            parts = process.split()
            try:
                pid = int(parts[1])
                name = parts[0]
                if name.lower() != 'tasklist.exe':  # Ignore tasklist itself
                    process_dict[pid] = name
            except ValueError:
                continue  # Skip lines where PID is not an integer
    return process_dict


def monitor_processes():
    previous_processes = get_process_list()
    while True:
        time.sleep(3)
        current_processes = get_process_list()
        new_processes = {pid: name for pid, name in current_processes.items() if pid not in previous_processes}

        if new_processes:
            for pid, name in new_processes.items():
                print(f"New process detected: {name} (PID: {pid})")
                threading.Thread(target=start_countdown, args=(pid, name)).start()

        previous_processes = current_processes
# THIS SHOULDNT WORK BUT IT DOES FOR SOME REASON 🔥🔥🔥

def start_countdown(pid, name):
    try:
        seconds = int(entry.get())
        print(f"Counting down from {seconds} seconds for process {name} (PID: {pid})...")
        for i in range(seconds, 0, -1):
            time.sleep(1)
            print(f"{i} seconds remaining")
        print(f"Time's up! Terminating process {name} (PID: {pid})...")
        subprocess.run(['taskkill', '/PID', str(pid), '/F'])
    except ValueError:
        print("Please enter a valid number.")
# note to self: figure out how to stop the seconds remaining from looping onto itself

# window lore
root = tk.Tk()
root.title("BRS (version 1.0.0)")
root.geometry("300x200")

label = tk.Label(root, text="Enter time (seconds):", font=("Arial", 12))
label.pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=5)

button = tk.Button(root, text="Set Timer", command=lambda: print(f"Timer set to {entry.get()} seconds."))
button.pack(pady=10)
# lambda my beloathed, i hate you exist but you're so useful

# threading lore
process_thread = threading.Thread(target=monitor_processes, daemon=True)
process_thread.start()

root.mainloop()
