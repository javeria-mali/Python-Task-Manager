
import json
import os

FILE_NAME = "tasks.json"

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

tasks = load_tasks()

print("==============================")
print("      MY TASK MANAGER")
print("==============================")

while True:
    print("\n1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter your task: ")
        tasks.append({"name": task, "completed": False})
        save_tasks()
        print("Task added successfully!")

    elif choice == "2":
        if not tasks:
            print("No tasks available.")
        else:
            print("\nYour Tasks:")
            for i, task in enumerate(tasks, start=1):
                status = "Completed" if task["completed"] else "Pending"
                print(f'{i}. {task["name"]} - {status}')

    elif choice == "3":
        if not tasks:
            print("No tasks to complete.")
        else:
            for i, task in enumerate(tasks, start=1):
                print(f'{i}. {task["name"]}')

            try:
                number = int(input("Enter task number to complete: "))
                if 1 <= number <= len(tasks):
                    tasks[number - 1]["completed"] = True
                    save_tasks()
                    print("Task marked as completed!")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")

    elif choice == "4":
        if not tasks:
            print("No tasks to delete.")
        else:
            for i, task in enumerate(tasks, start=1):
                print(f'{i}. {task["name"]}')

            try:
                number = int(input("Enter task number to delete: "))
                if 1 <= number <= len(tasks):
                    removed = tasks.pop(number - 1)
                    save_tasks()
                    print(f'Task "{removed["name"]}" deleted successfully!')
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")

    elif choice == "5":
        print("Thank you for using Task Manager!")
        break

    else:
        print("Invalid choice. Please try again.")
