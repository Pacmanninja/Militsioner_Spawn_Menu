import tkinter as tk
from tkinter import ttk
import csv
import os
import sys

# Get the exact directory where this .exe (or .py) is running from
if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable)  # If running as .exe
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))  # If running as .py

# Define absolute paths for our files
csv_path = os.path.join(current_dir, "Dump.csv")
cmd_path = os.path.join(current_dir, "cmd.txt")

def spawn_item(name, path):
    with open(cmd_path, "w") as f:
        f.write(f"{name}|{path}")

# Load the CSV
items_by_category = {}
item_data = {}

try:
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter='\t')
        headers = next(reader) # Skip header
        current_category = "Uncategorized"

        for row in reader:
            if not row or not any(row):
                continue

            # If the first column has text but second doesn't, it's a category
            if row[0] and (len(row) < 2 or not row[1]):
                current_category = row[0].strip()
                if current_category not in items_by_category:
                    items_by_category[current_category] = []
            # If second column has text, it's an item
            elif len(row) >= 3 and row[1]:
                name = row[1].strip()
                path = row[2].strip()
                comment = row[3].strip() if len(row) >= 4 else ""

                # Make sure the category exists in our dict
                if current_category not in items_by_category:
                    items_by_category[current_category] = []

                items_by_category[current_category].append(name)
                item_data[name] = {"path": path, "comment": comment}

except Exception as e:
    print(f"Error loading CSV: {e}")

# Setup the Window
root = tk.Tk()
root.title("Militsioner Spawner -pacmanninja998")
root.geometry("500x600")
root.attributes("-topmost", True)

def on_tree_select(event):
    selection = tree.selection()
    if selection:
        item = tree.item(selection[0])
        # Check if it's a leaf node (actual item, not category)
        if not tree.get_children(selection[0]):
            name = item['text']
            if name in item_data:
                comment = item_data[name]["comment"]
                comment_var.set(f"Note: {comment}" if comment else "")
            else:
                comment_var.set("")
        else:
            comment_var.set("")

def filter_tree(event=None):
    search_term = search_var.get().lower()

    # Clear the tree
    for item in tree.get_children():
        tree.delete(item)

    # Re-populate based on search
    for category, items in items_by_category.items():
        # Check if category matches or any item in it matches
        matching_items = [item for item in items if search_term in item.lower()]

        if search_term in category.lower() or matching_items:
            cat_id = tree.insert("", tk.END, text=category, open=True)

            # If category matches, show all items. Otherwise show only matching items.
            items_to_show = items if search_term in category.lower() else matching_items

            for item in items_to_show:
                tree.insert(cat_id, tk.END, text=item)

# UI Elements
tk.Label(root, text="Search Item/Category:").pack(pady=5)
search_var = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack(fill=tk.X, padx=10)
search_entry.bind("<KeyRelease>", filter_tree)

# Create Treeview
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = ttk.Scrollbar(tree_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set, show="tree")
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=tree.yview)

tree.bind("<<TreeviewSelect>>", on_tree_select)

# Initial population
filter_tree()

# Comment display
comment_var = tk.StringVar()
comment_label = tk.Label(root, textvariable=comment_var, fg="gray", wraplength=480, justify="left")
comment_label.pack(fill=tk.X, padx=10, pady=5)

def on_spawn():
    selection = tree.selection()
    if selection:
        item = tree.item(selection[0])
        # Check if it's a leaf node (actual item)
        if not tree.get_children(selection[0]):
            name = item['text']
            if name in item_data:
                spawn_item(name, item_data[name]["path"])

tk.Button(root, text="SPAWN IN GAME", command=on_spawn, bg="green", fg="white", height=2).pack(fill=tk.X, padx=10, pady=10)

root.mainloop()
