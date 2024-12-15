from kiss_ai_stack.core.utilities.logger import LOG
from kiss_ai_stack_server.events.event_handlers import on_close
from kiss_ai_stack_server.models.db.session import Session
from kiss_ai_stack_server.services.kiss_ai_agent_service import KissAIAgentService
from kiss_ai_stack_server.services.session_service import SessionService
from kiss_ai_stack_types.enums import SessionScope
from kiss_ai_stack_types.models import QueryRequestBody, GenericResponseBody


@on_close
async def handle_close(data: QueryRequestBody, session: Session = None) -> GenericResponseBody:
    stack = KissAIAgentService()
    temporary = session.scope == SessionScope.TEMPORARY
    await stack.destroy_agent(agent_id=session.client_id, cleanup=temporary)
    LOG.info(f'CloseEventHandler :: Agent session {session.client_id} closed')
    if temporary:
        await SessionService.deactivate_session(session.client_id)
        LOG.info(f'CloseEventHandler :: Temporary client {session.client_id} deactivated')

    return GenericResponseBody(
        agent_id=session.client_id,
        result='Good bye!'
    )
