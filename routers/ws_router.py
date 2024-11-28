import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from events import event_handlers

ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            event = data.get("event")
            payload = data.get("data")
            if event in event_handlers:
                result = await event_handlers[event](payload)
                await websocket.send_json({"event": event, "result": result})
            else:
                await websocket.send_json({"error": f"Unknown event '{event}'"})
    except WebSocketDisconnect:
        logging.warning("WebSocket disconnected")
