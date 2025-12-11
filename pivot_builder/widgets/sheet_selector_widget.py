"""Widget for selecting Excel sheets."""

import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional


class SheetSelectorWidget(ttk.Frame):
    """Widget for selecting sheets from Excel files."""

    def __init__(self, parent, file_id: str, sheets: List[str], on_select: Callable):
        """
        Initialize sheet selector widget.

        Args:
            parent: Parent widget
            file_id: ID of the file this selector belongs to
            sheets: List of sheet names
            on_select: Callback function(file_id, sheet_name)
        """
        super().__init__(parent)
        self.file_id = file_id
        self.sheets = sheets
        self.on_select = on_select
        self.selected_sheet = None

        self._create_ui()

    def _create_ui(self):
        """Create the UI components."""
        # Label
        label = ttk.Label(self, text="Select sheet:", font=("TkDefaultFont", 8))
        label.pack(side=tk.LEFT, padx=(0, 5))

        # Combobox for sheet selection
        self.sheet_var = tk.StringVar()
        self.combobox = ttk.Combobox(
            self,
            textvariable=self.sheet_var,
            values=self.sheets,
            state='readonly',
            width=20
        )
        self.combobox.pack(side=tk.LEFT)

        # Set default selection to first sheet if available
        if self.sheets:
            self.combobox.current(0)
            self.selected_sheet = self.sheets[0]

        # Bind selection event
        self.combobox.bind('<<ComboboxSelected>>', self._on_sheet_selected)

    def _on_sheet_selected(self, event=None):
        """Handle sheet selection."""
        selected = self.sheet_var.get()
        if selected and selected != self.selected_sheet:
            self.selected_sheet = selected
            if self.on_select:
                self.on_select(self.file_id, selected)

    def get_selected_sheet(self) -> Optional[str]:
        """Get the currently selected sheet."""
        return self.selected_sheet
