from fastapi import APIRouter
from finanz_analyse.ui.depot import sunburst
from finanz_analyse import cache
from fastapi.responses import HTMLResponse

def get_router() -> APIRouter:
    api = APIRouter(prefix="/api")

    @api.get("/hello")
    async def root():
        return {"message": "Hello World"}

    @api.get("/all_depots")
    async def depot() -> HTMLResponse:
        return HTMLResponse(content=sunburst('tr'), status_code=200)

    @api.get("/depot/{name}")
    async def depot(name: str) -> HTMLResponse:
        return HTMLResponse(content=sunburst(name), status_code=200)

    @api.get("/depots")
    async def depots() -> list[str]:
        return list(cache.DEPOTS.keys())


    return api
