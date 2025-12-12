"""Validation panel for data quality checks."""

import tkinter as tk
from tkinter import ttk

from pivot_builder.models.validation_model import ValidationReport


class ValidationPanel(ttk.Frame):
    """Panel for displaying validation results."""

    def __init__(self, parent, controller):
        """
        Initialize validation panel.

        Args:
            parent: Parent widget
            controller: ValidationController instance
        """
        super().__init__(parent)
        self.controller = controller

        # Create UI
        self._create_ui()

    def _create_ui(self):
        """Create the validation UI."""
        # Top summary strip
        summary_frame = ttk.Frame(self)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(summary_frame, text="Validation Summary:",
                 font=("TkDefaultFont", 10, "bold")).pack(side=tk.LEFT, padx=(0, 20))

        # Error count
        self.error_label = ttk.Label(summary_frame, text="Errors: 0", foreground="red")
        self.error_label.pack(side=tk.LEFT, padx=10)

        # Warning count
        self.warning_label = ttk.Label(summary_frame, text="Warnings: 0", foreground="orange")
        self.warning_label.pack(side=tk.LEFT, padx=10)

        # Info count
        self.info_label = ttk.Label(summary_frame, text="Info: 0", foreground="blue")
        self.info_label.pack(side=tk.LEFT, padx=10)

        # Refresh button
        ttk.Button(summary_frame, text="Refresh Validation",
                  command=self._on_refresh).pack(side=tk.RIGHT, padx=5)

        # Separator
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)

        # Scrollable issue list area
        self._create_issue_list()

    def _create_issue_list(self):
        """Create scrollable issue list."""
        # Container frame
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Canvas and scrollbar for scrolling
        canvas = tk.Canvas(list_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = canvas

        # Initial message
        ttk.Label(self.scrollable_frame,
                 text="No validation issues. Click 'Refresh Validation' to run checks.",
                 foreground="gray").pack(pady=20)

    def _on_refresh(self):
        """Handle refresh button click."""
        if self.controller:
            self.controller.refresh()

    def refresh_report(self, report: ValidationReport):
        """
        Update UI with validation report.

        Args:
            report: ValidationReport to display
        """
        # Update summary counts
        error_count = len(report.errors())
        warning_count = len(report.warnings())
        info_count = len(report.infos())

        self.error_label.config(text=f"Errors: {error_count}")
        self.warning_label.config(text=f"Warnings: {warning_count}")
        self.info_label.config(text=f"Info: {info_count}")

        # Clear existing issue widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Display issues grouped by level
        if not report.issues:
            ttk.Label(self.scrollable_frame,
                     text="✓ No validation issues found",
                     foreground="green",
                     font=("TkDefaultFont", 10, "bold")).pack(pady=20)
            return

        # Display errors
        if report.errors():
            self._add_issue_section("Errors", report.errors(), "red")

        # Display warnings
        if report.warnings():
            self._add_issue_section("Warnings", report.warnings(), "orange")

        # Display infos
        if report.infos():
            self._add_issue_section("Info", report.infos(), "blue")

    def _add_issue_section(self, title: str, issues: list, color: str):
        """
        Add a section for a specific issue level.

        Args:
            title: Section title (e.g., "Errors")
            issues: List of ValidationIssue objects
            color: Color for the section
        """
        # Section header
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.pack(fill=tk.X, pady=(10, 5), padx=5)

        ttk.Label(header_frame,
                 text=f"{title} ({len(issues)})",
                 font=("TkDefaultFont", 9, "bold"),
                 foreground=color).pack(side=tk.LEFT)

        # Issue items
        for issue in issues:
            self._add_issue_item(issue, color)

    def _add_issue_item(self, issue, color: str):
        """
        Add a single issue item to the list.

        Args:
            issue: ValidationIssue object
            color: Color for the level badge
        """
        item_frame = ttk.Frame(self.scrollable_frame, relief=tk.RIDGE, borderwidth=1)
        item_frame.pack(fill=tk.X, pady=2, padx=10)

        # Level badge
        badge_frame = ttk.Frame(item_frame)
        badge_frame.pack(side=tk.LEFT, padx=(5, 10), pady=5)

        badge_label = tk.Label(badge_frame,
                              text=issue.level.upper()[:1],
                              width=2,
                              bg=color,
                              fg="white",
                              font=("TkDefaultFont", 8, "bold"))
        badge_label.pack()

        # Content
        content_frame = ttk.Frame(item_frame)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)

        # Code
        ttk.Label(content_frame,
                 text=issue.code,
                 font=("TkDefaultFont", 8, "bold"),
                 foreground="gray").pack(anchor=tk.W)

        # Message
        ttk.Label(content_frame,
                 text=issue.message,
                 wraplength=600).pack(anchor=tk.W)

        # Context (if available)
        if issue.context:
            context_str = " | ".join([f"{k}: {v}" for k, v in issue.context.items()])
            ttk.Label(content_frame,
                     text=context_str,
                     font=("TkDefaultFont", 7),
                     foreground="gray").pack(anchor=tk.W)
