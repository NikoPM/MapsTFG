from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QMessageBox



class InputDialog(QDialog):
    def __init__(self, title, label_text):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.label = QLabel(label_text)
        self.lineEdit = QLineEdit(self)
        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(self.accept)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.okButton)
        self.setLayout(self.layout)

    def get_input(self):
        return self.lineEdit.text()
    
    def show_warning(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Hay columnas vacías en la tabla.")
        msgBox.setWindowTitle("Advertencia")
        msgBox.exec_()