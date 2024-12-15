from fastapi import HTTPException
from kiss_ai_stack_types.enums import ServerEvent
from kiss_ai_stack_types.models import QueryRequestBody, GenericResponseBody, SessionResponse, DocumentsRequestBody

from kiss_ai_stack_server.events import event_handlers
from kiss_ai_stack_server.models.db import Session


def handle_server_event(
        event: ServerEvent,
        data: QueryRequestBody | DocumentsRequestBody,
        session: Session = None
) -> GenericResponseBody | SessionResponse:
    """
    Generic handler for server events with consistent error handling.

    :param event: (ServerEvent) The specific server event to handle
    :param data: Inputs to pass into the event
    :param session: Authorized client data
    :returns: The result of the event handler
    :raises HTTPException: If no handler is found for the event
    """
    if event in event_handlers:
        return event_handlers[event](data, session)
    raise HTTPException(
        status_code=404,
        detail=f'{event} handler not found'
    )
