class CTFDError(Exception):
    """Exception class to handle exceptions thrown for any request regarding CTFd API"""

class HTTPError(CTFDError):
    """Exception class to handle exceptions thrown for any HTTP request"""

    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message)
        self.status_code = status_code

    def __str__(self) -> str:
        return f"HTTP error raised with status code {self.status_code}:\n{super().__str__()}"