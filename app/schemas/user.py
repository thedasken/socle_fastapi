from datetime import datetime

from pydantic import UUID4, EmailStr, Field

from app.core.schemas import CustomModel


class UserRead(CustomModel):
    id: UUID4
    username: str = Field(..., min_length=1, max_length=128)
    email: EmailStr
    created_at: datetime
