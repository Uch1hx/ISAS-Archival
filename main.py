from PyQt5 import QtCore, QtGui, QtWidgets
from a2m8.mass_rename import mass_rename
from a2m8.working_files_creator import working_files
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("A2M8")

        # Create a label
        self.label = QtWidgets.QLabel("ISAS")
        self.label.setAlignment(QtCore.Qt.AlignTop)
        self.label.setStyleSheet("font-size: 24pt;")

        # Create buttons
        self.button1 = QtWidgets.QPushButton("Button 1")
        self.button2 = QtWidgets.QPushButton("Button 2")
        self.button3 = QtWidgets.QPushButton("Button 3")
        self.button4 = QtWidgets.QPushButton("Button 4")
        self.button5 = QtWidgets.QPushButton("Working Files Creator")
        self.button6 = QtWidgets.QPushButton("Mass Rename")

        # Create a grid layout for the buttons
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.button1, 0, 0)
        grid_layout.addWidget(self.button2, 0, 1)
        grid_layout.addWidget(self.button3, 0, 2)
        grid_layout.addWidget(self.button4, 1, 0)
        grid_layout.addWidget(self.button5, 1, 1)
        grid_layout.addWidget(self.button6, 1, 2)

        # Add the label and button grid to the main window
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addLayout(grid_layout)
        layout.addStretch()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect button signals to slots
        self.button6.clicked.connect(self.open_new_window)

        self.button5.clicked.connect(self.open_working_files_window)

    def open_new_window(self):
        self.new_window = NewWindow()
        self.new_window.show()
        self.new_window.resize(800, 600)
    def open_working_files_window(self):
        self.new_window = WorkingFilesTool()
        self.new_window.show()
        self.new_window.resize(800, 600)

class WorkingFilesTool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Working Files Creator")

        # Create a label to display the selected directory path
        self.selected_path_label = QtWidgets.QLabel("No directory selected")
        self.selected_path_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create labels and line edits
        self.label = QtWidgets.QLabel("Select a directory and press Create")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.directorybutton = QtWidgets.QPushButton("...")
        self.directorybutton.clicked.connect(self.select_directory)
        self.Createbutton = QtWidgets.QPushButton("Create")
        self.Createbutton.clicked.connect(self.working_files)

    def select_directory(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        if directory:
            self.directory = directory
            self.selected_path_label.setText(f"Selected directory: {directory}")

    def working_files(self):
        self.masterdir = self.directory
        working_files(self.masterdir)

class NewWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mass Rename Tool")

        # Create a label to display the selected directory path
        self.selected_path_label = QtWidgets.QLabel("No directory selected")
        self.selected_path_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create labels and line edits
        self.label = QtWidgets.QLabel("Select a directory and press Rename")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.label_old = QtWidgets.QLabel("Enter Old Substring:")
        self.old_substring = QtWidgets.QLineEdit()

        self.label_new = QtWidgets.QLabel("Enter New Substring:")
        self.new_substring = QtWidgets.QLineEdit()

        # Create buttons
        self.directorybutton = QtWidgets.QPushButton("...")
        self.renamebutton = QtWidgets.QPushButton("Rename")

        # Add the labels, line edits, and buttons to layouts
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.directorybutton)
        button_layout.addWidget(self.renamebutton)

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.selected_path_label)
        layout.addWidget(self.label)
        layout.addWidget(self.label_old)
        layout.addWidget(self.old_substring)
        layout.addWidget(self.label_new)
        layout.addWidget(self.new_substring)
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect button signals to slots
        self.directorybutton.clicked.connect(self.select_directory)
        self.renamebutton.clicked.connect(lambda: self.mass_rename())

    def select_directory(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        if directory:
            self.directory = directory
            self.selected_path_label.setText(f"Selected directory: {directory}")

    def mass_rename(self):
        old_str = self.old_substring.text()
        new_str = self.new_substring.text()
        mass_rename(self.directory, old_str, new_str)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    window.resize(1280, 720)
    app.exec_()
