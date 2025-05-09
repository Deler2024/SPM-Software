from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog
import csv

class DataLoggingTab(QWidget):
    """
    A tab for real-time data logging and saving.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the layout
        self.layout = QVBoxLayout(self)

        # Add a table to display the data
        self.data_table = QTableWidget(self)
        self.data_table.setColumnCount(3)  # X, Y, Z columns
        self.data_table.setHorizontalHeaderLabels(["X Position", "Y Position", "Z Position"])
        self.layout.addWidget(self.data_table)

        # Add a "Save Data" button
        self.save_button = QPushButton("Save Data", self)
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)

        # Initialize an empty data list
        self.data = []

    def add_data(self, x, y, z):
        """
        Add a new row of data to the table.
        :param x: X position
        :param y: Y position
        :param z: Z position
        """
        self.data.append((x, y, z))
        row = self.data_table.rowCount()
        self.data_table.insertRow(row)
        self.data_table.setItem(row, 0, QTableWidgetItem(f"{x:.2f}"))
        self.data_table.setItem(row, 1, QTableWidgetItem(f"{y:.2f}"))
        self.data_table.setItem(row, 2, QTableWidgetItem(f"{z:.2f}"))

    def save_data(self):
        """
        Save the logged data to a CSV file.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Data", "", "CSV Files (*.csv);;All Files (*)", options=options
        )
        if file_path:
            try:
                with open(file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["X Position", "Y Position", "Z Position"])
                    writer.writerows(self.data)
                print(f"Data saved to {file_path}")
            except Exception as e:
                print(f"Error saving data: {e}")