from enum import Enum

# Convention explicite pour éviter les noms de contraintes aléatoires par défaut
DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Environment(str, Enum):
    LOCAL = "LOCAL"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self) -> bool:
        return self in (self.LOCAL)

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)
