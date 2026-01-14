from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, field_serializer


def datetime_to_gmt_str(dt: datetime) -> str:
    # Force le passage en UTC si aucune info de timezone n'est présente
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class CustomModel(BaseModel):
    """Modèle de base pour tous les schémas Pydantic du projet"""

    model_config = ConfigDict(
        # Encode automatiquement tous les datetime via la fonction ci-dessus
        populate_by_name=True,
        from_attributes=True,
    )

    @field_serializer("*")
    def serialize_dates(self, value: any):
        if isinstance(value, datetime):
            return datetime_to_gmt_str(value)
        return value
