import uvicorn

from app.configs.settings import ProjectSettings

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host=ProjectSettings.host,
        port=int(ProjectSettings.port),
        reload=True,
    )
