from uuid import UUID

from sqlalchemy import insert, select

from app.core.database import transaction
from app.models.user import User


class UserRepository:
    @staticmethod
    async def get_by_id(user_id: UUID) -> dict | None:
        """Récupère un utilisateur par son UUID."""
        async with transaction() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            return result.mappings().first()

    @staticmethod
    async def create(username: str, email: str) -> dict:
        """Crée un utilisateur et retourne les données insérées."""
        async with transaction() as session:
            query = insert(User).values(username=username, email=email).returning(User)
            result = await session.execute(query)
            return result.mappings().first()

    @staticmethod
    async def list_users(limit: int = 10) -> list[dict]:
        """Liste les utilisateurs avec une limite."""
        async with transaction() as session:
            query = select(User).limit(limit)
            result = await session.execute(query)
            return list(result.scalars().all())
