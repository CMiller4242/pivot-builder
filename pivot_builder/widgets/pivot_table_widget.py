"""Widget for displaying pivot table results."""

import tkinter as tk
from tkinter import ttk

try:
    from tksheet import Sheet
except ImportError:
    Sheet = None


class PivotTableWidget(ttk.Frame):
    """Widget for displaying pivot tables using tksheet."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

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

        # Initial empty message
        self.set_empty_message("No pivot table generated.\n\nTo create a pivot:\n1. Configure rows/columns/values\n2. Click 'Build Pivot'")

    def load_pivot(self, pivot_df):
        """
        Load pivot DataFrame into the table.

        Args:
            pivot_df: pandas DataFrame with pivot results
        """
        if Sheet is None:
            return

        if pivot_df is None or len(pivot_df) == 0:
            self.set_empty_message("Pivot result is empty.\n\nCheck your configuration and data.")
            return

        try:
            # Get headers and data
            headers = list(pivot_df.columns)
            data = pivot_df.values.tolist()

            # Update sheet
            self.sheet.headers(headers)
            self.sheet.set_sheet_data(data)

            # Auto-resize columns
            self.sheet.set_all_column_widths()

        except Exception as e:
            self.set_empty_message(f"Error loading pivot: {str(e)}")

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
