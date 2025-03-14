from pydantic import BaseModel, Field
from typing import Optional


class PiHoleSession(BaseModel):
    valid: bool = Field(default=False)
    totp: bool = Field(default=False)
    sid: Optional[str] = Field(default=None)
    csrf: Optional[str] = Field(default=None)
    validity: int = Field(default=0)
    message: Optional[str] = Field(default=None)


class PiHoleAuth(BaseModel):
    session: PiHoleSession
    took: float = Field(default=0)