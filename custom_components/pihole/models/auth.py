from pydantic import BaseModel
from typing import Optional


class PiHoleSession(BaseModel):
    valid: bool
    totp: bool
    sid: Optional[str]
    csrf: Optional[str]
    validity: int
    message: Optional[str]


class PiHoleAuth(BaseModel):
    session: PiHoleSession
    took: int