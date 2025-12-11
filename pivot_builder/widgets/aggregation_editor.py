"""Widget for editing aggregation functions."""

import tkinter as tk
from tkinter import ttk


class AggregationEditor(ttk.Frame):
    """Widget for selecting and editing aggregation functions."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Placeholder label
        self.label = ttk.Label(self, text="Aggregation Editor")
        self.label.pack()
