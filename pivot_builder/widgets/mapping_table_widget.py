"""Widget for displaying column mappings."""

import tkinter as tk
from tkinter import ttk

try:
    from tksheet import Sheet
except ImportError:
    Sheet = None


class MappingTableWidget(ttk.Frame):
    """Widget for displaying and editing column mappings using tksheet."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.mapping_model = None
        self.file_list = []  # List of file descriptors

        # Create UI
        self._create_ui()

    def _create_ui(self):
        """Create the UI components."""
        if Sheet is None:
            # Fallback if tksheet is not available
            self.label = ttk.Label(
                self,
                text="tksheet library not available. Please install it.",
                foreground="red"
            )
            self.label.pack(pady=20)
            return

        # Create tksheet
        self.sheet = Sheet(
            self,
            headers=[],
            data=[],
            theme="light blue",
            width=800,
            height=400
        )
        self.sheet.enable_bindings()
        self.sheet.pack(fill=tk.BOTH, expand=True)

        # Bind cell edit event
        self.sheet.bind("<<SheetModified>>", self._on_cell_edited)

        # Initial empty message
        self.set_empty_message("No files loaded. Add files to see column mappings.")

    def load_mapping(self, mapping_model):
        """
        Load mapping model into the table.

        Args:
            mapping_model: ColumnMappingModel to display
        """
        if Sheet is None:
            return

        self.mapping_model = mapping_model

        # Get file list from controller
        if self.controller:
            self.file_list = self.controller.get_files_list()
        else:
            self.file_list = []

        # Check if there are any mappings to display
        if not mapping_model.canonical_fields or not self.file_list:
            self.set_empty_message(
                "No mappings available. Load files to generate mappings."
            )
            return

        # Build headers: ["Canonical Field", "file1.csv", "file2.xlsx", ...]
        headers = ["Canonical Field"] + [
            self._get_file_display_name(fd) for fd in self.file_list
        ]

        # Build data rows
        data = []
        for canonical_field in mapping_model.canonical_fields:
            row = [canonical_field.name]

            # Add mapping for each file
            for file_desc in self.file_list:
                # Find which original column maps to this canonical
                original_col = self._find_original_column(
                    file_desc.id,
                    canonical_field.name
                )
                row.append(original_col if original_col else "")

            data.append(row)

        # Update sheet
        self.sheet.headers(headers)
        self.sheet.set_sheet_data(data)

        # Make first column (Canonical Field) read-only
        self.sheet.readonly_columns([0])

        # Auto-resize columns
        self.sheet.set_all_column_widths()

    def _find_original_column(self, file_id: str, canonical_name: str) -> str:
        """
        Find the original column name that maps to a canonical field.

        Args:
            file_id: File ID
            canonical_name: Canonical field name

        Returns:
            Original column name or empty string if not found
        """
        if not self.mapping_model:
            return ""

        # Look through file_column_to_canonical mapping
        if file_id in self.mapping_model.file_column_to_canonical:
            for original_col, mapped_canonical in self.mapping_model.file_column_to_canonical[file_id].items():
                if mapped_canonical == canonical_name:
                    return original_col

        return ""

    def _on_cell_edited(self, event=None):
        """Handle cell edit events."""
        if not self.mapping_model or not self.file_list:
            return

        # Get edited cells
        edited_cells = self.sheet.get_currently_selected()
        if not edited_cells:
            return

        # Process each edited cell
        for row, col in edited_cells:
            if col == 0:
                # Can't edit canonical field column (should be read-only)
                continue

            # Get canonical field for this row
            if row >= len(self.mapping_model.canonical_fields):
                continue
            canonical_field = self.mapping_model.canonical_fields[row]

            # Get file for this column
            file_col_index = col - 1  # Subtract 1 for canonical field column
            if file_col_index >= len(self.file_list):
                continue
            file_desc = self.file_list[file_col_index]

            # Get new value
            new_value = self.sheet.get_cell_data(row, col)

            # Find old original column that was mapped to this canonical
            old_original = self._find_original_column(file_desc.id, canonical_field.name)

            # Handle the edit
            if new_value and new_value.strip():
                # User entered a new mapping
                new_original = new_value.strip()

                # Notify controller of manual edit
                if self.controller and old_original != new_original:
                    self.controller.on_manual_canonical_edit(
                        file_desc.id,
                        new_original,
                        canonical_field.name
                    )
            else:
                # User cleared the mapping
                if old_original and self.controller:
                    self.controller.on_manual_canonical_edit(
                        file_desc.id,
                        old_original,
                        None  # Unmap
                    )

    def set_empty_message(self, message: str):
        """
        Display an empty state message.

        Args:
            message: Message to display
        """
        if Sheet is None:
            return

        self.sheet.headers(["Message"])
        self.sheet.set_sheet_data([[message]])
        self.sheet.readonly_columns([0])

    def _get_file_display_name(self, file_descriptor) -> str:
        """
        Get display name for a file.

        Args:
            file_descriptor: FileDescriptor object

        Returns:
            Display name for the file
        """
        display_name = file_descriptor.filename
        if file_descriptor.selected_sheet:
            display_name += f" [{file_descriptor.selected_sheet}]"
        return display_name
