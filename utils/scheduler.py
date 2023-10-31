import threading
import time
from datetime import datetime

class Scheduler:
    def __init__(self, data_handler, api_handler):
        self.data_handler = data_handler
        self.api_handler = api_handler
        self.run_scheduler()

    def run_scheduler(self):
        threading.Thread(target=self.execute_scheduled_tasks).start()

    def execute_scheduled_tasks(self):
        while True:
            tasks = self.data_handler.get_all_tasks()
            current_time = datetime.now()
            for task in tasks:
                # Combine date and time into a single datetime object for comparison
                scheduled_date_str = task['date'] + " " + task['time']
                scheduled_time = datetime.strptime(scheduled_date_str, '%Y-%m-%d %I:%M %p')

                if scheduled_time <= current_time:
                    self.api_handler.upload_video(task['video_path'],
                                                  task['title'])  # Assuming title is used as description
                    self.data_handler.delete_task(task['id'])  # Assuming tasks have an id
            time.sleep(60)

