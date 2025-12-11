"""Widget for displaying available pivot fields."""

import tkinter as tk
from tkinter import ttk


class PivotFieldList(ttk.Frame):
    """Widget for displaying available fields for pivot table."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Placeholder label
        self.label = ttk.Label(self, text="Pivot Field List")
        self.label.pack()
