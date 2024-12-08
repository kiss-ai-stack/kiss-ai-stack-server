from fastapi import Depends

from events.event_handlers import on_query
from models.queries import QueryRequestBody
from services.kiss_ai_agent_service import kiss_ai_agent_service, KissAIAgentService


@on_query
async def handle_init(data: QueryRequestBody, agent: KissAIAgentService = Depends(kiss_ai_agent_service)):
    return agent.process(data.query)
