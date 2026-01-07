from typing import Any, Optional
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse


class DetailedHTTPException(HTTPException):
    STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL: str = "Internal Server Error"

    def __init__(self, detail: Optional[str] = None, headers: Optional[dict[str, Any]] = None) -> None:
        # Utilise le détail spécifique si fourni, sinon la constante de classe
        super().__init__(
            status_code=self.STATUS_CODE, 
            detail=detail or self.DETAIL, 
            headers=headers
        )


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Resource not found"


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "User not authenticated"

    def __init__(self, detail: Optional[str] = None) -> None:
        # RFC 6750: Le header WWW-Authenticate est requis pour la 401
        super().__init__(
            detail=detail, 
            headers={"WWW-Authenticate": "Bearer"}
        )


async def detailed_http_exception_handler(request: Request, exc: DetailedHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.detail,
            "path": request.url.path,
            "request_id": getattr(request.state, "request_id", None)
        },
        headers=exc.headers,
    )