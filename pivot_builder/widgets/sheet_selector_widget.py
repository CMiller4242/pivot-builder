"""Widget for selecting Excel sheets."""

import tkinter as tk
from tkinter import ttk


class SheetSelectorWidget(ttk.Frame):
    """Widget for selecting sheets from Excel files."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Placeholder label
        self.label = ttk.Label(self, text="Sheet Selector")
        self.label.pack()
