"""Widget for editing pivot value fields with aggregations."""

import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional

from pivot_builder.models.pivot_model import PivotValueField


class PivotValueEditorWidget(ttk.Frame):
    """Widget for managing value fields with aggregation functions."""

    AGGREGATIONS = ['sum', 'count', 'mean', 'min', 'max']

    def __init__(
        self,
        parent,
        on_add: Optional[Callable] = None,
        on_remove: Optional[Callable] = None
    ):
        """
        Initialize value editor widget.

        Args:
            parent: Parent widget
            on_add: Callback when add button clicked (column, aggregation)
            on_remove: Callback when remove button clicked (index)
        """
        super().__init__(parent)
        self.on_add = on_add
        self.on_remove = on_remove

        self._create_ui()

    def _create_ui(self):
        """Create the UI components."""
        # Title
        title_label = ttk.Label(
            self,
            text="Value Fields",
            font=("TkDefaultFont", 9, "bold")
        )
        title_label.pack(pady=(0, 5))

        # Value field list with scrollbar
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.value_listbox = tk.Listbox(
            list_frame,
            height=6,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        scrollbar.config(command=self.value_listbox.yview)

        self.value_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add controls
        add_frame = ttk.Frame(self)
        add_frame.pack(fill=tk.X, pady=(5, 0))

        # Aggregation dropdown
        ttk.Label(add_frame, text="Function:").pack(side=tk.LEFT, padx=(0, 5))

        self.agg_var = tk.StringVar(value=self.AGGREGATIONS[0])
        self.agg_combo = ttk.Combobox(
            add_frame,
            textvariable=self.agg_var,
            values=self.AGGREGATIONS,
            state='readonly',
            width=10
        )
        self.agg_combo.pack(side=tk.LEFT, padx=(0, 5))

        # Buttons
        if self.on_add:
            self.add_button = ttk.Button(
                add_frame,
                text="Add →",
                command=self._handle_add,
                width=8
            )
            self.add_button.pack(side=tk.LEFT, padx=2)

        if self.on_remove:
            self.remove_button = ttk.Button(
                add_frame,
                text="← Remove",
                command=self._handle_remove,
                width=8
            )
            self.remove_button.pack(side=tk.LEFT, padx=2)

    def _handle_add(self):
        """Handle add button click."""
        if self.on_add:
            aggregation = self.agg_var.get()
            self.on_add(aggregation)

    def _handle_remove(self):
        """Handle remove button click."""
        selection = self.value_listbox.curselection()
        if selection and self.on_remove:
            index = selection[0]
            self.on_remove(index)

    def set_value_fields(self, value_fields: List[PivotValueField]):
        """
        Set the list of value fields.

        Args:
            value_fields: List of PivotValueField objects
        """
        self.value_listbox.delete(0, tk.END)
        for vf in value_fields:
            display = f"{vf.column} ({vf.aggregation})"
            self.value_listbox.insert(tk.END, display)

    def get_selected_index(self) -> Optional[int]:
        """
        Get the selected value field index.

        Returns:
            Selected index or None
        """
        selection = self.value_listbox.curselection()
        return selection[0] if selection else None

    def clear(self):
        """Clear all value fields."""
        self.value_listbox.delete(0, tk.END)
