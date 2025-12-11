"""Main application window."""

import tkinter as tk
from tkinter import ttk

from pivot_builder.config import app_config
from pivot_builder.ui.menus_toolbar import MenuBar, ToolBar
from pivot_builder.ui.file_panel import FilePanel
from pivot_builder.ui.column_mapping_view import ColumnMappingView
from pivot_builder.ui.preview_view import PreviewView
from pivot_builder.ui.pivot_builder_view import PivotBuilderView
from pivot_builder.ui.validation_panel import ValidationPanel
from pivot_builder.widgets.status_bar import StatusBar


class MainWindow:
    """Main application window."""

    def __init__(self, root, app_controller):
        self.root = root
        self.app_controller = app_controller

        # Configure root window
        self.root.title(app_config.WINDOW_TITLE)
        self.root.geometry(f"{app_config.WINDOW_MIN_WIDTH}x{app_config.WINDOW_MIN_HEIGHT}")
        self.root.minsize(app_config.WINDOW_MIN_WIDTH, app_config.WINDOW_MIN_HEIGHT)

        # Create menu bar
        self.menu_bar = MenuBar(self.root, self.app_controller)
        self.root.config(menu=self.menu_bar)

        # Create toolbar
        self.toolbar = ToolBar(self.root, self.app_controller)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Create main content area with PanedWindow
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Left panel - Files
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)

        # Right panel - Notebook with tabs
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=3)

        # Create file panel
        self.file_panel = FilePanel(self.left_frame, self.app_controller.file_controller)
        self.file_panel.pack(fill=tk.BOTH, expand=True)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.mapping_view = ColumnMappingView(self.notebook, self.app_controller.mapping_controller)
        self.notebook.add(self.mapping_view, text="Mapping")

        self.preview_view = PreviewView(self.notebook, self.app_controller.preview_controller)
        self.notebook.add(self.preview_view, text="Preview")

        self.pivot_view = PivotBuilderView(self.notebook, self.app_controller.pivot_controller)
        self.notebook.add(self.pivot_view, text="Pivot")

        self.validation_panel = ValidationPanel(self.notebook, None)
        self.notebook.add(self.validation_panel, text="Validation")

        # Create status bar
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Set main window reference in app_controller
        self.app_controller.set_main_window(self)

    def show_preview_tab(self):
        """Switch to the Preview tab."""
        # Find the index of the Preview tab (it's the second tab, index 1)
        self.notebook.select(1)  # 0=Mapping, 1=Preview, 2=Pivot, 3=Validation

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()
