from fastapi import APIRouter
from finanz_analyse.ui.depot import sunburst
from fastapi.responses import HTMLResponse

def get_router() -> APIRouter:
    api = APIRouter(prefix="/api")

    @api.get("/hello")
    async def root():
        return {"message": "Hello World"}

    @api.get("/depot/{name}")
    async def depot(name: str) -> HTMLResponse:
        return HTMLResponse(content=sunburst(name), status_code=200)


    return api
