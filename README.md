## discord_data

Library to parse information from the discord data export, see more info [here](https://support.discord.com/hc/en-us/articles/360004027692).

The request to process the data has to be done manually, and it can take a while for them to deliver it to you.

This takes the `messages` and `activity` directories as arguments, like:

```
from pathlib import Path
from discord_data import events, activity
print(messages(Path('./discord/october_2020/messages')))
print(activity(Path('./discord/october_2020/activity')))

```

# TODO:

Once I actually have multiple data exports (so wont be able to update this for at least a month), write `merge.py` to merge multiple data exports into one.

The export looks quite complete; If all the data is returned, we can keep the latest discord export, instead of trying to merge multiple exports from the past.

#### Requires:

`python3.6+`

To install with pip, run:

    pip install 'git+https://github.com/seanbreckenridge/discord_data'
