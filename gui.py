
import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"
tasks = []

def load_tasks():
    global tasks
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                tasks = json.load(file)
        except (json.JSONDecodeError, OSError):
            tasks = []

def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

def refresh_tasks():
    task_list.delete(0, tk.END)

    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        task_list.insert(
            tk.END, f'{task["name"]} - {status}'
        )

def add_task():
    name = task_entry.get().strip()

    if not name:
        messagebox.showwarning("Warning", "Please enter a task!")
        return

    tasks.append({"name": name, "completed": False})
    save_tasks()
    refresh_tasks()
    task_entry.delete(0, tk.END)

def complete_task():
    selected = task_list.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a task first!")
        return

    tasks[selected[0]]["completed"] = True
    save_tasks()
    refresh_tasks()

def delete_task():
    selected = task_list.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a task first!")
        return

    tasks.pop(selected[0])
    save_tasks()
    refresh_tasks()

load_tasks()

root = tk.Tk()
root.title("My Task Manager")
root.geometry("550x520")
root.configure(bg="#F4EEFF")

title = tk.Label(
    root,
    text="MY TASK MANAGER",
    font=("Arial", 22, "bold"),
    bg="#F4EEFF",
    fg="#6236A0"
)
title.pack(pady=20)

task_entry = tk.Entry(
    root,
    font=("Arial", 13),
    width=35
)
task_entry.pack(pady=10)

add_button = tk.Button(
    root,
    text="Add Task",
    command=add_task,
    bg="#805AD5",
    fg="white",
    font=("Arial", 11, "bold"),
    width=18
)
add_button.pack(pady=5)

task_list = tk.Listbox(
    root,
    font=("Arial", 12),
    width=43,
    height=12,
    selectbackground="#805AD5"
)
task_list.pack(pady=15)

complete_button = tk.Button(
    root,
    text="Mark as Completed",
    command=complete_task,
    bg="#38A169",
    fg="white",
    font=("Arial", 10, "bold"),
    width=20
)
complete_button.pack(pady=4)

delete_button = tk.Button(
    root,
    text="Delete Task",
    command=delete_task,
    bg="#E53E3E",
    fg="white",
    font=("Arial", 10, "bold"),
    width=20
)
delete_button.pack(pady=4)

refresh_tasks()

root.mainloop()
