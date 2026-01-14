import logging

from fastapi import APIRouter
from pydantic import BaseModel

from app.api.repositories.user import UserRepository
from app.core.exceptions import NotFound
from app.schemas.user import UserRead

router = APIRouter()
logger = logging.getLogger(__name__)


class UserInput(BaseModel):
    name: str
    age: int


@router.post("/examples/validation-error")
async def test_validation(user: UserInput):
    """Teste la capture des erreurs Pydantic (RequestValidationError)"""
    logger.info("Déclenchement d'une erreur Pydantic surchargée")
    return {"message": f"Hello {user.name}"}


@router.get("/examples/not-found")
async def test_not_found():
    """Teste l'exception NotFound standard"""
    logger.info("Déclenchement d'une 404 par défaut")
    raise NotFound()


@router.get("/examples/custom-error")
async def test_custom_error():
    """Teste une exception avec un message surchargé"""
    logger.info("Déclenchement d'une 404 customisée")
    raise NotFound(detail="Cet item spécifique n'existe pas dans la base de données")


@router.get("/db-test", response_model=list[UserRead])
async def test_db_repository():
    """Teste le repository avec le pattern de transaction."""
    users = await UserRepository.list_users(limit=5)
    return users
