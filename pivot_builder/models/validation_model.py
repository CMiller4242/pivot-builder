"""Validation models for pivot builder."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ValidationIssue:
    """Represents a single validation issue."""

    level: str  # "error" | "warning" | "info"
    code: str
    message: str
    context: Optional[dict] = None

    def __post_init__(self):
        """Validate level."""
        valid_levels = ["error", "warning", "info"]
        if self.level not in valid_levels:
            raise ValueError(f"Level must be one of {valid_levels}")


@dataclass
class ValidationReport:
    """Collection of validation issues."""

    issues: List[ValidationIssue] = field(default_factory=list)

    def has_errors(self) -> bool:
        """Check if report contains any errors."""
        return any(issue.level == "error" for issue in self.issues)

    def errors(self) -> List[ValidationIssue]:
        """Get all error-level issues."""
        return [issue for issue in self.issues if issue.level == "error"]

    def warnings(self) -> List[ValidationIssue]:
        """Get all warning-level issues."""
        return [issue for issue in self.issues if issue.level == "warning"]

    def infos(self) -> List[ValidationIssue]:
        """Get all info-level issues."""
        return [issue for issue in self.issues if issue.level == "info"]

    def add(self, level: str, code: str, message: str, context: Optional[dict] = None):
        """Add an issue to the report."""
        self.issues.append(ValidationIssue(level, code, message, context))

    def clear(self):
        """Clear all issues."""
        self.issues.clear()
