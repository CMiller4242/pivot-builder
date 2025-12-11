"""Widget for displaying data preview."""

import tkinter as tk
from tkinter import ttk

try:
    from tksheet import Sheet
except ImportError:
    Sheet = None


class PreviewTableWidget(ttk.Frame):
    """Widget for displaying data preview in table format using tksheet."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sheet = None

        self._create_ui()

    def _create_ui(self):
        """Create the UI components."""
        if Sheet is None:
            # Fallback if tksheet is not installed
            error_label = ttk.Label(
                self,
                text="tksheet is not installed. Install it with: pip install tksheet",
                foreground="red"
            )
            error_label.pack(pady=20)
            return

        # Create tksheet widget
        self.sheet = Sheet(
            self,
            headers=[],
            data=[],
            height=400,
            width=800
        )
        self.sheet.enable_bindings()
        self.sheet.pack(fill=tk.BOTH, expand=True)

    def load_dataframe(self, df):
        """
        Load a pandas DataFrame into the sheet.

        Args:
            df: pandas DataFrame to display
        """
        if self.sheet is None:
            return

        if df is None or df.empty:
            self.clear()
            return

        try:
            # Convert DataFrame to lists for tksheet
            headers = list(df.columns)
            data = df.values.tolist()

            # Set headers and data
            self.sheet.headers(headers)
            self.sheet.set_sheet_data(data)

            # Auto-size columns
            self.sheet.set_all_column_widths()

        except Exception as e:
            print(f"Error loading dataframe: {e}")

    def clear(self):
        """Clear the sheet."""
        if self.sheet is None:
            return

        self.sheet.headers([])
        self.sheet.set_sheet_data([])

    def set_empty_message(self, message: str = "No data to preview"):
        """Display an empty message when no data is available."""
        if self.sheet is None:
            return

        self.clear()
        # Show a simple message in the first cell
        self.sheet.headers(["Message"])
        self.sheet.set_sheet_data([[message]])
