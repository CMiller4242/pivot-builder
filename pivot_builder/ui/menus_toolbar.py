"""Menus and toolbar for the application."""

import tkinter as tk
from tkinter import ttk


class MenuBar(tk.Menu):
    """Main menu bar for the application."""

    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.app_controller = app_controller

        # File menu
        self.file_menu = tk.Menu(self, tearoff=0)
        self.file_menu.add_command(
            label="Add Files...",
            command=self._on_add_files,
            accelerator="Ctrl+O"
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Export...")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=parent.quit)
        self.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self, tearoff=0)
        self.edit_menu.add_command(label="Clear All")
        self.add_cascade(label="Edit", menu=self.edit_menu)

        # View menu
        self.view_menu = tk.Menu(self, tearoff=0)
        self.view_menu.add_command(label="Refresh")
        self.add_cascade(label="View", menu=self.view_menu)

        # Help menu
        self.help_menu = tk.Menu(self, tearoff=0)
        self.help_menu.add_command(label="About")
        self.add_cascade(label="Help", menu=self.help_menu)

    def _on_add_files(self):
        """Handle Add Files menu action."""
        if self.app_controller:
            self.app_controller.on_add_files()


class ToolBar(ttk.Frame):
    """Toolbar for the application."""

    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.app_controller = app_controller

        # Toolbar buttons
        self.open_button = ttk.Button(
            self,
            text="Add Files",
            command=self._on_add_files
        )
        self.open_button.pack(side=tk.LEFT, padx=2)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        self.refresh_button = ttk.Button(
            self,
            text="Refresh",
            command=self._on_refresh
        )
        self.refresh_button.pack(side=tk.LEFT, padx=2)

    def _on_add_files(self):
        """Handle Add Files toolbar action."""
        if self.app_controller:
            self.app_controller.on_add_files()

    def _on_refresh(self):
        """Handle Refresh toolbar action."""
        if self.app_controller:
            self.app_controller.refresh_all()
