from robyn import SubRouter, Request

from api.__rest import success
from config import GlobalConfig

index_router = SubRouter(__file__, prefix="")


@index_router.get("/config")
async def get_config(request):
    return success(GlobalConfig.get_all())


@index_router.put("/config")
async def set_config(request:Request):
    json = request.json()
    return success(GlobalConfig.update_all(json))


@index_router.get("/status")
async def get_status(request):
    return success({
        "status": "ok"
    })