from PyQt5 import QtCore, QtGui, QtWidgets
from a2m8.mass_rename import mass_rename
from a2m8.working_files_creator import working_files
from a2m8.tif2jpg import do_tif2jpg
from a2m8.masters_creator import create_master
import sys

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
        self.button3 = QtWidgets.QPushButton("Masters Creator")
        self.button4 = QtWidgets.QPushButton("TIF 2 JPG")
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
        self.button3.clicked.connect(self.open_masters_window)

        self.button6.clicked.connect(self.open_rename_window)

        self.button5.clicked.connect(self.open_working_files_window)

        self.button4.clicked.connect(self.open_tif2jpg_window)

    def open_masters_window(self):
        self.masters_window = MastersWindow()
        self.masters_window.show()
        self.masters_window.resize(800, 600)
    def open_rename_window(self):
        self.rename_window = RenameWindow()
        self.rename_window.show()
        self.rename_window.resize(800, 600)
    def open_working_files_window(self):
        self.rename_window = WorkingFilesTool()
        self.rename_window.show()
        self.rename_window.resize(800, 600)
    def open_tif2jpg_window(self):
        self.rename_window = TIF2JPGWindow()
        self.rename_window.show()
        self.rename_window.resize(800, 600)

class MastersWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Masters Creator")

        # Create a label to display the selected directory path
        self.selected_path_label = QtWidgets.QLabel("No directory selected")
        self.selected_path_label.setAlignment(QtCore.Qt.AlignCenter)
        # Create labels and line edits
        self.label = QtWidgets.QLabel("Copy all files from originals to masters and then select the masters folder and press Create")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.directorybutton = QtWidgets.QPushButton("...")
        self.directorybutton.clicked.connect(self.select_directory)
        self.label_id = QtWidgets.QLabel("Enter Collection ID:")
        self.collectionid = QtWidgets.QLineEdit()
        self.terminal = QtWidgets.QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.Createbutton = QtWidgets.QPushButton("Create")
        self.Createbutton.clicked.connect(self.do_masters)

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.addWidget(self.label)
        layout.addWidget(self.directorybutton)
        layout.addWidget(self.selected_path_label)
        layout.addWidget(self.label_id)
        layout.addWidget(self.collectionid)
        layout.addWidget(self.terminal)
        layout.addWidget(self.Createbutton)

        # Set the central widget of the main window
        self.setCentralWidget(widget)

    def select_directory(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        if directory:
            self.directory = directory
            self.selected_path_label.setText(f"Selected directory: {directory}")

    def do_masters(self):
        masterdir = self.directory
        collection_id = self.collectionid.text()
        self.label.setText("Processing...")
        QtWidgets.QApplication.processEvents()
        create_master(masterdir, collection_id)
        self.label.setText("Done.")

class WorkingFilesTool(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Working Files Creator")

        # Create a label to display the selected directory path
        self.selected_path_label = QtWidgets.QLabel("No directory selected")
        self.selected_path_label.setAlignment(QtCore.Qt.AlignCenter)
        # Create labels and line edits
        self.label = QtWidgets.QLabel("Select path to Access and press Create")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.directorybutton = QtWidgets.QPushButton("...")
        self.directorybutton.clicked.connect(self.select_directory)
        self.terminal = QtWidgets.QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.Createbutton = QtWidgets.QPushButton("Create")
        self.Createbutton.clicked.connect(self.do_working_files)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.directorybutton)
        layout.addWidget(self.terminal)
        layout.addWidget(self.Createbutton)
        self.setLayout(layout)

    def select_directory(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        if directory:
            self.directory = directory
            self.selected_path_label.setText(f"Selected directory: {directory}")

    def do_working_files(self):
        self.masterdir = self.directory
        self.label.setText("Processing...")
        QtWidgets.QApplication.processEvents()
        working_files(self.masterdir, self.terminal)
        self.label.setText("Done.")


class RenameWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mass Rename Tool")

        # Create a label to display the selected directory path
        self.selected_path_label = QtWidgets.QLabel("No directory selected")
        self.selected_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.terminal = QtWidgets.QPlainTextEdit()
        self.terminal.setReadOnly(True)
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
        layout.addWidget(self.terminal)
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
        mass_rename(self.directory, old_str, new_str, self.terminal)

class TIF2JPGWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TIF to JPG Converter")

        # Create a label to display the selected directory path
        self.selected_path_label = QtWidgets.QLabel("No directory selected")
        self.selected_path_label.setAlignment(QtCore.Qt.AlignCenter)

        self.terminal = QtWidgets.QPlainTextEdit()
        self.terminal.setReadOnly(True)

        # Create labels and line edits
        self.label = QtWidgets.QLabel("Select a directory and press Convert")
        self.label.setAlignment(QtCore.Qt.AlignCenter)


        # Create buttons
        self.directorybutton = QtWidgets.QPushButton("...")
        self.convertbutton = QtWidgets.QPushButton("Convert")

        # Add the labels, line edits, and buttons to layouts
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.directorybutton)
        button_layout.addWidget(self.convertbutton)

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.selected_path_label)
        layout.addWidget(self.label)
        layout.addWidget(self.terminal)
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect button signals to slots
        self.directorybutton.clicked.connect(self.select_directory)
        self.convertbutton.clicked.connect(lambda: self.tif2jpg())

    def tif2jpg(self):
        path = self.directory  # use the selected directory, not the label widget
        sys.stdout = self.terminal
        do_tif2jpg(path)
        sys.stdout = sys.__stdout__
    def select_directory(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        if directory:
            self.directory = directory
            self.selected_path_label.setText(f"Selected directory: {directory}")
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    window.resize(1280, 720)
    app.exec_()
