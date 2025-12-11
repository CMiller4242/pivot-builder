"""Widget for displaying column mappings."""

import tkinter as tk
from tkinter import ttk

try:
    from tksheet import Sheet
except ImportError:
    Sheet = None


class MappingTableWidget(ttk.Frame):
    """Widget for displaying and editing column mappings."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Placeholder label
        self.label = ttk.Label(self, text="Mapping Table (tksheet placeholder)")
        self.label.pack()
