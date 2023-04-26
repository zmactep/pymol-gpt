from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel
)

from .config import ConfigDialog
from .gpt import send_request, run_response

class GPTDialog(QDialog):
    """Main plugin dialog"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GPT Plugin")

        self.conf_dialog = ConfigDialog()

        self.text_area = QTextEdit()

        self.status_label = QLabel(" ")

        self.run_button = QPushButton("Run")
        self.conf_button = QPushButton("...")

        vlay = QVBoxLayout()
        hlay = QHBoxLayout()

        vlay.addWidget(self.text_area)
        hlay.addWidget(self.run_button)
        hlay.addWidget(self.conf_button)
        vlay.addWidget(self.status_label)
        vlay.addLayout(hlay)
        self.setLayout(vlay)

        self.conf_button.clicked.connect(self.conf_pressed)
        self.run_button.clicked.connect(self.run_pressed)

    def config(self):
        """Returns config"""
        return self.conf_dialog.config

    def run_pressed(self):
        """Runs model with request"""
        self.status_label.setText('Sending request to OpenAI GPT')
        response = send_request(self.text_area.toPlainText(), self.config())
        if not response:
            self.status_label.setText("Request failed")
            return
        if self.config()['autorun']:
            run_response(response)
        else:
            print(response)
        self.status_label.setText('Done!')

    def conf_pressed(self):
        """Show config dialog"""
        self.conf_dialog.show()
