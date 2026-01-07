from enum import Enum


class Environment(str, Enum):
    LOCAL = "LOCAL"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)