## discord_data

Library to parse information from the discord data export, see more info [here](https://support.discord.com/hc/en-us/articles/360004027692).

The request to process the data has to be done manually, and it can take a while for them to deliver it to you.

This takes the `messages` and `activity` directories as arguments, like:

```python
>>> from pathlib import Path
>>> from discord_data import parse_messages, parse_activity
>>> next(parse_messages(Path('./discord/october_2020/messages')))
>>> next(parse_activity(Path('./discord/october_2020/activity')))
```

``Message(mid='747951969171275807', dt=datetime.datetime(2020, 8, 25, 22, 54, 5, 726000, tzinfo=datetime.timezone.utc), channel=Channel(cid='464051583559139340', name='general', server_name='Dream World'), content='<:NotLikeThis:237729324885606403>', attachments='')``

`{'event_type': 'ack_messages', 'event_id': '3Bj0l1ZK52hxN2gx==', 'event_source': 'client', 'user_id': '52292364546181229242', 'ip': '....', 'day': '655', 'chosen_locale': 'en-US', 'detected_locale': 'en-US', 'browser': 'Discord Client', 'city': '...', 'country_code': 'US', 'region_code': 'CA', 'time_zone': 'America/Los_Angeles', 'guild_id': '40922123327445216540', 'guild_size_total': '374', 'guild_member_num_roles': '9', 'guild_member_perms': '2616662909', 'guild_num_channels': '25', 'guild_num_text_channels': '19', 'guild_num_voice_channels': '6', 'guild_num_roles': '200', 'guild_is_vip': False, 'channel_id': '82785028073258646612', 'channel_type': '0', 'channel_size_total': '0', 'channel_member_perms': '104193088', 'channel_hidden': True, 'client_send_timestamp': '"2018-05-02T00:47:33.534Z"', 'client_track_timestamp': '"2018-05-02T00:47:33.459Z"', 'timestamp': '"2018-05-02T00:47:33.667Z"'}`

Created to be used as part of [HPI](https://github.com/seanbreckenridge/HPI)

### TODO:

Once I actually have multiple data exports (so wont be able to update this for at least a month), write `merge.py` to merge multiple data exports into one.

The export looks quite complete; If all the data is returned, we can keep the latest discord export, instead of trying to merge multiple exports from the past.

#### Requires:

`python3.6+`

To install with pip, run:

    pip install 'git+https://github.com/seanbreckenridge/discord_data'
