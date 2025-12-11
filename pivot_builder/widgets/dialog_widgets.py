"""Common dialog widgets."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class DialogWidgets:
    """Collection of common dialog utilities."""

    @staticmethod
    def show_error(title, message):
        """Show error dialog."""
        messagebox.showerror(title, message)

    @staticmethod
    def show_info(title, message):
        """Show info dialog."""
        messagebox.showinfo(title, message)

    @staticmethod
    def show_warning(title, message):
        """Show warning dialog."""
        messagebox.showwarning(title, message)

    @staticmethod
    def ask_yes_no(title, message):
        """Show yes/no dialog."""
        return messagebox.askyesno(title, message)

    @staticmethod
    def open_file_dialog(file_types):
        """Show file open dialog."""
        return filedialog.askopenfilename(filetypes=file_types)

    @staticmethod
    def save_file_dialog(file_types):
        """Show file save dialog."""
        return filedialog.asksaveasfilename(filetypes=file_types)
