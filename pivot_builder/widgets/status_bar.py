"""Status bar widget for the application."""

import tkinter as tk
from tkinter import ttk


class StatusBar(ttk.Frame):
    """Status bar widget for displaying application status."""

    def __init__(self, parent):
        super().__init__(parent)
        self.label = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(fill=tk.X, expand=True)

    def set(self, text: str):
        """
        Set status message.

        Args:
            text: Status text to display
        """
        self.label.config(text=text)

    def set_status(self, message):
        """Set status message (backward compatibility)."""
        self.set(message)
