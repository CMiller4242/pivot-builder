"""Column mapping view."""

import tkinter as tk
from tkinter import ttk


class ColumnMappingView(ttk.Frame):
    """View for mapping columns across files."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Placeholder UI
        self.label = ttk.Label(self, text="Column Mapping View")
        self.label.pack(pady=10)

        self.auto_map_button = ttk.Button(self, text="Auto Map")
        self.auto_map_button.pack(pady=5)

        # Placeholder frame for mapping table
        self.mapping_frame = ttk.Frame(self)
        self.mapping_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
