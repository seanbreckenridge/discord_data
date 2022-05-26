import json
import csv
import logging

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Optional, Dict, List, Any, Union


from .model import Message, Channel, Json, Activity, RegionInfo, Fingerprint, Server
from .common import expand_path, PathIsh


def get_self_user_id(export_root_dir: PathIsh) -> str:
    user_info_f: Path = expand_path(export_root_dir) / "account" / "user.json"
    assert user_info_f.exists()
    user_json = json.loads(user_info_f.read_text())
    return str(user_json["id"])


# timezone aware
DT_FORMATS = [r"%Y-%m-%d %H:%M:%S.%f%z", r"%Y-%m-%d %H:%M:%S%z"]


def _parse_message_datetime(ds: str) -> datetime:
    for dfmt in DT_FORMATS:
        try:
            return datetime.strptime(ds, dfmt)
        except ValueError:
            pass
    # try as a fallback?
    return _parse_activity_datetime(ds)


def _parse_activity_datetime(ds: str) -> datetime:
    try:
        d = ds.strip('"').rstrip("Z")
        naive = datetime.fromisoformat(d)
        return naive.replace(tzinfo=timezone.utc)
    except ValueError as v:
        print(f"Could not parse datetime with any of the known formats: {ds}")
        raise v


def parse_messages(messages_dir: PathIsh) -> Iterator[Message]:
    pmsg_dir: Path = expand_path(messages_dir)
    # get user id
    # my_user: str = _get_self_user_id(pmsg_dir.parent)

    # parse index
    index_f = pmsg_dir / "index.json"
    assert index_f.exists(), f"Message index 'index.json' doesnt exist at {index_f}"
    index: Dict[str, Optional[str]] = json.loads(index_f.read_text())

    # get individual message directories
    msg_dirs: List[Path] = list(
        filter(lambda d: d.is_dir() and not d.name.startswith("."), pmsg_dir.iterdir())
    )
    for msg_chan in msg_dirs:

        # chanel.json has some metadata about the channel/server
        channel_info_f: Path = msg_chan / "channel.json"
        channel_json: Dict[str, Any] = json.loads(channel_info_f.read_text())

        # optionally, find server information
        server_info: Optional[Server] = None

        # if the channel.json included guild (server) info
        if "guild" in channel_json:
            server_info = Server(
                server_id=int(channel_json["guild"]["id"]),
                name=channel_json["guild"]["name"],
            )

        channel_name: Optional[str] = index.get(channel_json["id"])

        channel_obj: Channel = Channel(
            channel_id=int(channel_json["id"]),
            name=channel_name,
            server=server_info,
        )

        # read CSV file to get messages
        with (msg_chan / "messages.csv").open("r", encoding="utf-8", newline="") as f:
            csv_reader = csv.reader(
                f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            next(csv_reader)  # ignore header row
            for row in csv_reader:
                yield Message(
                    message_id=int(row[0]),
                    timestamp=_parse_message_datetime(row[1]),
                    channel=channel_obj,
                    content=row[2],
                    attachments=row[3],
                )


def _parse_activity_blob(blob: Json) -> Activity:
    reginfo = None
    try:
        reginfo = RegionInfo(
            city=blob["city"],
            country_code=blob["country_code"],
            region_code=blob["region_code"],
            time_zone=blob["time_zone"],
        )
    except KeyError:
        pass
    json_data: Dict[str, Union[str, None]] = {}
    event_type = blob["event_type"]
    if event_type == "launch_game":
        json_data["game"] = blob.get("game")
    elif event_type == "add_reaction":
        json_data["message_id"] = blob.get("message_id")
        json_data["emoji_name"] = blob.get("emoji_name")
    elif event_type == "game_opened":
        json_data["game"] = blob.get("game")
    elif event_type == "application_opened":
        json_data["application"] = blob.get("application_name")
    json_clean: Dict[str, str] = {k: v for k, v in json_data.items() if v is not None}
    return Activity(
        event_id=blob["event_id"],
        event_type=event_type,
        region_info=reginfo,
        fingerprint=Fingerprint.make(blob),
        timestamp=_parse_activity_datetime(blob["timestamp"]),
        json_data_str=json.dumps(json_clean) if json_clean else None,
    )


def parse_activity(
    events_dir: PathIsh, logger: Optional[logging.Logger] = None
) -> Iterator[Activity]:
    """
    Return useful fields from the JSON blobs
    """
    yield from map(_parse_activity_blob, parse_raw_activity(events_dir, logger))


def parse_raw_activity(
    events_dir: PathIsh, logger: Optional[logging.Logger] = None
) -> Iterator[Json]:
    """
    Return all the objects from the activity directory, as
    JSON blobs
    """
    for activity_f in expand_path(events_dir).rglob("*.json"):
        if logger is not None:
            logger.debug(f"Parsing {activity_f}...")
        # not a 'json file', this has json objects, one per line
        for line in activity_f.open("r"):
            yield json.loads(line)
