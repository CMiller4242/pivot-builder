"""Validation panel for data quality checks."""

import tkinter as tk
from tkinter import ttk


class ValidationPanel(ttk.Frame):
    """Panel for displaying validation results."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Placeholder UI
        self.label = ttk.Label(self, text="Validation Panel")
        self.label.pack(pady=10)

        self.validate_button = ttk.Button(self, text="Run Validation")
        self.validate_button.pack(pady=5)

        # Placeholder text widget for validation results
        self.results_text = tk.Text(self, height=20, width=60)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
