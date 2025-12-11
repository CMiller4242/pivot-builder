"""Pivot table builder view."""

import tkinter as tk
from tkinter import ttk


class PivotBuilderView(ttk.Frame):
    """View for building pivot tables."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Placeholder UI
        self.label = ttk.Label(self, text="Pivot Builder View")
        self.label.pack(pady=10)

        # Placeholder frames for field lists and buckets
        self.fields_frame = ttk.LabelFrame(self, text="Available Fields")
        self.fields_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.buckets_frame = ttk.Frame(self)
        self.buckets_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Placeholder buckets
        self.rows_bucket = ttk.LabelFrame(self.buckets_frame, text="Rows")
        self.rows_bucket.pack(fill=tk.BOTH, expand=True, pady=2)

        self.columns_bucket = ttk.LabelFrame(self.buckets_frame, text="Columns")
        self.columns_bucket.pack(fill=tk.BOTH, expand=True, pady=2)

        self.values_bucket = ttk.LabelFrame(self.buckets_frame, text="Values")
        self.values_bucket.pack(fill=tk.BOTH, expand=True, pady=2)

        self.build_button = ttk.Button(self, text="Build Pivot")
        self.build_button.pack(pady=5)
