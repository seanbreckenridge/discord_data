## discord_data

Library to parse information from the discord data export, see more info [here](https://support.discord.com/hc/en-us/articles/360004027692).

The request to process the data has to be done manually, and it can take a while for them to deliver it to you.

This takes the `messages` and `activity` directories as arguments, like:

```python
>>> from discord_data import parse_messages, parse_activity
>>> next(parse_messages("./discord/october_2020/messages"))
>>> next(parse_activity("./discord/october_2020/activity"))
```

`Message(mid='747951969171275807', dt=datetime.datetime(2020, 8, 25, 22, 54, 5, 726000, tzinfo=datetime.timezone.utc), channel=Channel(cid='464051583559139340', name='general', server_name='Dream World'), content='<:NotLikeThis:237729324885606403>', attachments='')`

`Activity(event_id='AQICfXBljgG+pYXCTRrwzy6MqgAAAAA=', event_type='start_listening', region_info=RegionInfo(city='cityNameHere', country_code='US', region_code='CA', time_zone='America/Los_Angeles'), fingerprint=Fingerprint(os='Mac OS X', os_version='16.1.0', browser='Discord Client', ip='216.58.195.78', isp=None, device=None, distro=None), timestamp=datetime.datetime(2016, 11, 26, 7, 8, 47))`

---

Each of these returns a `Generator`, so they only read from the (giant) JSON files as needed. If you want to process all the data, you can call `list` on it to consume the whole generator:

```python
from discord_data import parse_messages, parse_activity
msg = list(parse_messages("./discord/october_2020/messages"))
acts = list(parse_activity("./discord/october_2020/activity"))
```

The raw activity data includes lots of additional fields, this only includes items I thought would be useful. If you want to parse the JSON blobs yourself, you do so by using `from discord_data import parse_raw_activity`

Created to be used as part of [`HPI`](https://github.com/seanbreckenridge/HPI)

### TODO:

Once I actually have multiple data exports (so wont be able to update this for at least a month), write `merge.py` to merge multiple data exports into one.

The export looks quite complete; If all the data is returned, we can keep the latest discord export, instead of trying to merge multiple exports from the past.

#### Requires:

`python3.6+`

To install with pip, run:

    pip install 'git+https://github.com/seanbreckenridge/discord_data'
