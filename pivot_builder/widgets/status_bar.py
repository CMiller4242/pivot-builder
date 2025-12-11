"""Status bar widget for the application."""

import tkinter as tk
from tkinter import ttk


class StatusBar(ttk.Frame):
    """Status bar widget for displaying application status."""

    def __init__(self, parent):
        super().__init__(parent)
        self.label = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(fill=tk.X, expand=True)

    def set_status(self, message):
        """Set status message."""
        self.label.config(text=message)
