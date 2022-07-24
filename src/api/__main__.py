import uvicorn

from .settings import settings

uvicorn.run(
    'api.app:app',
    port=settings.port,
    reload=settings.debug,
    debug=settings.debug,
)
