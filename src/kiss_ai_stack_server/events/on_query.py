from kiss_ai_stack.core.utilities.logger import LOG
from kiss_ai_stack_server.events.event_handlers import on_query
from kiss_ai_stack_server.models.db.session import Session
from kiss_ai_stack_server.services.kiss_ai_agent_service import KissAIAgentService
from kiss_ai_stack_types.models import QueryRequestBody, GenericResponseBody


@on_query
async def handle_query(data: QueryRequestBody, session: Session) -> GenericResponseBody:
    stack = KissAIAgentService()
    answer = await stack.generate_answer(
        agent_id=session.client_id,
        query=data.query
    )
    LOG.info(f'QueryEventHandler :: Agent session {session.client_id} answer generated')

    return GenericResponseBody(
        agent_id=session.client_id,
        result=answer.answer,
        extras={
            'query': data.query,
            'metadata': answer.metadata,
            'distances': answer.distances,
            'supporting_documents': answer.supporting_documents
        }
    )
