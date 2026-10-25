import tkinter as tk
import csv
import os
import sys

# Get the exact directory where this .exe (or .py) is running from
if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable) # If running as .exe
else:
    current_dir = os.path.dirname(os.path.abspath(__file__)) # If running as .py

# Define absolute paths for our files
csv_path = os.path.join(current_dir, "ActorDump.csv")
cmd_path = os.path.join(current_dir, "cmd.txt")

def spawn_item(name, path):
    with open(cmd_path, "w") as f:
        f.write(f"{name}|{path}")

# Load the CSV
items = []
try:
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader) # Skip header
        for row in reader:
            if len(row) >= 2:
                items.append({"name": row[0].strip(), "path": row[1].strip()})
except Exception as e:
    items.append({"name": "ERROR: Could not load ActorDump.csv", "path": ""})

# Setup the Window
root = tk.Tk()
root.title("Militsioner Spawner -pacmanninja998")
root.geometry("400x500")
root.attributes("-topmost", True)

def update_list(event=None):
    search_term = search_var.get().lower()
    listbox.delete(0, tk.END)
    for item in items:
        if search_term in item["name"].lower():
            listbox.insert(tk.END, item["name"])

tk.Label(root, text="Search Item:").pack(pady=5)
search_var = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack(fill=tk.X, padx=10)
search_entry.bind("<KeyRelease>", update_list)

listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

update_list()

def on_spawn():
    selection = listbox.curselection()
    if selection:
        selected_name = listbox.get(selection[0])
        for item in items:
            if item["name"] == selected_name:
                spawn_item(item["name"], item["path"])
                break

tk.Button(root, text="SPAWN IN GAME", command=on_spawn, bg="green", fg="white", height=2).pack(fill=tk.X, padx=10, pady=10)

root.mainloop()
