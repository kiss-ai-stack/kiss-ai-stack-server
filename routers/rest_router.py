from fastapi import APIRouter, HTTPException

from events import event_handlers

rest_router = APIRouter()

@rest_router.post('/auth')
async def exec_auth(data: dict):
    if 'on_auth' in event_handlers:
        result = await event_handlers['on_auth'](data)
        return result
    raise HTTPException(status_code=404, detail="on_init handler not found")


@rest_router.post('/sessions')
async def exec_session_action(action: str, data: dict):
    """
    Perform an action on the session based on the query parameter 'action'.

    Actions:
    - close: Close the session.
    - init: Initialize the session.
    """
    if action == 'close':
        pass
    elif action == 'init':
        pass
    else:
        raise HTTPException(status_code=400, detail=f"Invalid action: {action}")

    return {"status": "success", "action": action}

@rest_router.post('/queries')
async def exec_query(data: dict):
    pass

@rest_router.post('/documents')
async def exec_store(data: dict):
    pass
