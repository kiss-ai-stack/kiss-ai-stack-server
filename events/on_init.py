from fastapi import Depends

from events.event_handlers import on_init
from services.kiss_ai_agent_service import kiss_ai_agent_service, KissAIAgentService


@on_init
async def handle_init(data, agent: KissAIAgentService = Depends(kiss_ai_agent_service)):
    agent.initialize()
