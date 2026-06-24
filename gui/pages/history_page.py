from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QHeaderView, QLabel
from services.history_service import HistoryService

class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.history_service = HistoryService()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Download History")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Controls
        controls = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.setStyleSheet("padding: 8px 15px;")
        self.refresh_btn.clicked.connect(self.load_data)
        controls.addWidget(self.refresh_btn)
        controls.addStretch()
        layout.addLayout(controls)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Date", "Title", "URL", "Platform", "Quality", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        
        self.setLayout(layout)

    def load_data(self):    
        history = self.history_service.load_history()
        history.reverse() # Show newest first
        
        self.table.setRowCount(len(history))
        for row, record in enumerate(history):
            self.table.setItem(row, 0, QTableWidgetItem(record.get('download_date', '')))
            self.table.setItem(row, 1, QTableWidgetItem(record.get('title', '')))
            self.table.setItem(row, 2, QTableWidgetItem(record.get('url', '')))
            self.table.setItem(row, 3, QTableWidgetItem(record.get('platform', '')))
            self.table.setItem(row, 4, QTableWidgetItem(record.get('quality', '')))
            self.table.setItem(row, 5, QTableWidgetItem(record.get('status', '')))
