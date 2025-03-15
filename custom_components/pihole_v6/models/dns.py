from pydantic import BaseModel, PlainSerializer, Field
from enum import Enum
from typing_extensions import Annotated
from typing import Optional


class BlockingEnum(str, Enum):
    enabled='enabled'
    disabled='disabled'
    failed='failed'
    unknown='unknown'


class PiHoleDnsBlocking(BaseModel):
    blocking: BlockingEnum
    timer: Optional[float] = Field(default=None)
    took: float

    @property
    def is_blocking(self):
        match self.blocking:
            case BlockingEnum.disabled:
                return False
            case BlockingEnum.enabled:
                return True
            case BlockingEnum.failed:
                return True
            case BlockingEnum.unknown:
                return False
            case _:
                return False