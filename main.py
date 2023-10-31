from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QStyleFactory
from PySide6.QtGui import QPalette, QColor, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout
import sys

from utils.data_handler import DataHandler
from utils.api_handler import APIHandler
from utils.scheduler import Scheduler

from widgets.task_preparation_widget import TaskPreparationWidget
from widgets.scheduled_tasks_list_widget import ScheduledTasksListWidget
from widgets.calendar_widget import CustomCalendar
from PySide6.QtWidgets import QLabel


class MainWindow(QWidget):
    def __init__(self, data_handler, api_handler):
        super().__init__()

        self.data_handler = data_handler
        self.api_handler = api_handler

        # Initialize UI components
        self.init_ui()

        # Load initial data
        self.load_initial_data()

    def init_ui(self):
        main_layout = QVBoxLayout(self)  # Main layout to stack header and other widgets

        # Adding a header image
        header_label = QLabel(self)
        pixmap = QPixmap("assets/header.png")  # Replace with your image path
        header_label.setPixmap(pixmap.scaledToWidth(800))  # Adjust width as needed
        main_layout.addWidget(header_label)

        # Horizontal layout for other widgets
        layout = QHBoxLayout()
        # Set the main window size
        self.setMinimumSize(1200, 900)  # You can adjust the values based on your needs

        # Instantiate Components
        self.task_preparation_widget = TaskPreparationWidget(self.data_handler)
        self.scheduled_tasks_widget = ScheduledTasksListWidget(self.data_handler)
        self.calendar_widget = CustomCalendar(self.data_handler)
        self.scheduler = Scheduler(self.data_handler, self.api_handler)

        # Connecting DataHandler signals to widgets
        self.data_handler.task_added.connect(self.scheduled_tasks_widget.refresh_tasks)
        self.data_handler.task_added.connect(self.calendar_widget.refresh_calendar)
        self.data_handler.task_deleted.connect(self.scheduled_tasks_widget.refresh_tasks)
        self.data_handler.task_deleted.connect(self.calendar_widget.refresh_calendar)

        # Add widgets to layout in the desired order
        layout.addWidget(self.calendar_widget)
        layout.addWidget(self.task_preparation_widget)
        layout.addWidget(self.scheduled_tasks_widget)

        main_layout.addLayout(layout)  # Add horizontal layout to the main vertical layout
        self.setLayout(main_layout)

        self.task_preparation_widget.connect_task_list(self.scheduled_tasks_widget)
        self.scheduled_tasks_widget.connect_calendar(self.calendar_widget)

    def handle_date_clicked(self, date):
        print(f"Date clicked: {date.toString('yyyy-MM-dd')}")

    def load_initial_data(self):
        # Load saved tasks and other initial data into the widgets
        tasks = self.data_handler.get_all_tasks()
        self.scheduled_tasks_widget.display_tasks(tasks)


def set_dark_mode(app):
    app.setStyle(QStyleFactory.create('Fusion'))

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")


# Instantiate and run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    data_handler = DataHandler()
    api_handler = APIHandler()
    set_dark_mode(app)

    window = MainWindow(data_handler, api_handler)
    window.show()

    sys.exit(app.exec())
