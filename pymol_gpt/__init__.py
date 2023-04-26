"""This plugin asks GPT to perform standard pymol actions"""
from pymol.plugins import addmenuitemqt

from .config import load_config
from .dialog import GPTDialog

# global reference to avoid garbage collection of our dialog
dialog = None

def __init_plugin__(app=None):
    load_config()
    addmenuitemqt('GPT Plugin', run_plugin_gui)

def run_plugin_gui():
    """Shows dialog of the plugin"""
    # pymol.Qt provides the PyQt5 interface, but may support PyQt4 and/or PySide as well
    global dialog

    if dialog is None:
        # create a new (empty) Window
        dialog = GPTDialog()
    dialog.show()
