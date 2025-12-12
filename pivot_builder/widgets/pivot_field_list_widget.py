"""Widget for managing field selections in pivot configuration."""

import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional


class PivotFieldListWidget(ttk.Frame):
    """Widget for displaying and managing a list of fields with add/remove buttons."""

    def __init__(
        self,
        parent,
        title: str,
        on_add: Optional[Callable] = None,
        on_remove: Optional[Callable] = None
    ):
        """
        Initialize field list widget.

        Args:
            parent: Parent widget
            title: Title for the field list (e.g., "Row Fields")
            on_add: Callback when add button clicked
            on_remove: Callback when remove button clicked
        """
        super().__init__(parent)
        self.title = title
        self.on_add = on_add
        self.on_remove = on_remove

        self._create_ui()

    def _create_ui(self):
        """Create the UI components."""
        # Title label
        title_label = ttk.Label(
            self,
            text=self.title,
            font=("TkDefaultFont", 9, "bold")
        )
        title_label.pack(pady=(0, 5))

        # Listbox with scrollbar
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(
            list_frame,
            height=6,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=(5, 0))

        if self.on_add:
            self.add_button = ttk.Button(
                button_frame,
                text="Add →",
                command=self._handle_add,
                width=8
            )
            self.add_button.pack(side=tk.LEFT, padx=2)

        if self.on_remove:
            self.remove_button = ttk.Button(
                button_frame,
                text="← Remove",
                command=self._handle_remove,
                width=8
            )
            self.remove_button.pack(side=tk.LEFT, padx=2)

    def _handle_add(self):
        """Handle add button click."""
        if self.on_add:
            self.on_add()

    def _handle_remove(self):
        """Handle remove button click."""
        selection = self.listbox.curselection()
        if selection and self.on_remove:
            index = selection[0]
            item = self.listbox.get(index)
            self.on_remove(index, item)

    def set_items(self, items: List[str]):
        """
        Set the list of items.

        Args:
            items: List of item names to display
        """
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)

    def get_items(self) -> List[str]:
        """
        Get all items in the list.

        Returns:
            List of item names
        """
        return list(self.listbox.get(0, tk.END))

    def get_selected_index(self) -> Optional[int]:
        """
        Get the selected item index.

        Returns:
            Selected index or None
        """
        selection = self.listbox.curselection()
        return selection[0] if selection else None

    def get_selected_item(self) -> Optional[str]:
        """
        Get the selected item.

        Returns:
            Selected item name or None
        """
        selection = self.listbox.curselection()
        return self.listbox.get(selection[0]) if selection else None

    def clear(self):
        """Clear all items."""
        self.listbox.delete(0, tk.END)
