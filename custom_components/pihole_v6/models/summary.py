from pydantic import BaseModel, Field
from datetime import datetime


class Gravity(BaseModel):
    domains_being_blocked: int
    last_update: datetime


class Clients(BaseModel):
    active: int
    total: int


class Replies(BaseModel):
    UNKNOWN: int
    NODATA: int
    NXDOMAIN: int
    CNAME: int
    IP: int
    DOMAIN: int
    RRNAME: int
    SERVFAIL: int
    REFUSED: int
    NOTIMP: int
    OTHER: int
    DNSSEC: int
    NONE: int
    BLOB: int


class Status(BaseModel):
    UNKNOWN: int
    GRAVITY: int
    FORWARDED: int
    CACHE: int
    REGEX: int
    DENYLIST: int
    EXTERNAL_BLOCKED_IP: int
    EXTERNAL_BLOCKED_NULL: int
    EXTERNAL_BLOCKED_NXRA: int
    GRAVITY_CNAME: int
    REGEX_CNAME: int
    DENYLIST_CNAME: int
    RETRIED: int
    RETRIED_DNSSEC: int
    IN_PROGRESS: int
    DBBUSY: int
    SPECIAL_DOMAIN: int
    CACHE_STALE: int
    EXTERNAL_BLOCKED_EDE15: int


class Types(BaseModel):
    A: int
    AAAA: int
    ANY: int
    SRV: int
    SOA: int
    PTR: int
    TXT: int
    NAPTR: int
    MX: int
    DS: int
    RRSIG: int
    DNSKEY: int
    NS: int
    SVCB: int
    HTTPS: int
    OTHER: int


class Queries(BaseModel):
    total: int
    blocked: int
    percent_blocked: float
    unique_domains: int
    forwarded: int
    cached: int
    frequency: float
    types: Types
    status: Status
    replies: Replies


class PiHoleSummary(BaseModel):
    queries: Queries
    clients: Clients
    gravity: Gravity
    took: int