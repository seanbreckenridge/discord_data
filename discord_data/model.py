from datetime import datetime
from typing import NamedTuple, Optional, Dict, Any


class Channel(NamedTuple):
    cid: str
    name: Optional[str]
    server_name: Optional[str]  # if this is a guild (server), the server name


class Message(NamedTuple):
    mid: str
    dt: datetime
    channel: Channel
    content: str
    attachments: str


Json = Dict[str, Any]
