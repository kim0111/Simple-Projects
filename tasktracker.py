import sys
import json
import os
from datetime import datetime
from tabulate import tabulate

TASKS_FILE = "tasks.json"


def load_tasks():
    """
    Reads the tasks from the JSON file.
    If the file doesn't exist, returns an empty structure.
    """
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []



def save_tasks(tasks):
    """
    Writes the tasks list/dictionary back to the JSON file.
    """
    try:
        with open(TASKS_FILE, "w") as file:
            json.dump(tasks, file, indent=4)
    except IOError as e:
        print(f"Error saving tasks: {e}")



def add_task(description):
    """
    1. Load current tasks.
    2. Generate a new ID.
    3. Create a task dictionary with timestamps.
    4. Append to data and save.
    """
    tasks = load_tasks()

    new_id = max([t['id'] for t in tasks], default=0) + 1

    now = datetime.now().strftime("%Y-%m-%d \n%H:%M:%S")
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added: {new_id}, description: {description}")



def update_task(task_id, new_description):
    """
    1. Load tasks.
    2. Find the task by ID.
    3. Update description and 'updatedAt' timestamp.
    4. Save.
    """
    tasks = load_tasks()
    found = False

    for task in tasks:
        if task['id'] == int(task_id):
            task['description'] = new_description
            task['updatedAt'] = datetime.now().strftime("%Y-%m-%d \n%H:%M:%S")
            found = True
            break

    if found:
        save_tasks(tasks)
        print(f"Task updated: {task_id}, description: {new_description}")
    else:
        print(f"Task not found: {task_id}")



def delete_task(task_id):
    """
    1. Load tasks.
    2. Remove the task with matching ID.
    3. Save.
    """
    tasks = load_tasks()
    # Create a new list excluding the ID we want to delete
    original_length = len(tasks)
    tasks = [t for t in tasks if t['id'] != int(task_id)]

    if len(tasks) < original_length:
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully")
    else:
        print(f"Error: Task {task_id} not found.")



def mark_status(task_id, status):
    """
    1. Load tasks.
    2. Update the status of the specific ID.
    3. Update 'updatedAt' timestamp and save.
    """
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == int(task_id):
            task['status'] = status
            task['updatedAt'] = datetime.now().strftime("%Y-%m-%d \n%H:%M:%S")
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}")
            return
    print(f"Error: Task {task_id} not found.")



def list_tasks(filter_status=None):
    """
    1. Load tasks.
    2. Filter based on status (if provided).
    3. Print tasks in a readable format.
    """
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    if filter_status:
        display_list = [t for t in tasks if t['status'] == filter_status]
    else:
        display_list = tasks

    if not display_list:
        print("No tasks found.")
        return

    print(tabulate(display_list, headers="keys", tablefmt="rounded_grid"))



def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli [action] [arguments]")
        return

    action = sys.argv[1]

    if action == "add":
        add_task(sys.argv[2])
    elif action == "list":
        list_tasks(sys.argv[2] if len(sys.argv) > 2 else None)
    elif action == "update":
        update_task(sys.argv[2], sys.argv[3])
    elif action == "delete":
        delete_task(sys.argv[2])
    elif action == "mark":
        mark_status(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown command: {action}")



if __name__ == "__main__":
    main()