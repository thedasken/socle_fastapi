from pydantic import EmailStr, Field, UUID4
from datetime import datetime
from ..core.schemas import CustomModel

class UserRead(CustomModel):
    id: UUID4
    username: str = Field(..., min_length=1, max_length=128)
    email: EmailStr
    created_at: datetime