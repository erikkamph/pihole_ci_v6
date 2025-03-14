from pydantic import BaseModel, Field
from typing import Optional


class Local(BaseModel):
    branch: Optional[str] = Field(default=None)
    version: Optional[str] = Field(default=None)
    hash: Optional[str] = Field(default=None)


class Remote(BaseModel):
    version: Optional[str] = Field(default=None)
    hash: Optional[str] = Field(default=None)


class Docker(BaseModel):
    local: Optional[str] = Field(default=None)
    remote: Optional[str] = Field(default=None)


class BaseVersionInfo(BaseModel):
    local: Optional[Local] = Field(default=None)
    remote: Optional[Remote] = Field(default=None)


class Version(BaseModel):
    core: Optional[BaseVersionInfo] = Field(default=None)
    web: Optional[BaseVersionInfo] = Field(default=None)
    ftl: Optional[BaseVersionInfo] = Field(default=None)


class PiHoleVersionInfo(BaseModel):
    version: Optional[Version] = Field(default=None)
    docker: Optional[Docker] = Field(default=None)
    took: float