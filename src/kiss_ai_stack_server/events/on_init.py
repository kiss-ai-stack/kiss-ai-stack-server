from kiss_ai_stack.core.utilities.logger import LOG
from kiss_ai_stack_server.events.event_handlers import on_init
from kiss_ai_stack_server.models.db.session import Session
from kiss_ai_stack_server.services.kiss_ai_agent_service import KissAIAgentService
from kiss_ai_stack_types.enums import SessionScope
from kiss_ai_stack_types.models import QueryRequestBody, GenericResponseBody


@on_init
async def handle_init(data: QueryRequestBody, session: Session) -> GenericResponseBody:
    stack = KissAIAgentService()
    temporary = session.scope == SessionScope.TEMPORARY
    await stack.bootstrap_agent(agent_id=session.client_id, temporary=temporary)
    LOG.info(f'InitEventHandler :: Agent session {session.client_id} initialized and standby')

    return GenericResponseBody(
        agent_id=session.client_id,
        result='Greetings!'
    )
