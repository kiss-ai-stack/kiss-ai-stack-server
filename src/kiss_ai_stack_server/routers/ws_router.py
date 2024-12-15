from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.websockets import WebSocketState
from kiss_ai_stack.core.utilities.logger import LOG
from kiss_ai_stack_types.enums import ServerEvent
from kiss_ai_stack_types.models import QueryRequestBody, DocumentsRequestBody

from kiss_ai_stack_server.services.session_service import SessionService
from kiss_ai_stack_server.services.token_service import TokenService
from kiss_ai_stack_server.utilities.server_event_utils import handle_server_event

ws_router = APIRouter()


@ws_router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint with JWT authentication and session retrieval.

    :param websocket: (WebSocket) The active WebSocket connection
    """
    try:
        authorization = websocket.headers.get('Authorization')
        if not authorization or not authorization.startswith('Bearer '):
            await websocket.close(code=4001, reason='Missing or invalid Authorization header')
            return

        access_token = authorization[7:]
        try:
            payload = TokenService.decode_token(access_token)
        except Exception:
            await websocket.close(code=4001, reason="Invalid token")
            return
        session = await SessionService.get_active_session_by_client_id(
            client_id=payload['sub']
        )
        if not session:
            await websocket.close(code=4001, reason="Invalid or inactive session")
            return

    except Exception:
        await websocket.close(code=4001, reason="Authentication failed")
        return

    await websocket.accept()

    try:
        while websocket.client_state != WebSocketState.DISCONNECTED:
            try:
                data = await websocket.receive_json()
                event_str = data.get('event')

                try:
                    event = ServerEvent(event_str)
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail=f'Invalid event: {event_str}'
                    )
                match event:
                    case ServerEvent.ON_STORE:
                        request_data = DocumentsRequestBody(**data.get('data', {}))
                    case _:
                        request_data = QueryRequestBody(**data.get('data', {}))

                response = await handle_server_event(
                    event,
                    request_data,
                    session=session
                )
                await websocket.send_json({
                    'event': event_str,
                    'result': response.model_dump()
                })

            except HTTPException as http_exc:
                await websocket.send_json({
                    'error': True,
                    'status_code': http_exc.status_code,
                    'detail': http_exc.detail
                })
            except ValueError as ve:
                LOG.warning(f'Invalid data received: {ve}')
                await websocket.send_json({
                    'error': True,
                    'status_code': 400,
                    'detail': 'Invalid data'
                })

    except WebSocketDisconnect:
        LOG.warning('WebSocket disconnected')
    except Exception as e:
        LOG.error(f'Unexpected WebSocket error: {e}')
    finally:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()
        LOG.info('WebSocket connection closed')
