"""File management panel."""

import tkinter as tk
from tkinter import ttk

from pivot_builder.widgets.file_item_widget import FileItemWidget


class FilePanel(ttk.Frame):
    """Panel for managing files."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.file_widgets = {}  # Dict[file_id, FileItemWidget]

        # Create UI components
        self._create_ui()

    def _create_ui(self):
        """Create the UI components."""
        # Title label
        title_label = ttk.Label(self, text="Files", font=("TkDefaultFont", 10, "bold"))
        title_label.pack(pady=(5, 10), padx=5, anchor=tk.W)

        # Add Files button
        self.add_button = ttk.Button(
            self,
            text="Add Files...",
            command=self._on_add_files_clicked
        )
        self.add_button.pack(pady=5, padx=5, fill=tk.X)

        # Scrollable frame for file list
        self._create_scrollable_file_list()

        # Info label at bottom
        self.info_label = ttk.Label(self, text="No files loaded", foreground="gray")
        self.info_label.pack(side=tk.BOTTOM, pady=5, padx=5)

    def _create_scrollable_file_list(self):
        """Create scrollable container for file items."""
        # Create canvas with scrollbar
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _on_add_files_clicked(self):
        """Handle Add Files button click."""
        if self.controller:
            self.controller.on_add_files()

    def refresh(self, file_descriptors):
        """
        Refresh the file list display.

        Args:
            file_descriptors: List of FileDescriptor objects
        """
        # Clear existing widgets
        for widget in self.file_widgets.values():
            widget.destroy()
        self.file_widgets.clear()

        # Create widgets for each file
        for descriptor in file_descriptors:
            widget = FileItemWidget(
                self.scrollable_frame,
                descriptor,
                self.controller
            )
            widget.pack(fill=tk.X, padx=2, pady=2)
            self.file_widgets[descriptor.id] = widget

        # Update info label
        if len(file_descriptors) == 0:
            self.info_label.config(text="No files loaded")
        elif len(file_descriptors) == 1:
            self.info_label.config(text="1 file loaded")
        else:
            self.info_label.config(text=f"{len(file_descriptors)} files loaded")
