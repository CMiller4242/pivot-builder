"""Data preview view."""

import tkinter as tk
from tkinter import ttk

from pivot_builder.widgets.preview_table_widget import PreviewTableWidget


class PreviewView(ttk.Frame):
    """View for previewing file data."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.file_list = []  # List of file descriptors
        self.current_file_id = None

        self._create_ui()

    def _create_ui(self):
        """Create the UI components."""
        # Top control panel
        control_panel = ttk.Frame(self)
        control_panel.pack(fill=tk.X, padx=10, pady=10)

        # File selector
        file_selector_frame = ttk.Frame(control_panel)
        file_selector_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(file_selector_frame, text="Select File:").pack(side=tk.LEFT, padx=(0, 5))

        self.file_var = tk.StringVar()
        self.file_combo = ttk.Combobox(
            file_selector_frame,
            textvariable=self.file_var,
            state='readonly',
            width=40
        )
        self.file_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.file_combo.bind('<<ComboboxSelected>>', self._on_file_selected)

        # Info label
        self.info_label = ttk.Label(control_panel, text="", foreground="gray")
        self.info_label.pack(side=tk.RIGHT, padx=10)

        # Preview table
        self.preview_table = PreviewTableWidget(self, self.controller)
        self.preview_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Initial empty state
        self.preview_table.set_empty_message("No files loaded. Add files to preview data.")

    def _on_file_selected(self, event=None):
        """Handle file selection from dropdown."""
        selected = self.file_var.get()
        if not selected:
            return

        # Find the file descriptor by display name
        for file_desc in self.file_list:
            display_name = self._get_file_display_name(file_desc)
            if display_name == selected:
                self.current_file_id = file_desc.id
                if self.controller:
                    self.controller.show_preview_for(file_desc.id)
                break

    def refresh_file_list(self, file_descriptors):
        """
        Refresh the list of available files.

        Args:
            file_descriptors: List of FileDescriptor objects
        """
        self.file_list = file_descriptors

        # Update combobox values
        display_names = [self._get_file_display_name(f) for f in file_descriptors]
        self.file_combo['values'] = display_names

        # If there was a selection, try to maintain it
        if self.current_file_id:
            for i, file_desc in enumerate(file_descriptors):
                if file_desc.id == self.current_file_id:
                    self.file_combo.current(i)
                    break
        elif display_names:
            # Select first file by default
            self.file_combo.current(0)
            self._on_file_selected()

    def show_preview(self, file_descriptor):
        """
        Show preview for a specific file.

        Args:
            file_descriptor: FileDescriptor to preview
        """
        if file_descriptor is None:
            self.preview_table.set_empty_message("File not found")
            self.info_label.config(text="")
            return

        # Check if file has data loaded
        if not file_descriptor.has_dataframe:
            if file_descriptor.needs_sheet_selection:
                self.preview_table.set_empty_message(
                    f"Please select a sheet for {file_descriptor.filename}"
                )
            else:
                self.preview_table.set_empty_message("File data not loaded yet")
            self.info_label.config(text="")
            return

        # Load the preview data
        if file_descriptor.preview_rows is not None:
            self.preview_table.load_dataframe(file_descriptor.preview_rows)

            # Update info label
            total_rows = len(file_descriptor.dataframe) if file_descriptor.dataframe is not None else 0
            preview_rows = len(file_descriptor.preview_rows)
            info_text = f"Showing {preview_rows} of {total_rows} rows"

            if file_descriptor.selected_sheet:
                info_text += f" (Sheet: {file_descriptor.selected_sheet})"

            self.info_label.config(text=info_text)
        else:
            self.preview_table.set_empty_message("No preview data available")
            self.info_label.config(text="")

    def _get_file_display_name(self, file_descriptor):
        """Get display name for file in dropdown."""
        display_name = file_descriptor.filename
        if file_descriptor.selected_sheet:
            display_name += f" [{file_descriptor.selected_sheet}]"
        return display_name
