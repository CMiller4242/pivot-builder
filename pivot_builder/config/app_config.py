"""Application configuration constants."""


# Preview settings
DEFAULT_PREVIEW_ROWS = 200

# File settings
SUPPORTED_FILE_TYPES = [
    ("Excel files", "*.xlsx *.xls"),
    ("CSV files", "*.csv"),
    ("All files", "*.*")
]

# UI settings
WINDOW_TITLE = "Pivot Builder"
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800

# Export settings
DEFAULT_EXPORT_FORMAT = "xlsx"
EXPORT_FORMATS = ["xlsx", "csv"]

# Validation settings
MAX_FILE_SIZE_MB = 100
