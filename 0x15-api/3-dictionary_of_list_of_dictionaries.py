#!/usr/bin/python3
"""
Fetch and display TODO list progress for a given employee ID
"""

import requests
import sys


def fetch_todo_list(employee_id):
    """
    Fetch TODO list for a given employee ID from the specified REST API.
    Returns a list of completed tasks and total number of tasks.
    """
    url = f"https://jsonplaceholder.typicode.com/users/{employee_id}/todos"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: Unable to fetch TODO list for employee {employee_id}")
        sys.exit(1)

    todos = response.json()
    completed_tasks = [task for task in todos if task['completed']]

    return completed_tasks, len(todos)


def display_todo_progress(employee_name, completed_tasks, total_tasks):
    """
    Displaying the TODO list progress in the specified format.
    """
    print(f"Employee {employee_name} is done with tasks
         ({len(completed_tasks)}/{total_tasks}): ")
    for task in completed_tasks:
        print(f"\t{task['title']}")


def export_to_json(employee_data, filename):
    """
    Export employee TODO data to a JSON file.
    """
    import json
    with open(filename, 'w') as json_file:
        json.dump(employee_data, json_file, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <employee_id>")
        sys.exit(1)

    employee_id = int(sys.argv[1])

    completed_tasks, total_tasks = fetch_todo_list(employee_id)

    user_info_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    user_info = requests.get(user_info_url).json()
    employee_name = user_info['name']

    display_todo_progress(employee_name, completed_tasks, total_tasks)

    # Exporting to JSON
    all_employees_data = {str(employee_id): [{"username":
                                             user_info['username'],
            "task": task['title'], "completed": task['completed']}
        for task in completed_tasks]}
    export_to_json(all_employees_data, 'todo_all_employees.json')
