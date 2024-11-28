from events import on_close


@on_close
async def handle_close(data):
    return {"status": "close completed"}