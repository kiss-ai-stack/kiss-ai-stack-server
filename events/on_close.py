from fastapi import Depends

from events import on_close
from services.kiss_ai_agent_service import kiss_ai_agent_service, KissAIAgentService


@on_close
async def handle_close(data, agent: KissAIAgentService = Depends(kiss_ai_agent_service)):
    agent.close()
