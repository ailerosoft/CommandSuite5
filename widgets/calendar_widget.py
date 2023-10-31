from PySide6.QtWidgets import QCalendarWidget
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QPainter, QColor, QTextCharFormat


class CustomCalendar(QCalendarWidget):
    date_clicked = Signal(QDate)

    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.initUI()

        # Connect the built-in clicked signal to a custom slot
        self.clicked.connect(self.on_date_clicked)

    def initUI(self):
        self.setStyleSheet("""
                    QCalendarWidget QWidget {
                        alternate-background-color: #1d1d1d;
                        background-color: #2d2d2d;
                    }
                    QCalendarWidget QTableView {
                        border: 1px solid #555;
                        selection-background-color: #888;
                    }
                    QCalendarWidget QHeaderView {
                        background-color: #555;
                        text-color: #999
                    }
                """)

        # Setting the text color of the weekend dates to black
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(Qt.white))  # You can choose another color if you prefer

        self.setWeekdayTextFormat(Qt.Saturday, fmt)
        self.setWeekdayTextFormat(Qt.Sunday, fmt)

        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setGridVisible(True)

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)  # Call the base class paintCell first

        # Get tasks for the date directly from the DataHandler
        tasks = self.data_handler.scheduled_tasks.get(date.toString("yyyy-MM-dd"), [])

        print(f"Date: {date.toString('yyyy-MM-dd')}, Tasks: {tasks}")  # Debugging line

        # Draw a colored line for each task
        line_height = 5  # Height of each line
        gap = 2  # Gap between each line

        for i, task in enumerate(tasks):
            color = QColor(task['color'])
            painter.fillRect(rect.x(),
                             rect.y() + i * (line_height + gap),  # Adjusted y-position
                             rect.width(), line_height, color)

    def on_date_clicked(self, date):
        """Slot to handle the clicked signal."""
        self.date_clicked.emit(date)
        print(f"emitted date_clicked: {date}")  # Printing for debugging

    def refresh_calendar(self):
        print("refresh calendar called correctly...")
        self.updateCells()  # This will redraw the calendar cells, which will fetch updated tasks from the DataHandler

