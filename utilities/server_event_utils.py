from fastapi import HTTPException

from events import event_handlers
from models.enums.events import ServerEvent


def handle_server_event(event: ServerEvent, data: dict):
    """
    Generic handler for server events with consistent error handling.

    Args:
        event (ServerEvent): The specific server event to handle
        data (dict): The request data

    Returns:
        The result of the event handler

    Raises:
        HTTPException: If no handler is found for the event
    """
    if event in event_handlers:
        return event_handlers[event](data)
    raise HTTPException(
        status_code=404,
        detail=f'{event} handler not found'
    )
