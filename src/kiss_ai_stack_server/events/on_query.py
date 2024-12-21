from kiss_ai_stack.core.utilities.logger import LOG
from kiss_ai_stack_server.events.event_handlers import on_query
from kiss_ai_stack_server.models.db.session import Session
from kiss_ai_stack_server.services.stacks_service import StacksService
from kiss_ai_stack_types.models import QueryRequestBody, GenericResponseBody


@on_query
async def handle_query(data: QueryRequestBody, session: Session) -> GenericResponseBody:
    stacks = StacksService()
    answer = await stacks.generate_answer(
        stack_id=session.client_id,
        query=data.query
    )
    LOG.info(f'QueryEventHandler :: Stack session {session.client_id} answer generated')

    return GenericResponseBody(
        stack_id=session.client_id,
        result=answer.answer,
        extras={
            'query': data.query,
            'metadata': answer.metadata,
            'distances': answer.distances,
            'supporting_documents': answer.supporting_documents
        }
    )
