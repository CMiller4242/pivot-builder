"""Main entry point for Pivot Builder application."""

import tkinter as tk

from pivot_builder.config.logging_config import logger
from pivot_builder.controllers.app_controller import AppController
from pivot_builder.controllers.file_controller import FileController
from pivot_builder.controllers.mapping_controller import MappingController
from pivot_builder.controllers.preview_controller import PreviewController
from pivot_builder.controllers.pivot_controller import PivotController
from pivot_builder.controllers.export_controller import ExportController
from pivot_builder.ui.main_window import MainWindow


def main():
    """Initialize and run the Pivot Builder application."""
    logger.info("Starting Pivot Builder application")

    # Create root Tk instance
    root = tk.Tk()

    # Create main application controller
    app_controller = AppController()

    # Create sub-controllers
    file_controller = FileController(app_controller)
    mapping_controller = MappingController(
        app_controller,
        app_controller.column_normalization_service,
        app_controller.column_matching_service,
        app_controller.column_mapping_model
    )
    preview_controller = PreviewController(app_controller)
    pivot_controller = PivotController(app_controller, app_controller.pivot_engine_service)
    export_controller = ExportController(app_controller)

    # Wire controllers to app controller
    app_controller.set_file_controller(file_controller)
    app_controller.set_mapping_controller(mapping_controller)
    app_controller.set_preview_controller(preview_controller)
    app_controller.set_pivot_controller(pivot_controller)
    app_controller.set_export_controller(export_controller)

    # Create main window
    main_window = MainWindow(root, app_controller)

    # Wire views to controllers
    file_controller.set_view(main_window.file_panel)
    mapping_controller.set_view(main_window.mapping_view)
    preview_controller.set_view(main_window.preview_view)
    pivot_controller.set_view(main_window.pivot_view)

    logger.info("Application initialized successfully")

    # Start the main loop
    main_window.run()


if __name__ == "__main__":
    main()
