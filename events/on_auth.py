from events.event_handlers import on_auth


@on_auth
async def handle_auth(data):
    return {"status": "auth completed"}