"""Widget for displaying a single file item."""

import tkinter as tk
from tkinter import ttk


class FileItemWidget(ttk.Frame):
    """Widget representing a single file in the file list."""

    def __init__(self, parent, file_path, controller):
        super().__init__(parent)
        self.file_path = file_path
        self.controller = controller

        # Placeholder label
        self.label = ttk.Label(self, text=f"File: {file_path}")
        self.label.pack()
