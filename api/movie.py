from sanic import text


def map_router(app):
    @app.get("/")
    async def hello_world(request):
        return text("Hello, world.")
