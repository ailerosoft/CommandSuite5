import json
import os
from PySide6.QtCore import QObject, Signal

DATA_FILE = "tasks_data.json"


class DataHandler(QObject):
    task_added = Signal(dict)
    task_deleted = Signal(int)

    def __init__(self):
        super().__init__()
        self.file_path = DATA_FILE
        if not os.path.exists(self.file_path):
            self.save_data([])

    def save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def add_task(self, task):
        data = self.load_data()
        task_id = self.generate_task_id(data)
        task['id'] = task_id
        data.append(task)
        self.save_data(data)
        self.task_added.emit(task)

    def delete_task(self, task_id):
        data = self.load_data()
        data = [task for task in data if task['id'] != task_id]
        self.save_data(data)
        self.task_deleted.emit(task_id)

    def load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            return data
        except json.JSONDecodeError:
            return []

    def get_all_tasks(self):
        return self.load_data()

    @property
    def scheduled_tasks(self):
        tasks = self.get_all_tasks()
        tasks_by_date = {}
        for task in tasks:
            date = task['date']
            if date not in tasks_by_date:
                tasks_by_date[date] = []
            tasks_by_date[date].append(task)
        return tasks_by_date

    def generate_task_id(self, data):
        ids = [task['id'] for task in data]
        new_id = max(ids, default=-1) + 1
        return new_id

    def edit_task(self, task_id, new_task):
        data = self.load_data()
        data[task_id] = new_task
        self.save_data(data)

    def get_task(self, task_id):
        data = self.load_data()
        # Iterating through tasks to find the one with the matching ID
        for task in data:
            if task['id'] == task_id:
                return task
        # Returning None if no task is found with the given ID
        return None

    def initial_setup(self):
        data = {"username": input("Enter your username: ")}

        print("Enter your API keys for the following platforms (or leave blank if you don't have one):")
        for platform in ["Facebook", "Twitter", "Instagram", "TikTok"]:
            key = input(f"{platform} API key: ")
            data[platform] = key

        self.save_data(data)

    def get_api_keys(self):
        data = self.load_data()
        return {platform: data[platform] for platform in ["Facebook", "Twitter", "Instagram", "TikTok"] if
                platform in data}




