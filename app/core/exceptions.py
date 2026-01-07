from typing import Any, Optional
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .config import settings


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


async def detailed_http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # 1. Déterminer le code statut
    status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # 2. Déterminer le nom de l'erreur (pour le champ 'error')
    if isinstance(exc, DetailedHTTPException):
        error_name = exc.__class__.__name__
        message = exc.detail
    elif isinstance(exc, RequestValidationError):
        error_name = "ValidationError"
        status_code = 422
        if settings.ENVIRONMENT.is_deployed:
            # En PROD : message générique sécurisé
            message = "Invalid input data"
        else:
            # En DEV/LOCAL : on renvoie le détail technique de Pydantic
            message = exc.errors()
    else:
        # Pour StarletteHTTPException (404/405)
        error_name = "APIError"
        message = getattr(exc, "detail", str(exc))

    return JSONResponse(
        status_code=status_code,
        content={
            "error": error_name,
            "message": message,
            "path": request.url.path,
            "request_id": getattr(request.state, "request_id", "n/a")
        },
        headers=getattr(exc, "headers", None),
    )