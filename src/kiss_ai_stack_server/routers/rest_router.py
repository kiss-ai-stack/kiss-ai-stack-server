from fastapi import APIRouter, HTTPException
from kiss_ai_stack_types.enums import ServerEvent
from kiss_ai_stack_types.models import SessionRequest, SessionResponse, QueryRequestBody, DocumentsRequestBody
from starlette.requests import Request

from kiss_ai_stack_server.utilities.server_event_utils import handle_server_event

rest_router = APIRouter()


@rest_router.post('/auth')
async def exec_auth(data: SessionRequest) -> SessionResponse:
    return await handle_server_event(ServerEvent.ON_AUTH, data)


@rest_router.post('/sessions')
async def exec_session_action(action: str, data: QueryRequestBody, request: Request):
    """
    Perform an action on the session based on the query parameter 'action'.

    Supported actions:
    - close: Close the session
    - init: Initialize the session
    """
    event_map = {
        'close': ServerEvent.ON_CLOSE,
        'init': ServerEvent.ON_INIT
    }

    if action not in event_map:
        raise HTTPException(status_code=400, detail=f'Invalid action: {action}')

    session = getattr(request.state, 'session', None)
    return await handle_server_event(event_map[action], data, session)


@rest_router.post('/queries')
async def exec_query(data: QueryRequestBody, request: Request):
    session = getattr(request.state, 'session', None)
    return await handle_server_event(ServerEvent.ON_QUERY, data, session)


@rest_router.post('/documents')
async def exec_store(data: DocumentsRequestBody, request: Request):
    session = getattr(request.state, 'session', None)
    return await handle_server_event(ServerEvent.ON_STORE, data, session)
