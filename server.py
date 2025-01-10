import os.path
from urllib.request import Request
from tortoise.contrib.sanic import register_tortoise
from sanic import Sanic, response

import env_util
from api import scrape, settings
from models.models import Task

app = Sanic("MyHelloWorldApp")
app.update_config({
    'KEEP_ALIVE': False,
    'CORS_ORIGINS': ["*"],
})
register_tortoise(
    app, db_url=f"sqlite://{os.path.join(env_util.config_path, 'scrapelib.db')}", modules={"models": ["models.models"]},
    generate_schemas=False
)
app.static("/static", "./static")

app.add_route(settings.settings_list, "/settings", methods=["GET"])
app.add_route(settings.save_settings, "/settings", methods=["POST"])

# app.add_route(get_tasks, "/gettasks", methods=["GET"])
#

@app.before_server_stop
async def on_close(*_):
    print("111111")


scrape.map_router(app)


@app.get("/")
async def handler(request: Request):
    return {"title": "1111111"}


@app.route("/list")
async def list_all(request):
    tasks = await Task.all()
    return response.json({"tasks": [str(tasks) for user in tasks]})
