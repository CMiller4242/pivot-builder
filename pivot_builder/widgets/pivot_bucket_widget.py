"""Widget for pivot field buckets (rows, columns, values)."""

import tkinter as tk
from tkinter import ttk


class PivotBucketWidget(ttk.Frame):
    """Widget representing a bucket for pivot fields (rows/columns/values)."""

    def __init__(self, parent, bucket_type, controller):
        super().__init__(parent)
        self.bucket_type = bucket_type
        self.controller = controller

        # Placeholder label
        self.label = ttk.Label(self, text=f"Pivot Bucket: {bucket_type}")
        self.label.pack()
