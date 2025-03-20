from pydantic import BaseModel, Field
from typing import Any, Optional

class Replies(BaseModel):
    UNKNOWN: Optional[int] = Field(default=None)
    NODATA: Optional[int] = Field(default=None)
    NXDOMAIN: Optional[int] = Field(default=None)
    CNAME: Optional[int] = Field(default=None)
    IP: Optional[int] = Field(default=None)
    DOMAIN: Optional[int] = Field(default=None)
    RRNAME: Optional[int] = Field(default=None)
    SERVFAIL: Optional[int] = Field(default=None)
    REFUSED: Optional[int] = Field(default=None)
    NOTIMP: Optional[int] = Field(default=None)
    OTHER: Optional[int] = Field(default=None)
    DNSSEC: Optional[int] = Field(default=None)
    NONE: Optional[int] = Field(default=None)
    BLOB: Optional[int] = Field(default=None)


class Status(BaseModel):
    UNKNOWN: Optional[int] = Field(default=None)
    GRAVITY: Optional[int] = Field(default=None)
    FORWARDED: Optional[int] = Field(default=None)
    CACHE: Optional[int] = Field(default=None)
    REGEX: Optional[int] = Field(default=None)
    DENYLIST: Optional[int] = Field(default=None)
    EXTERNAL_BLOCKED_IP: Optional[int] = Field(default=None)
    EXTERNAL_BLOCKED_NULL: Optional[int] = Field(default=None)
    EXTERNAL_BLOCKED_NXRA: Optional[int] = Field(default=None)
    GRAVITY_CNAME: Optional[int] = Field(default=None)
    REGEX_CNAME: Optional[int] = Field(default=None)
    DENYLIST_CNAME: Optional[int] = Field(default=None)
    RETRIED: Optional[int] = Field(default=None)
    RETRIED_DNSSEC: Optional[int] = Field(default=None)
    IN_PROGRESS: Optional[int] = Field(default=None)
    DBBUSY: Optional[int] = Field(default=None)
    SPECIAL_DOMAIN: Optional[int] = Field(default=None)
    CACHE_STALE: Optional[int] = Field(default=None)
    EXTERNAL_BLOCKED_EDE15: Optional[int] = Field(default=None)


class Types(BaseModel):
    A: Optional[int] = Field(default=None)
    AAAA: Optional[int] = Field(default=None)
    ANY: Optional[int] = Field(default=None)
    SRV: Optional[int] = Field(default=None)
    SOA: Optional[int] = Field(default=None)
    PTR: Optional[int] = Field(default=None)
    TXT: Optional[int] = Field(default=None)
    NAPTR: Optional[int] = Field(default=None)
    MX: Optional[int] = Field(default=None)
    DS: Optional[int] = Field(default=None)
    RRSIG: Optional[int] = Field(default=None)
    DNSKEY: Optional[int] = Field(default=None)
    NS: Optional[int] = Field(default=None)
    SVCB: Optional[int] = Field(default=None)
    HTTPS: Optional[int] = Field(default=None)
    OTHER: Optional[int] = Field(default=None)


class Clients(BaseModel):
    active: Optional[int] = Field(default=None)
    total: Optional[int] = Field(default=None)


class Gravity(BaseModel):
    domains_being_blocked: Optional[int] = Field(default=None)
    last_update: Optional[int] = Field(default=None)


class Queries(BaseModel):
    total: Optional[int] = Field(default=None)
    blocked: Optional[int] = Field(default=None)
    percent_blocked: Optional[float] = Field(default=None)
    unique_domains: Optional[int] = Field(default=None)
    forwarded: Optional[int] = Field(default=None)
    cached: Optional[int] = Field(default=None)
    frequency: Optional[float] = Field(default=None)
    types: Optional[Types] = Field(default=None)
    status: Optional[Status] = Field(default=None)
    replies: Optional[Replies] = Field(default=None)


class PiHoleSummary(BaseModel):
    queries: Optional[Queries] = Field(default=None)
    clients: Optional[Clients] = Field(default=None)
    gravity: Optional[Gravity] = Field(default=None)
    took: Optional[float] = Field(default=None)