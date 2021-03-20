from datetime import datetime
from typing import NamedTuple, Optional, Dict, Any


Json = Dict[str, Any]


class Channel(NamedTuple):
    channel_id: str
    name: Optional[str]
    server_name: Optional[str]  # if this is a guild (server), the server name


class Message(NamedTuple):
    message_id: str
    timestamp: datetime
    channel: Channel
    content: str
    attachments: str


class RegionInfo(NamedTuple):
    city: str
    country_code: str
    region_code: str
    time_zone: str


def _strip_quotes(o: Optional[str]) -> Optional[str]:
    if o:
        return o.strip('"')
    return o

class Fingerprint(NamedTuple):
    os: Optional[str]
    os_version: Optional[str]
    browser: Optional[str]
    ip: Optional[str]
    isp: Optional[str]
    device: Optional[str]
    distro: Optional[str]

    @classmethod
    def make(cls, blob: Json) -> "Fingerprint":
        return cls(**{f: _strip_quotes(blob.get(f)) for f in cls._fields})


class Activity(NamedTuple):
    event_id: str
    event_type: str
    region_info: Optional[RegionInfo]
    # additional data that doesn't conform to this spec
    fingerprint: Fingerprint
    timestamp: datetime
