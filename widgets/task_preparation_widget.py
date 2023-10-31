from PySide6.QtWidgets import (QWidget, QPushButton, QLineEdit, QVBoxLayout, QColorDialog, QFileDialog, QMessageBox)
from PySide6.QtCore import Signal, QUrl, QDate
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget


class TaskPreparationWidget(QWidget):

    def __init__(self, data_handler):
        super().__init__()

        self.data_handler = data_handler

        self.video_path = ""
        self.task_color = ""
        self.media_player = QMediaPlayer()

        # Initialize UI elements
        self.init_ui()

        # Connect to data handler signals
        self.data_handler.task_added.connect(self.on_task_added)
        self.data_handler.task_deleted.connect(self.on_task_deleted)

    def init_ui(self):
        print("Initializing UI elements in TaskPreparationWidget...")

        layout = QVBoxLayout()

        # Row for New Task and Save Task buttons
        self.new_task_button = QPushButton("New Task")
        self.new_task_button.clicked.connect(self.on_new_task_button_clicked)

        self.save_task_button = QPushButton("Save Task")
        self.save_task_button.clicked.connect(self.on_save_task_button_clicked)

        layout.addWidget(self.new_task_button)
        layout.addWidget(self.save_task_button)

        # Row for Title, Date, and Time
        self.title_input = QLineEdit(placeholderText="Title")
        self.date_input = QLineEdit(placeholderText="10/01/23")
        self.time_input = QLineEdit(placeholderText="10:00 AM")

        layout.addWidget(self.title_input)
        layout.addWidget(self.date_input)
        layout.addWidget(self.time_input)

        # Row for Video, Color, and Add to Schedule button
        self.video_button = QPushButton("Choose File")
        self.video_button.clicked.connect(self.on_video_button_clicked)

        self.color_button = QPushButton()
        self.color_button.clicked.connect(self.on_color_button_clicked)

        self.add_to_schedule_button = QPushButton("Add to Schedule")
        self.add_to_schedule_button.clicked.connect(self.on_save_task_button_clicked)

        layout.addWidget(self.video_button)
        layout.addWidget(self.color_button)
        layout.addWidget(self.add_to_schedule_button)

        # Video Preview
        self.video_preview = QVideoWidget()
        self.media_player.setVideoOutput(self.video_preview)
        layout.addWidget(self.video_preview)

        self.setLayout(layout)

        print("UI elements in TaskPreparationWidget initialized successfully.")

    def handle_media_error(self):
        """Handle any error that occurs during media playback."""
        error_message = self.media_player.errorString()
        QMessageBox.warning(self, "Media Player Error", error_message)

    def on_save_task_button_clicked(self):
        """Saves the current task details."""
        if self.validate_fields():
            # Convert date to QDate object
            date_obj = QDate.fromString(self.date_input.text(), 'MM/dd/yy')

            # Adjust year to 2000s if it defaults to 1900s
            if date_obj.year() < 2000:
                date_obj = date_obj.addYears(100)

            # Convert date to yyyy-MM-dd format
            date = date_obj.toString('yyyy-MM-dd')

            task_data = {
                'title': self.title_input.text(),
                'date': date,
                'time': self.time_input.text(),
                'video_path': self.video_path,
                'color': self.task_color
            }
            self.data_handler.add_task(task_data)  # Directly add task through data handler

    def load_task_for_editing(self, task_id):
        """Populate the widget fields with the data of the task to be edited."""
        task_data = self.data_handler.get_task(task_id)  # Fetching task data using task ID

        if task_data:
            self.title_input.setText(task_data['title'])

            # Convert date to MM/dd/yy format
            date = QDate.fromString(task_data['date'], 'yyyy-MM-dd').toString('MM/dd/yy')

            self.date_input.setText(date)
            self.time_input.setText(task_data['time'])
            self.video_path = task_data['video_path']
            self.task_color = task_data['color']

            # Load and pause the video to show the first frame
            self.media_player.setSource(QUrl.fromLocalFile(self.video_path))
            self.media_player.play()

            # Set the task color button background
            self.color_button.setStyleSheet(f"background-color: {self.task_color}")

    def preview_video(self, video_path):
        """Load and play the video for preview."""
        print("signal for preview_video called correctly...")
        self.media_player.setSource(QUrl.fromLocalFile(video_path))
        self.media_player.play()

    def connect_task_list(self, task_list_widget):
        """Connect signals from the task list widget."""
        task_list_widget.task_edit_requested.connect(self.load_task_for_editing)
        task_list_widget.task_preview_requested.connect(self.preview_video)
        print("connected the task list signals...")

    def on_new_task_button_clicked(self):
        """Clears all fields to prepare for a new task entry."""
        self.title_input.clear()
        self.date_input.clear()
        self.time_input.clear()
        self.video_path = ""
        self.task_color = ""
        self.media_player.setSource(QUrl())  # Updated this line to clear the media player
        self.media_player.stop()  # Stop the media player

    def on_video_button_clicked(self):
        """Opens a dialog to choose a video file and previews it."""
        video_path, _ = QFileDialog.getOpenFileName(self, "Open Video File")
        if video_path:
            self.video_path = video_path
            video_url = QUrl.fromLocalFile(video_path)

            if video_url.isValid():
                self.media_player.setSource(video_url)  # Updated this line
                self.media_player.play()
            else:
                QMessageBox.warning(self, "Invalid URL", "The chosen file could not be loaded as a valid media URL.")

    def validate_fields(self):
        """Validate the input fields."""
        return all([self.title_input.text().strip(),
                    self.date_input.text().strip(),
                    self.time_input.text().strip(),
                    self.video_path,
                    self.task_color])

    def on_color_button_clicked(self):
        """Opens a color dialog to choose a color for the task."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.task_color = color.name()
            self.color_button.setStyleSheet(f"background-color: {self.task_color}")

    def on_task_added(self, task):
        """Handles actions when a task is added."""
        QMessageBox.information(self, "Success", "Task saved successfully!")

    def on_task_deleted(self, task_id):
        """Handles actions when a task is deleted."""
        # You can implement any necessary actions here when a task is deleted