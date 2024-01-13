#!/usr/bin/python3
"""Fetch and display employee TODO list progress."""

import requests
from sys import argv

if __name__ == "__main__":
    if len(argv) != 2 or not argv[1].isdigit():
        print("Usage: ./0-gather_data_from_an_API.py <employee_id>")
    else:
        employee_id = int(argv[1])

        # Fetches user data
        user_info = requests.get(
            f'https://jsonplaceholder.typicode.com/users/{employee_id}'
        ).json()

        # Fetches TODO list
        todo_list = requests.get(
            f'https://jsonplaceholder.typicode.com/todos?userId={employee_id}'
        ).json()

        # Calculating the  progress
        total_tasks = len(todo_list)
        done_tasks = [task for task in todo_list if task.get('completed')]
        num_done_tasks = len(done_tasks)

        # Displays information
        print(f"Employee {user_info.get('name')} is done with tasks"
              f"({num_done_tasks}/{total_tasks}):")

        for task in done_tasks:
            print(f"\t{task.get('title')}")
