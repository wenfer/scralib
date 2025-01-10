import json

from sanic import response, Request
from models.models import Settings


async def settings_list(request: Request):
    settings = await Settings.all()
    if len(settings) > 0:
        return response.json(dict(map(lambda obj: (obj.name, obj.value), settings)))
    return response.json({})


async def save_settings(request: Request):
    data = request.json
    for key, value in data.items():
        setting = await Settings.get_or_none(name=key)
        if setting is None:
            setting = Settings(name=key, value=value)
            await setting.save()
        else:
            setting.value = value
            await setting.save()

    return response.json(data)
