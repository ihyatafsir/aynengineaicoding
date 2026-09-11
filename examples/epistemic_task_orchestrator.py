# Import necessary libraries
import threading
from typing import *
from collections import *

# Define the Governor class for task orchestration
class Governor:
    def __init__(self):
        self.tasks = {}
        self.lock = threading.Lock()

    # Method to add a new task with a unique identifier and priority
    def add_task(self, task_id: int, priority: int):
        with self.lock:
            if task_id in self.tasks:
                raise ValueError(f"Task {task_id} already exists")
            self.tasks[task_id] = {'priority': priority, 'state': 'Initializing'}

    # Method to update the state of a task
    def update_task_state(self, task_id: int, new_state: str):
        with self.lock:
            if task_id not in self.tasks:
                raise ValueError(f"Task {task_id} does not exist")
            self.tasks[task_id]['state'] = new_state

    # Method to execute a task
    def execute_task(self, task_id: int):
        with self.lock:
            if task_id not in self.tasks or self.tasks[task_id]['state'] != 'Initializing':
                raise ValueError(f"Task {task_id} is not initialized")
            self.tasks[task_id]['state'] = 'Active'
            # Simulate task execution
            print(f"Executing task {task_id}")
            # Simulate task completion
            self.update_task_state(task_id, 'Closed')

    # Method to cancel a task
    def cancel_task(self, task_id: int):
        with self.lock:
            if task_id not in self.tasks or self.tasks[task_id]['state'] != 'Active':
                raise ValueError(f"Task {task_id} is not active")
            self.update_task_state(task_id, 'Failed')

# Define the Task class for individual tasks
class Task:
    def __init__(self, id: int, priority: int):
        self.id = id
        self.priority = priority

# Example usage of the Governor and Task classes
if __name__ == "__main__":
    governor = Governor()
    
    # Add tasks with priorities
    governor.add_task(1, 3)
    governor.add_task(2, 1)
    governor.add_task(3, 2)
    
    # Execute tasks in order of priority
    while governor.tasks:
        for task_id, task_info in governor.tasks.items():
            if task_info['state'] == 'Initializing':
                governor.execute_task(task_id)
                break

# Output the final state of the tasks
for task_id, task_info in governor.tasks.items():
    print(f"Task {task_id}: State = {task_info['state']}")