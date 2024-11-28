from events.event_handlers import on_init

@on_init
async def handle_init(data):
    return {"status": "init completed"}