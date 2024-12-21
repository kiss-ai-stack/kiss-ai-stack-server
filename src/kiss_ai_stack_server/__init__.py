from typing import Optional

import uvicorn
from fastapi import FastAPI

from kiss_ai_stack_server.routers.rest_router import rest_router
from kiss_ai_stack_server.routers.ws_router import ws_router
from kiss_ai_stack_server.services.session_service import SessionService
from kiss_ai_stack_server.utilities.session_auth_middleware import SessionAuthMiddleware


async def bootstrap_session_schema():
    """
    Initialize database connection and build schemas before starting the application
    """
    await SessionService.connect()
    await SessionService.build_schema()


def get_stack_server_app():
    app = FastAPI(
        title='KISS AI Stack Server',
        description='Enterprise-grade server for the KISS AI Stack',
        version='0.1.0-alpha'
    )

    # Add middleware for session authentication
    app.add_middleware(SessionAuthMiddleware)

    app.include_router(rest_router)
    app.include_router(ws_router)

    return app


def stacks_server(config: Optional[uvicorn.Config] = None) -> uvicorn.Server:
    """
    Prepare the Uvicorn server instance for execution

    :param config: uvicorn Server configurations.
    :returns: uvicorn.Server object.
    """
    # Default configuration for Uvicorn server if not provided
    if config is None:
        config = uvicorn.Config(
            app=get_stack_server_app(),
            host='0.0.0.0',
            port=8080,
            reload=True,
            log_level='info'
        )

    return uvicorn.Server(config)
