from events.event_handlers import on_store


@on_store
async def handle_store(data):
    return {"status": "store completed"}