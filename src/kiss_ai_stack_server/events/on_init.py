from kiss_ai_stack.core.utilities.logger import LOG
from kiss_ai_stack_server.events.event_handlers import on_init
from kiss_ai_stack_server.models.db.session import Session
from kiss_ai_stack_server.services.stacks_service import StacksService
from kiss_ai_stack_types.enums import SessionScope
from kiss_ai_stack_types.models import QueryRequestBody, GenericResponseBody


@on_init
async def handle_init(data: QueryRequestBody, session: Session) -> GenericResponseBody:
    stacks = StacksService()
    temporary = session.scope == SessionScope.TEMPORARY
    await stacks.bootstrap_stack(stack_id=session.client_id, temporary=temporary)
    LOG.info(f'InitEventHandler :: Stack session {session.client_id} initialized and standby')

    return GenericResponseBody(
        stack_id=session.client_id,
        result='Greetings!'
    )
