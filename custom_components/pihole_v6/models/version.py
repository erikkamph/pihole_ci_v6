from pydantic import BaseModel
from typing import Optional


class Local(BaseModel):
    branch: Optional[str]
    version: Optional[str]
    hash: Optional[str]


class Remote(BaseModel):
    version: Optional[str]
    hash: Optional[str]


class Docker(BaseModel):
    local: Optional[str]
    remote: Optional[str]


class BaseVersionInfo(BaseModel):
    local: Local
    remote: Remote


class Version(BaseModel):
    core: BaseVersionInfo
    web: BaseVersionInfo
    ftl: BaseVersionInfo


class PiHoleVersionInfo(BaseModel):
    version: Version
    docker: Docker
    took: int