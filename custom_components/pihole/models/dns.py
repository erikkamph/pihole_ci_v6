from pydantic import BaseModel, PlainSerializer
from enum import Enum
from typing_extensions import Annotated
from typing import Optional


class BlockingEnum(Enum, str):
    enabled='enabled'
    disabled='disabled'
    failed='failed'
    unknown='unknown'


def is_blocking(blocking: BlockingEnum):
    match blocking:
        case BlockingEnum.enabled:
            return True
        case BlockingEnum.disabled:
            return False
        case BlockingEnum.failed:
            return False
        case BlockingEnum.unknown:
            return False

BlockingAnnotated = Annotated[BlockingEnum, PlainSerializer(lambda _item: is_blocking(_item), return_type=bool)]


class PiHoleDnsBlocking(BaseModel):
    blocking: BlockingAnnotated
    timer: Optional[int]
    took: int