from events.event_handlers import on_query


@on_query
async def handle_init(data):
    return {"status": "query completed"}