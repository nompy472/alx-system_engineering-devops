#!/usr/bin/python3
"""
Module documentation goes here.
"""

import csv
import requests
import sys


def fetch_todo_list(employee_id):
    """
    Fetche and returns the employee's TODO list.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    user_url = f"{base_url}/users/{employee_id}"
    todos_url = f"{base_url}/todos?userId={employee_id}"

    try:
        user_response = requests.get(user_url)
        user_data = user_response.json()
        todos_response = requests.get(todos_url)
        todos_data = todos_response.json()
        return user_data, todos_data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)


def display_progress(user_data, todos_data):
    """
    Displaying employee TODO list progress on the standard output.
    """
    employee_name = user_data.get("name")
    total_tasks = len(todos_data)
    completed_tasks = [task for task in todos_data if task.get("completed")]

    print(f"Employee {employee_name} is done with tasks"
          f"({len(completed_tasks)}/{total_tasks}):")

    for task in completed_tasks:
        print(f"\t{task['title']}")


def export_to_csv(employee_id, user_data, todos_data):
    """
    Exporting TODO list data to CSV file.
    """
    file_name = f"{employee_id}.csv"
    fieldnames = ["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"]

    with open(file_name, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for task in todos_data:
            writer.writerow({
                "USER_ID": employee_id,
                "USERNAME": user_data.get("username"),
                "TASK_COMPLETED_STATUS": str(task["completed"]),
                "TASK_TITLE": task["title"]
            })


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <employee_id>")
        sys.exit(1)

    employee_id = int(sys.argv[1])
    user_data, todos_data = fetch_todo_list(employee_id)

    display_progress(user_data, todos_data)
    export_to_csv(employee_id, user_data, todos_data)
