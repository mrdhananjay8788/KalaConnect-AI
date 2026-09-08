from pydantic import BaseModel, ConfigDict
from typing import Optional, Any

class APIResponseBase(BaseModel):
    success: bool
    
class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[dict[str, Any]] = None

class APIErrorResponse(APIResponseBase):
    success: bool = False
    error: ErrorDetail

class APISuccessResponse(APIResponseBase):
    success: bool = True
    data: Any

