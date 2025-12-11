"""Widget for displaying a single file item."""

import tkinter as tk
from tkinter import ttk


class FileItemWidget(ttk.Frame):
    """Widget representing a single file in the file list."""

    # Status color mapping
    STATUS_COLORS = {
        'pending': '#808080',  # Gray
        'loaded': '#28a745',   # Green
        'error': '#dc3545'     # Red
    }

    def __init__(self, parent, file_descriptor, controller):
        super().__init__(parent, relief=tk.RIDGE, borderwidth=1)
        self.file_descriptor = file_descriptor
        self.controller = controller

        # Create UI
        self._create_ui()

    def _create_ui(self):
        """Create the widget UI."""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Top row: filename and remove button
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X)

        # Filename label
        filename_label = ttk.Label(
            top_frame,
            text=self.file_descriptor.filename,
            font=("TkDefaultFont", 9, "bold")
        )
        filename_label.pack(side=tk.LEFT)

        # Remove button
        remove_btn = ttk.Button(
            top_frame,
            text="×",
            width=3,
            command=self._on_remove_clicked
        )
        remove_btn.pack(side=tk.RIGHT)

        # Second row: file type and status
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(2, 0))

        # File type label
        type_label = ttk.Label(
            info_frame,
            text=f"Type: {self.file_descriptor.file_type.upper()}",
            foreground="gray",
            font=("TkDefaultFont", 8)
        )
        type_label.pack(side=tk.LEFT)

        # Status indicator
        self.status_label = tk.Label(
            info_frame,
            text=self._get_status_text(),
            font=("TkDefaultFont", 8, "bold"),
            foreground=self._get_status_color()
        )
        self.status_label.pack(side=tk.RIGHT)

        # Third row: metadata info (for loaded files)
        if self.file_descriptor.status == 'loaded':
            self._add_metadata_info(main_frame)
        elif self.file_descriptor.status == 'error' and self.file_descriptor.error_message:
            self._add_error_info(main_frame)

    def _add_metadata_info(self, parent):
        """Add metadata information for loaded files."""
        metadata_frame = ttk.Frame(parent)
        metadata_frame.pack(fill=tk.X, pady=(2, 0))

        if self.file_descriptor.file_type == 'csv':
            info_text = f"{len(self.file_descriptor.original_columns)} columns"
        elif self.file_descriptor.file_type == 'xlsx':
            sheets = len(self.file_descriptor.available_sheets)
            info_text = f"{sheets} sheet{'s' if sheets != 1 else ''}"
        else:
            info_text = ""

        if info_text:
            metadata_label = ttk.Label(
                metadata_frame,
                text=info_text,
                foreground="blue",
                font=("TkDefaultFont", 8)
            )
            metadata_label.pack(side=tk.LEFT)

    def _add_error_info(self, parent):
        """Add error information."""
        error_frame = ttk.Frame(parent)
        error_frame.pack(fill=tk.X, pady=(2, 0))

        error_label = ttk.Label(
            error_frame,
            text=f"Error: {self.file_descriptor.error_message}",
            foreground="red",
            font=("TkDefaultFont", 8),
            wraplength=200
        )
        error_label.pack(side=tk.LEFT)

    def _get_status_text(self):
        """Get the status text to display."""
        return self.file_descriptor.status.upper()

    def _get_status_color(self):
        """Get the color for the current status."""
        return self.STATUS_COLORS.get(self.file_descriptor.status, '#000000')

    def _on_remove_clicked(self):
        """Handle remove button click."""
        if self.controller:
            self.controller.on_remove_file(self.file_descriptor.id)
