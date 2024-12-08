from fastapi.params import Depends

from events.event_handlers import on_auth
from services.kiss_ai_agent_service import kiss_ai_agent_service, KissAIAgentService


@on_auth
async def handle_auth(data, agent: KissAIAgentService = Depends(kiss_ai_agent_service)):
    return {"status": "auth completed"}
