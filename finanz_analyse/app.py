import uvicorn

def main() -> None:
    config = uvicorn.Config("finanz_analyse.main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()