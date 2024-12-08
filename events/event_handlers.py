from typing import Callable, Dict

from models.enums.events import ServerEvent

event_handlers: Dict[str, Callable] = {}


def on_auth(func: Callable):
    event_handlers[ServerEvent.ON_AUTH] = func
    return func


def on_close(func: Callable):
    event_handlers[ServerEvent.ON_CLOSE] = func
    return func


def on_init(func: Callable):
    event_handlers[ServerEvent.ON_INIT] = func
    return func


def on_query(func: Callable):
    event_handlers[ServerEvent.ON_QUERY] = func
    return func

def on_store(func: Callable):
    event_handlers[ServerEvent.ON_STORE] = func
    return func
