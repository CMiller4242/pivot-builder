"""File management panel."""

import tkinter as tk
from tkinter import ttk


class FilePanel(ttk.Frame):
    """Panel for managing files."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Placeholder UI
        self.label = ttk.Label(self, text="File Panel")
        self.label.pack(pady=10)

        self.add_button = ttk.Button(self, text="Add Files")
        self.add_button.pack(pady=5)

        self.file_listbox = tk.Listbox(self)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
