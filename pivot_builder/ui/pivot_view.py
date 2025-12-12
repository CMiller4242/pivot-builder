"""Pivot builder view."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from pivot_builder.widgets.pivot_field_list_widget import PivotFieldListWidget
from pivot_builder.widgets.pivot_value_editor_widget import PivotValueEditorWidget
from pivot_builder.widgets.pivot_table_widget import PivotTableWidget


class PivotView(ttk.Frame):
    """View for building and previewing pivot tables."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self._create_ui()

    def _create_ui(self):
        """Create the UI components."""
        # Main layout: Configuration (top) + Preview (bottom)
        config_frame = ttk.LabelFrame(self, text="Pivot Configuration", padding=10)
        config_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

        preview_frame = ttk.LabelFrame(self, text="Pivot Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Configuration layout
        self._create_configuration_ui(config_frame)

        # Preview layout
        self._create_preview_ui(preview_frame)

    def _create_configuration_ui(self, parent):
        """Create the configuration UI."""
        # Top row: Available fields
        available_frame = ttk.Frame(parent)
        available_frame.pack(fill=tk.X, pady=(0, 10))

        self.available_fields = PivotFieldListWidget(
            available_frame,
            title="Available Fields",
            on_add=None,  # No add button for available fields
            on_remove=None
        )
        self.available_fields.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Middle row: Field selections
        fields_frame = ttk.Frame(parent)
        fields_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Rows
        self.row_fields = PivotFieldListWidget(
            fields_frame,
            title="Row Fields",
            on_add=self._on_add_row,
            on_remove=self._on_remove_row
        )
        self.row_fields.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Columns
        self.column_fields = PivotFieldListWidget(
            fields_frame,
            title="Column Fields",
            on_add=self._on_add_column,
            on_remove=self._on_remove_column
        )
        self.column_fields.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Values
        self.value_fields = PivotValueEditorWidget(
            fields_frame,
            on_add=self._on_add_value,
            on_remove=self._on_remove_value
        )
        self.value_fields.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Bottom row: Build button
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)

        self.build_button = ttk.Button(
            button_frame,
            text="Build Pivot",
            command=self._on_build_pivot
        )
        self.build_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(
            button_frame,
            text="Clear All",
            command=self._on_clear_all
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Config save/load buttons
        ttk.Separator(button_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)

        self.save_config_button = ttk.Button(
            button_frame,
            text="Save Config",
            command=self._on_save_config
        )
        self.save_config_button.pack(side=tk.LEFT, padx=5)

        self.load_config_button = ttk.Button(
            button_frame,
            text="Load Config",
            command=self._on_load_config
        )
        self.load_config_button.pack(side=tk.LEFT, padx=5)

        # Info label
        self.info_label = ttk.Label(
            button_frame,
            text="",
            foreground="gray",
            font=("TkDefaultFont", 8)
        )
        self.info_label.pack(side=tk.LEFT, padx=10)

    def _create_preview_ui(self, parent):
        """Create the preview UI."""
        # Export buttons
        export_frame = ttk.Frame(parent)
        export_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(export_frame, text="Export Pivot:", font=("TkDefaultFont", 9, "bold")).pack(side=tk.LEFT, padx=(0, 10))

        self.export_csv_button = ttk.Button(
            export_frame,
            text="Export as CSV",
            command=self._on_export_csv
        )
        self.export_csv_button.pack(side=tk.LEFT, padx=5)

        self.export_xlsx_button = ttk.Button(
            export_frame,
            text="Export as XLSX",
            command=self._on_export_xlsx
        )
        self.export_xlsx_button.pack(side=tk.LEFT, padx=5)

        self.export_json_button = ttk.Button(
            export_frame,
            text="Export as JSON",
            command=self._on_export_json
        )
        self.export_json_button.pack(side=tk.LEFT, padx=5)

        # Pivot table
        self.pivot_table = PivotTableWidget(parent, self.controller)
        self.pivot_table.pack(fill=tk.BOTH, expand=True)

    def _on_add_row(self):
        """Handle add row field."""
        selected = self.available_fields.get_selected_item()
        if selected and self.controller:
            self.controller.add_row_field(selected)
            self._refresh_field_lists()

    def _on_remove_row(self, index, item):
        """Handle remove row field."""
        if self.controller:
            self.controller.remove_row_field(item)
            self._refresh_field_lists()

    def _on_add_column(self):
        """Handle add column field."""
        selected = self.available_fields.get_selected_item()
        if selected and self.controller:
            self.controller.add_column_field(selected)
            self._refresh_field_lists()

    def _on_remove_column(self, index, item):
        """Handle remove column field."""
        if self.controller:
            self.controller.remove_column_field(item)
            self._refresh_field_lists()

    def _on_add_value(self, aggregation):
        """Handle add value field."""
        selected = self.available_fields.get_selected_item()
        if selected and self.controller:
            self.controller.add_value_field(selected, aggregation)
            self._refresh_field_lists()

    def _on_remove_value(self, index):
        """Handle remove value field."""
        if self.controller:
            self.controller.remove_value_field(index)
            self._refresh_field_lists()

    def _on_build_pivot(self):
        """Handle build pivot button click."""
        if self.controller:
            self.controller.rebuild_pivot()

    def _on_clear_all(self):
        """Handle clear all button click."""
        if self.controller:
            self.controller.clear_configuration()
            self._refresh_field_lists()
            self.pivot_table.set_empty_message("Configuration cleared.\n\nConfigure pivot and click 'Build Pivot'.")

    def _refresh_field_lists(self):
        """Refresh all field lists from controller."""
        if not self.controller:
            return

        # Update row fields
        self.row_fields.set_items(self.controller.config.rows)

        # Update column fields
        self.column_fields.set_items(self.controller.config.columns)

        # Update value fields
        self.value_fields.set_value_fields(self.controller.config.values)

        # Update info
        num_rows = len(self.controller.config.rows)
        num_cols = len(self.controller.config.columns)
        num_vals = len(self.controller.config.values)
        self.info_label.config(
            text=f"Rows: {num_rows}, Columns: {num_cols}, Values: {num_vals}"
        )

    def refresh_available_fields(self):
        """Refresh the list of available fields from controller."""
        if not self.controller:
            return

        available = self.controller.get_available_fields()
        self.available_fields.set_items(available)

        # Also refresh current selections
        self._refresh_field_lists()

    def load_pivot_preview(self, pivot_df):
        """
        Load pivot DataFrame into preview.

        Args:
            pivot_df: pandas DataFrame with pivot results
        """
        self.pivot_table.load_pivot(pivot_df)

    def show_error(self, message: str):
        """
        Show error message to user.

        Args:
            message: Error message
        """
        messagebox.showerror("Pivot Error", message)

    def _on_save_config(self):
        """Handle save config button click."""
        if not self.controller:
            return

        # Open file dialog for save location
        file_path = filedialog.asksaveasfilename(
            title="Save Pivot Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            success = self.controller.save_config(file_path)
            if success:
                messagebox.showinfo("Success", f"Configuration saved to:\n{file_path}")

    def _on_load_config(self):
        """Handle load config button click."""
        if not self.controller:
            return

        # Open file dialog for load location
        file_path = filedialog.askopenfilename(
            title="Load Pivot Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            success = self.controller.load_config(file_path)
            if success:
                messagebox.showinfo("Success", f"Configuration loaded from:\n{file_path}")

    def _on_export_csv(self):
        """Handle export CSV button click."""
        if not self.controller:
            return

        # Check if there's pivot data to export
        if self.controller.pivot_df is None or len(self.controller.pivot_df) == 0:
            messagebox.showwarning("No Data", "Please build a pivot table first before exporting.")
            return

        # Open file dialog for save location
        file_path = filedialog.asksaveasfilename(
            title="Export Pivot as CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            export_controller = self.controller.app.export_controller
            if export_controller:
                success = export_controller.export_csv(file_path)
                if success:
                    messagebox.showinfo("Success", f"Pivot exported to CSV:\n{file_path}")
                else:
                    messagebox.showerror("Error", "Failed to export pivot. Check logs for details.")

    def _on_export_xlsx(self):
        """Handle export XLSX button click."""
        if not self.controller:
            return

        # Check if there's pivot data to export
        if self.controller.pivot_df is None or len(self.controller.pivot_df) == 0:
            messagebox.showwarning("No Data", "Please build a pivot table first before exporting.")
            return

        # Open file dialog for save location
        file_path = filedialog.asksaveasfilename(
            title="Export Pivot as Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if file_path:
            export_controller = self.controller.app.export_controller
            if export_controller:
                success = export_controller.export_xlsx(file_path)
                if success:
                    messagebox.showinfo("Success", f"Pivot exported to Excel:\n{file_path}")
                else:
                    messagebox.showerror("Error", "Failed to export pivot. Check logs for details.")

    def _on_export_json(self):
        """Handle export JSON button click."""
        if not self.controller:
            return

        # Check if there's pivot data to export
        if self.controller.pivot_df is None or len(self.controller.pivot_df) == 0:
            messagebox.showwarning("No Data", "Please build a pivot table first before exporting.")
            return

        # Open file dialog for save location
        file_path = filedialog.asksaveasfilename(
            title="Export Pivot as JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            export_controller = self.controller.app.export_controller
            if export_controller:
                success = export_controller.export_json(file_path)
                if success:
                    messagebox.showinfo("Success", f"Pivot exported to JSON:\n{file_path}")
                else:
                    messagebox.showerror("Error", "Failed to export pivot. Check logs for details.")
