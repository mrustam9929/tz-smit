import uvicorn

from tz_smit.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "tz_smit.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
