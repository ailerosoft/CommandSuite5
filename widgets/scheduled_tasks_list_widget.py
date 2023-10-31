import cv2
from PySide6.QtWidgets import (QListWidget, QListWidgetItem, QPushButton, QWidget, QHBoxLayout, QLabel, QVBoxLayout)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Signal, Qt


class ScheduledTasksListWidget(QListWidget):
    task_deleted = Signal(int)
    task_edit_requested = Signal(int)
    task_preview_requested = Signal(str)

    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        # Apply the background color stylesheet
        self.setStyleSheet("background-color: rgb(53, 53, 53);")

        # Connect signals to automatically refresh the display
        self.data_handler.task_added.connect(self.refresh_tasks)
        self.data_handler.task_deleted.connect(self.refresh_tasks)

        self.refresh_tasks()  # Initial display of tasks

    def display_tasks(self, tasks):
        self.clear()
        for task in tasks:
            item = QListWidgetItem(self)
            task_widget = QWidget()
            layout = QVBoxLayout(task_widget)

            # Thumbnail and Buttons
            thumbnail_layout = QHBoxLayout()

            thumbnail_label = QLabel()
            thumbnail_pixmap = self.get_thumbnail(task['video_path'])
            thumbnail_label.setPixmap(thumbnail_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            thumbnail_layout.addWidget(thumbnail_label)

            button_layout = QVBoxLayout()

            edit_button = QPushButton('Edit')
            edit_button.clicked.connect(lambda *args, tid=task['id']: self.edit_task(tid))
            button_layout.addWidget(edit_button)

            preview_button = QPushButton('Preview')
            preview_button.clicked.connect(lambda *args, vid_path=task['video_path']: self.preview_task(vid_path))
            button_layout.addWidget(preview_button)

            delete_button = QPushButton('X')
            delete_button.clicked.connect(lambda *args, tid=task['id']: self.delete_task(tid))
            button_layout.addWidget(delete_button)

            thumbnail_layout.addLayout(button_layout)
            layout.addLayout(thumbnail_layout)

            # Title and Date
            title_label = QLabel(f"Title: {task['title']}")
            layout.addWidget(title_label)

            date_label = QLabel(f"Scheduled for: {task['date']} {task['time']}")
            layout.addWidget(date_label)

            task_widget.setLayout(layout)
            item.setSizeHint(task_widget.sizeHint())
            self.setItemWidget(item, task_widget)

    def highlight_tasks_on_date(self, date):
        print(f"called highlight_tasks_on_date correctly:   Date:{date}")
        for i in range(self.count()):
            item = self.item(i)
            widget = self.itemWidget(item)
            task_date = widget.property('task_date')  # Get the date from the widget property
            if task_date == date.toString("yyyy-MM-dd"):
                item.setBackground(Qt.blue)
            else:
                item.setBackground(Qt.white)

    def edit_task(self, task_id):
        self.task_edit_requested.emit(task_id)

    def preview_task(self, video_path):
        self.task_preview_requested.emit(video_path)

    def delete_task(self, task_id):
        self.data_handler.delete_task(task_id)  # Delete task using DataHandler
        self.refresh_tasks()

    def refresh_tasks(self):
        tasks = self.data_handler.get_all_tasks()
        self.display_tasks(tasks)

    def get_thumbnail(self, video_path):
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()  # Read the first frame
        cap.release()

        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            return QPixmap.fromImage(q_image)
        else:
            return QPixmap()

    def connect_calendar(self, calendar_widget):
        calendar_widget.date_clicked.connect(self.highlight_tasks_on_date)

