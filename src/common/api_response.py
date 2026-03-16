"""ApiResponse model class for consistent API responses."""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ApiResponse:
    """Standard API response model."""

    status_code: int = 200
    message: str = "Success"
    errors: Optional[list] = None
    data: Optional[dict] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "status_code": self.status_code,
            "message": self.message,
            "errors": self.errors,
            "data": self.data,
        }

    @classmethod
    def success(cls, data: Any = None, message: str = "Success", status_code: int = 200):
        """Create success response."""
        return cls(
            status_code=status_code,
            message=message,
            errors=None,
            data=data,
        )

    @classmethod
    def error(cls, message: str = "Error", errors: list = None, status_code: int = 400):
        """Create error response."""
        return cls(
            status_code=status_code,
            message=message,
            errors=errors if errors is not None else [],
            data=None,
        )
