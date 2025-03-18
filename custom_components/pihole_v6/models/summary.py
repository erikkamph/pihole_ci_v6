from pydantic import BaseModel, Field
from typing import Any, Optional
from .version import PiHoleVersionInfo

class Queries(BaseModel):
    total: Optional[int] = Field(default=None)
    blocked: Optional[int] = Field(default=None)
    percent_blocked: Optional[float] = Field(default=None)


class Cache(BaseModel):
    size: Optional[int] = Field(default=None)
    inserted: Optional[int] = Field(default=None)
    evicted: Optional[int] = Field(default=None)


class Transmission(BaseModel):
    value: Optional[float] = Field(default=None)
    unit: Optional[str] = Field(default=None)


class IP(BaseModel):
    addr: Optional[str] = Field(default=None)
    rx_bytes: Optional[Transmission] = Field(default=None)
    tx_bytes: Optional[Transmission] = Field(default=None)
    num_addrs: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    gw_addr: Optional[str] = Field(default=None)


class IFace(BaseModel):
    v4: Optional[IP] = Field(default=None)
    v6: Optional[IP] = Field(default=None)


class Config(BaseModel):
    dhcp_active: Optional[bool] = Field(default=None)
    dhcp_start: Optional[str] = Field(default=None)
    dhcp_end: Optional[str] = Field(default=None)
    dhcp_ipv6: Optional[bool] = Field(default=None)
    dns_domain: Optional[str] = Field(default=None)
    dns_port: Optional[int] = Field(default=None)
    dns_num_upstreams: Optional[int] = Field(default=None)
    dns_dnssec: Optional[bool] = Field(default=None)
    dns_revServer_active: Optional[bool] = Field(default=None)


class Sensors(BaseModel):
    cpu_temp: Optional[int] = Field(default=None)
    hot_limit: Optional[int] = Field(default=None)
    unit: Optional[str] = Field(default=None)


class Ram(BaseModel):
    total: Optional[int] = Field(default=None)
    free: Optional[int] = Field(default=None)
    used: Optional[int] = Field(default=None)
    available: Optional[int] = Field(default=None)
    percentage_used: Optional[float] = Field(default=None, alias="%%used")


class Memory(BaseModel):
    ram: Optional[Ram] = Field(default=None)
    swap: Optional[Ram] = Field(default=None)


class Load(BaseModel):
    raw: Optional[list[float]] = Field(default=None)
    percent: Optional[list[float]] = Field(default=None)


class SysCPU(BaseModel):
    nprocs: Optional[int] = Field(default=None)
    load: Optional[Load] = Field(default=None)


class System(BaseModel):
    uptime: Optional[int] = Field(default=None)
    memory: Optional[Memory] = Field(default=None)
    procs: Optional[int] = Field(default=None)
    cpu: Optional[SysCPU] = Field(default=None)


class PiHoleSummary(BaseModel):
    recent_blocked: Optional[str] = Field(default=None)
    top_domain: Optional[str] = Field(default=None)
    top_blocked: Optional[str] = Field(default=None)
    top_client: Optional[str] = Field(default=None)
    active_clients: Optional[int] = Field(default=None)
    gravity_size: Optional[int] = Field(default=None)
    blocking: Optional[str] = Field(default=None)
    queries: Optional[Queries] = Field(default=None)
    cache: Optional[Cache] = Field(default=None)
    iface: Optional[IFace] = Field(default=None)
    node_name: Optional[str] = Field(default=None)
    host_model: Optional[str] = Field(default=None)
    config: Optional[Config] = Field(default=None)
    cpu_usage: Optional[float] = Field(default=None, alias="%%cpu")
    mem_usage: Optional[float] = Field(default=None, alias="%%mem")
    pid: Optional[int] = Field(default=None)
    sensors: Optional[Sensors] = Field(default=None)
    system: Optional[System] = Field(default=None)
    version: Optional[PiHoleVersionInfo] = Field(default=None)
    took: float