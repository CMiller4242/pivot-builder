"""Data preview view."""

import tkinter as tk
from tkinter import ttk


class PreviewView(ttk.Frame):
    """View for previewing combined dataset."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Placeholder UI
        self.label = ttk.Label(self, text="Preview View")
        self.label.pack(pady=10)

        self.refresh_button = ttk.Button(self, text="Refresh Preview")
        self.refresh_button.pack(pady=5)

        # Placeholder frame for preview table
        self.preview_frame = ttk.Frame(self)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
