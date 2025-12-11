"""Widget for displaying column lists."""

import tkinter as tk
from tkinter import ttk


class ColumnListWidget(ttk.Frame):
    """Widget for displaying a list of columns."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Placeholder label
        self.label = ttk.Label(self, text="Column List")
        self.label.pack()
