#!/usr/bin/python3
"""
Retrieve employee TODO list progress using a REST API.
"""

import requests
import sys


def get_employee_todo_progress(employee_id):
    """
    Retrieves and displays employee TODO list progress.
    Args:
        employee_id (int): The employee ID.
    Returns:
        dict: TODO list information.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    user_url = f"{base_url}/users/{employee_id}"
    todos_url = f"{user_url}/todos"

    try:
        user_response = requests.get(user_url)
        todos_response = requests.get(todos_url)
        user_data = user_response.json()
        todos_data = todos_response.json()

        completed_tasks = [task for task in todos_data if task['completed']]
        total_tasks = len(todos_data)

        print(f"Employee {user_data['name']} is done with tasks "
              f"({len(completed_tasks)}/{total_tasks}):")

        for task in completed_tasks:
            print(f"\t{task['title']}")

        return {str(employee_id): [{"task": task['title'],
                                    "completed": task['completed'],
                                    "username": user_data['username']}
                                   for task in todos_data]}
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: ./script.py <employee_id>")
        sys.exit(1)

    employee_id = int(sys.argv[1])
    todo_data = get_employee_todo_progress(employee_id)

    # Exporting data to JSON file
    json_filename = f"{employee_id}.json"
    with open(json_filename, 'w') as json_file:
        json_file.write(str(todo_data))

    print(f"Data exported to {json_filename}")
