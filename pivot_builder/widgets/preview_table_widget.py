"""Widget for displaying data preview."""

import tkinter as tk
from tkinter import ttk

try:
    from tksheet import Sheet
except ImportError:
    Sheet = None


class PreviewTableWidget(ttk.Frame):
    """Widget for displaying data preview in table format."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Placeholder label
        self.label = ttk.Label(self, text="Preview Table (tksheet placeholder)")
        self.label.pack()
