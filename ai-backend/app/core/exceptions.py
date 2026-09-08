from fastapi import HTTPException
from typing import Any, Dict, Optional

class APIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=message)
        self.error_code = error_code
        self.message = message
        self.details = details

class InvalidInputException(APIException):
    def __init__(self, message: str = "Invalid input provided", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=400, error_code="INVALID_INPUT", message=message, details=details)

class AIFailureException(APIException):
    def __init__(self, message: str = "AI service failed to process the request", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=502, error_code="AI_FAILURE", message=message, details=details)
