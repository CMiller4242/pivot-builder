"""Widget for displaying column lists."""

import tkinter as tk
from tkinter import ttk


class ColumnListWidget(ttk.Frame):
    """Widget for displaying a list of columns with their mappings."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        # Create UI
        self._create_ui()

    def _create_ui(self):
        """Create the UI components."""
        # Title label
        self.title_label = ttk.Label(
            self,
            text="Column Details",
            font=("TkDefaultFont", 10, "bold")
        )
        self.title_label.pack(pady=(5, 10))

        # Scrollable frame for column list
        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Initial empty state
        self.show_empty_state()

    def load_columns(self, file_descriptor, mapping_model=None):
        """
        Load and display columns for a file.

        Args:
            file_descriptor: FileDescriptor to display columns for
            mapping_model: Optional ColumnMappingModel for showing mappings
        """
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not file_descriptor or not file_descriptor.original_columns:
            self.show_empty_state()
            return

        # Update title
        self.title_label.config(text=f"Columns: {file_descriptor.filename}")

        # Display each column
        for idx, original_col in enumerate(file_descriptor.original_columns):
            self._create_column_item(
                original_col,
                file_descriptor.id,
                mapping_model,
                idx
            )

    def _create_column_item(self, original_col: str, file_id: str, mapping_model, index: int):
        """
        Create a display item for a single column.

        Args:
            original_col: Original column name
            file_id: File ID
            mapping_model: ColumnMappingModel for getting mappings
            index: Index of the column
        """
        # Container frame for this column
        item_frame = ttk.Frame(self.scrollable_frame, relief=tk.RIDGE, borderwidth=1)
        item_frame.pack(fill=tk.X, padx=5, pady=2)

        # Column index and original name
        name_frame = ttk.Frame(item_frame)
        name_frame.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(
            name_frame,
            text=f"{index + 1}.",
            font=("TkDefaultFont", 8, "bold"),
            width=3
        ).pack(side=tk.LEFT)

        ttk.Label(
            name_frame,
            text=original_col,
            font=("TkDefaultFont", 9, "bold")
        ).pack(side=tk.LEFT)

        # Show normalized name and canonical mapping if available
        if mapping_model:
            # Normalized name
            normalized = mapping_model.normalized_columns.get(file_id, {}).get(original_col)
            if normalized:
                norm_frame = ttk.Frame(item_frame)
                norm_frame.pack(fill=tk.X, padx=15, pady=1)

                ttk.Label(
                    norm_frame,
                    text="Normalized:",
                    font=("TkDefaultFont", 8),
                    foreground="gray"
                ).pack(side=tk.LEFT, padx=(0, 5))

                ttk.Label(
                    norm_frame,
                    text=normalized,
                    font=("TkDefaultFont", 8, "italic"),
                    foreground="blue"
                ).pack(side=tk.LEFT)

            # Canonical mapping
            canonical = mapping_model.file_column_to_canonical.get(file_id, {}).get(original_col)
            if canonical:
                canon_frame = ttk.Frame(item_frame)
                canon_frame.pack(fill=tk.X, padx=15, pady=1)

                ttk.Label(
                    canon_frame,
                    text="Maps to:",
                    font=("TkDefaultFont", 8),
                    foreground="gray"
                ).pack(side=tk.LEFT, padx=(0, 5))

                ttk.Label(
                    canon_frame,
                    text=canonical,
                    font=("TkDefaultFont", 8, "bold"),
                    foreground="green"
                ).pack(side=tk.LEFT)

    def show_empty_state(self):
        """Show empty state message."""
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Reset title
        self.title_label.config(text="Column Details")

        # Show empty message
        empty_label = ttk.Label(
            self.scrollable_frame,
            text="No file selected or no columns available",
            foreground="gray",
            font=("TkDefaultFont", 9, "italic")
        )
        empty_label.pack(pady=20)
