from fastapi import APIRouter, HTTPException

from models.documents import DocumentsRequestBody
from models.enums.events import ServerEvent
from models.queries import QueryRequestBody
from utilities.server_event_utils import handle_server_event

rest_router = APIRouter()


@rest_router.post('/auth')
async def exec_auth(data: dict):
    return await handle_server_event(ServerEvent.ON_AUTH, data)


@rest_router.post('/sessions')
async def exec_session_action(action: str, data: dict):
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

    return await handle_server_event(event_map[action], data)


@rest_router.post('/queries')
async def exec_query(data: QueryRequestBody):
    return await handle_server_event(ServerEvent.ON_QUERY, data)


@rest_router.post('/documents')
async def exec_store(data: DocumentsRequestBody):
    return await handle_server_event(ServerEvent.ON_STORE, data)
