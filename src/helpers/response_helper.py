"""Response helper for Flask endpoints."""

from flask import jsonify
from common.api_response import ApiResponse


class ResponseHelper:
    """Helper class for creating Flask responses."""

    @staticmethod
    def success(data: dict = None, message: str = "Success", status_code: int = 200):
        """Return success response tuple for Flask."""
        response = ApiResponse.success(data=data, message=message, status_code=status_code)
        return jsonify(response.to_dict()), status_code

    @staticmethod
    def error(message: str = "Error", errors: list = None, status_code: int = 400):
        """Return error response tuple for Flask."""
        response = ApiResponse.error(message=message, errors=errors, status_code=status_code)
        return jsonify(response.to_dict()), status_code
