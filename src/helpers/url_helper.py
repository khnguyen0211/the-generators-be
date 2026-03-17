"""URL helper for building full URLs based on environment."""


class UrlHelper:
    """Helper for building environment-aware URLs."""

    @staticmethod
    def build_output_url(path: str, config) -> str:
        """Build full URL for output files.
        
        Args:
            path: Relative path like /output/images/abc.png
            config: ConfigService instance
            
        Returns:
            Full URL like http://localhost:5000/output/images/abc.png
        """
        base_url = config.get("API_BASE_URL", "").rstrip("/")
        
        if not base_url:
            # Fallback for dev
            port = config.flask_port
            base_url = f"http://localhost:{port}"
        
        return f"{base_url}{path}"
