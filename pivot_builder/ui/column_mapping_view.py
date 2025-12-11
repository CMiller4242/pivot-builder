"""Column mapping view."""

import tkinter as tk
from tkinter import ttk, messagebox

from pivot_builder.models.mapping_model import MappingRule
from pivot_builder.widgets.mapping_table_widget import MappingTableWidget


class ColumnMappingView(ttk.Frame):
    """View for mapping columns across files."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Track current rule
        self.current_rule = MappingRule()

        # Create UI
        self._create_ui()

    def _create_ui(self):
        """Create the UI components."""
        # Top panel: Normalization rules
        rules_frame = ttk.LabelFrame(self, text="Normalization Rules", padding=10)
        rules_frame.pack(fill=tk.X, padx=10, pady=10)

        self._create_rule_controls(rules_frame)

        # Middle panel: Control buttons
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.rebuild_button = ttk.Button(
            control_frame,
            text="Rebuild Suggestions",
            command=self._on_rebuild_clicked
        )
        self.rebuild_button.pack(side=tk.LEFT, padx=5)

        # Info label
        self.info_label = ttk.Label(
            control_frame,
            text="",
            foreground="gray",
            font=("TkDefaultFont", 8)
        )
        self.info_label.pack(side=tk.LEFT, padx=10)

        # Main panel: Mapping table
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.mapping_table = MappingTableWidget(table_frame, self.controller)
        self.mapping_table.pack(fill=tk.BOTH, expand=True)

    def _create_rule_controls(self, parent):
        """
        Create checkbox controls for normalization rules.

        Args:
            parent: Parent widget for the controls
        """
        # Create checkbox variables
        self.trim_var = tk.BooleanVar(value=self.current_rule.trim_whitespace)
        self.lower_var = tk.BooleanVar(value=self.current_rule.to_lower)
        self.spaces_var = tk.BooleanVar(value=self.current_rule.replace_spaces_with_underscore)
        self.special_var = tk.BooleanVar(value=self.current_rule.remove_special_chars)

        # Create checkboxes in a grid
        checkboxes_frame = ttk.Frame(parent)
        checkboxes_frame.pack(fill=tk.X)

        ttk.Checkbutton(
            checkboxes_frame,
            text="Trim whitespace",
            variable=self.trim_var,
            command=self._on_rule_changed
        ).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)

        ttk.Checkbutton(
            checkboxes_frame,
            text="Convert to lowercase",
            variable=self.lower_var,
            command=self._on_rule_changed
        ).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Checkbutton(
            checkboxes_frame,
            text="Replace spaces with underscores",
            variable=self.spaces_var,
            command=self._on_rule_changed
        ).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)

        ttk.Checkbutton(
            checkboxes_frame,
            text="Remove special characters",
            variable=self.special_var,
            command=self._on_rule_changed
        ).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

    def _on_rule_changed(self):
        """Handle changes to normalization rule checkboxes."""
        # Update current rule from checkbox states
        self.current_rule = MappingRule(
            trim_whitespace=self.trim_var.get(),
            to_lower=self.lower_var.get(),
            replace_spaces_with_underscore=self.spaces_var.get(),
            remove_special_chars=self.special_var.get()
        )

        # Notify controller
        if self.controller:
            self.controller.on_normalization_rule_changed(self.current_rule)

    def _on_rebuild_clicked(self):
        """Handle rebuild suggestions button click."""
        if self.controller:
            self.controller.rebuild_mapping_from_files()

    def refresh_mapping(self, mapping_model):
        """
        Refresh the mapping display with new mapping model.

        Args:
            mapping_model: ColumnMappingModel to display
        """
        # Update info label
        num_canonical = len(mapping_model.canonical_fields)
        num_files = len(mapping_model.file_column_to_canonical)
        self.info_label.config(
            text=f"{num_canonical} canonical fields from {num_files} files"
        )

        # Update mapping table
        self.mapping_table.load_mapping(mapping_model)

    def show_error(self, message: str):
        """
        Show an error message to the user.

        Args:
            message: Error message to display
        """
        messagebox.showerror("Mapping Error", message)
