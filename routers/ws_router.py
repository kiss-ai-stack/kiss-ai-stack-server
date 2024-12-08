import logging
from typing import Dict, Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.websockets import WebSocketState

from models.enums.events import ServerEvent
from utilities.server_event_utils import handle_server_event

ws_router = APIRouter()


async def handle_websocket_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a WebSocket event with consistent error handling with SeverEvent.

    Args:
        payload (Dict[str, Any]): The event payload containing 'event' and 'data'

    Returns:
        Dict[str, Any]: Processing result

    Raises:
        HTTPException: If no handler is found for the event or processing fails
    """
    event = payload.get('event')
    data = payload.get('data', {})

    if not event:
        raise HTTPException(
            status_code=400,
            detail='Missing event type'
        )

    try:
        return await handle_server_event(ServerEvent(event), data)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid event type: {event}'
        )


@ws_router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while websocket.client_state != WebSocketState.DISCONNECTED:
            try:
                data = await websocket.receive_json()

                try:
                    response = await handle_websocket_event(data)
                    await websocket.send_json({
                        'event': data.get('event'),
                        'result': response
                    })
                except HTTPException as http_exc:
                    await websocket.send_json({
                        'error': True,
                        'status_code': http_exc.status_code,
                        'detail': http_exc.detail
                    })

            except ValueError as ve:
                logging.warning(f'Invalid JSON received: {ve}')
                await websocket.send_json({
                    'error': True,
                    'status_code': 400,
                    'detail': 'Invalid JSON'
                })

    except WebSocketDisconnect:
        logging.warning('WebSocket disconnected')
    except Exception as e:
        logging.error(f'Unexpected WebSocket error: {e}')
    finally:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()
        logging.info('WebSocket connection closed')
