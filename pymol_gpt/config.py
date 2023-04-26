"""Configuration load, save and modification"""
import os
import json
from pathlib import Path

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QCheckBox
)

MODELS = ['gpt-3.5-turbo', 'gpt-4']

# Configuration
CONFIG_DIR = os.path.join(os.path.join(Path.home(), ".config"), "pymol-gpt")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

def default_config():
    return {'api_key': '', 'model': 0, 'autorun': False}

def load_config():
    """Loads configuration of the plugin"""
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf8') as file:
            config = json.loads(file.read())
    else:
        config = default_config()
        save_config(config)
    return config

def save_config(config):
    """Saves configuration of the plugin"""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    with open(CONFIG_PATH, 'wt', encoding='utf8') as file:
        file.write(json.dumps(config))

class ConfigDialog(QDialog):
    """Configuration dialog"""
    def __init__(self):
        super().__init__()

        self.config = default_config()

        self.key_edit = QLineEdit()
        self.key_edit.setMinimumWidth(400)

        self.model = QComboBox()
        self.model.addItems(MODELS)

        self.autorun_check = QCheckBox()

        self.save_button = QPushButton("Save")
        self.reset_button = QPushButton("Reset")

        hlay1 = QHBoxLayout()
        hlay2 = QHBoxLayout()
        hlaya = QHBoxLayout()
        hlay3 = QHBoxLayout()

        hlay1.addWidget(QLabel("API Key:"))
        hlay1.addWidget(self.key_edit)

        hlay2.addWidget(QLabel("Model:"))
        hlay2.addWidget(self.model)

        hlaya.addWidget(QLabel("Autorun:"))
        hlaya.addWidget(self.autorun_check)

        hlay2.addLayout(hlaya)

        hlay3.addWidget(self.save_button)
        hlay3.addWidget(self.reset_button)

        vlay = QVBoxLayout()
        vlay.addLayout(hlay1)
        vlay.addLayout(hlay2)
        vlay.addLayout(hlay3)

        self.setLayout(vlay)
        self.reset_pressed()

        self.save_button.clicked.connect(self.save_pressed)
        self.reset_button.clicked.connect(self.reset_pressed)

    def save_pressed(self):
        """Saves inserted config"""
        self.config['api_key'] = self.key_edit.text()
        self.config['model'] = self.model.currentIndex()
        self.config['autorun'] = self.autorun_check.isChecked()

        save_config(self.config)
        self.hide()

    def reset_pressed(self):
        """Reloads saved config"""
        self.config = load_config()
        self.key_edit.setText(self.config['api_key'])
        self.model.setCurrentIndex(self.config['model'])
        self.autorun_check.setChecked(self.config['autorun'])
