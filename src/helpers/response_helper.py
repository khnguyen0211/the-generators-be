"""Response helper for Flask endpoints."""

from common.api_response import ApiResponse


class ResponseHelper:
    """Helper class for creating Flask responses."""

    @staticmethod
    def success(data: dict = None, message: str = "Success", status_code: int = 200):
        """Return success response dict with status code for flask-restx."""
        response = ApiResponse.success(data=data, message=message, status_code=status_code)
        return response.to_dict(), status_code

    @staticmethod
    def error(message: str = "Error", errors: list = None, status_code: int = 400):
        """Return error response dict with status code for flask-restx."""
        response = ApiResponse.error(message=message, errors=errors, status_code=status_code)
        return response.to_dict(), status_code
