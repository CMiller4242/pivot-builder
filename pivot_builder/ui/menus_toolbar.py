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
        self.file_menu.add_command(label="Open Files...")
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


class ToolBar(ttk.Frame):
    """Toolbar for the application."""

    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.app_controller = app_controller

        # Placeholder toolbar buttons
        self.open_button = ttk.Button(self, text="Open")
        self.open_button.pack(side=tk.LEFT, padx=2)

        self.save_button = ttk.Button(self, text="Save")
        self.save_button.pack(side=tk.LEFT, padx=2)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        self.refresh_button = ttk.Button(self, text="Refresh")
        self.refresh_button.pack(side=tk.LEFT, padx=2)
