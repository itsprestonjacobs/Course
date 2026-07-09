import data

FILE = "settings.json"
_settings = data.load(FILE, {})


def get(guild_id, key, default=None):
    return _settings.get(str(guild_id), {}).get(key, default)


def set_value(guild_id, key, value):
    gid = str(guild_id)
    _settings.setdefault(gid, {})
    _settings[gid][key] = value
    data.save(FILE, _settings)
