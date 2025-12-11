"""Widget for displaying a single file item."""

import tkinter as tk
from tkinter import ttk

from pivot_builder.widgets.sheet_selector_widget import SheetSelectorWidget


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
            # CSV: Show column count
            info_text = f"{len(self.file_descriptor.original_columns)} columns"
            metadata_label = ttk.Label(
                metadata_frame,
                text=info_text,
                foreground="blue",
                font=("TkDefaultFont", 8)
            )
            metadata_label.pack(side=tk.LEFT)

            # Add preview button for CSV (data is already loaded)
            if self.file_descriptor.has_dataframe:
                self._add_preview_button(metadata_frame)

        elif self.file_descriptor.file_type == 'xlsx':
            # XLSX: Show sheet selector if sheets are available
            if self.file_descriptor.available_sheets and self.file_descriptor.needs_sheet_selection:
                # Add sheet selector
                sheet_selector = SheetSelectorWidget(
                    metadata_frame,
                    self.file_descriptor.id,
                    self.file_descriptor.available_sheets,
                    self._on_sheet_selected
                )
                sheet_selector.pack(side=tk.LEFT, pady=(2, 0))
            elif self.file_descriptor.has_dataframe:
                # Sheet already selected - show selected sheet and preview button
                selected_sheet_label = ttk.Label(
                    metadata_frame,
                    text=f"Sheet: {self.file_descriptor.selected_sheet}",
                    foreground="blue",
                    font=("TkDefaultFont", 8)
                )
                selected_sheet_label.pack(side=tk.LEFT)

                self._add_preview_button(metadata_frame)

    def _add_preview_button(self, parent):
        """Add preview button to metadata frame."""
        preview_btn = ttk.Button(
            parent,
            text="Preview",
            width=10,
            command=self._on_preview_clicked
        )
        preview_btn.pack(side=tk.RIGHT, padx=(5, 0))

    def _on_sheet_selected(self, file_id, sheet_name):
        """Handle sheet selection."""
        if self.controller:
            self.controller.on_sheet_selected(file_id, sheet_name)

    def _on_preview_clicked(self):
        """Handle preview button click."""
        # This will be routed through app_controller
        if self.controller and hasattr(self.controller, 'app_controller'):
            self.controller.app_controller.on_request_file_preview(self.file_descriptor.id)

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
