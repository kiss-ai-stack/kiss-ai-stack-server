from typing import List, Dict, Any, Optional

from kiss_ai_stack import AgentStack


class KissAIAgentService:
    _instance = None

    def __new__(cls):
        """
        Ensure only one instance of the class is created.

        :returns: The singleton instance of the class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__stack = AgentStack()
        return cls._instance

    def __init__(self):
        pass

    async def bootstrap_agent(self, agent_id: str, temporary: Optional[bool] = True):
        """
        Initialize the AI agent stack.

        :param agent_id: Agent session's unique id, preferably client Id
        :param temporary: Whether to keep or cleanup stored docs
        """
        await self.__stack.bootstrap_agent(agent_id=agent_id, temporary=temporary)

    async def store_data(self, agent_id: str, files: List[str], metadata: Optional[Dict[str, Any]]):
        """
        Store documents using the AI agent stack core.

        :param agent_id: Agent's unique id, preferably client Id
        :param files: List of file paths to store
        :param metadata: Metadata for files/documents
        :returns: Status of storing documents
        """
        return await self.__stack.store_data(agent_id=agent_id, files=files, metadata=metadata)

    async def generate_answer(self, agent_id: str, query: any):
        """
        Process a query using the AI agent stack.

        :param agent_id: Agent session's unique id, preferably client Id
        :param query: User query/prompt input
        :returns: Answer for user prompt or query.
        """
        return await self.__stack.generate_answer(agent_id=agent_id, query=query)

    async def destroy_agent(self, agent_id: str, cleanup: bool = False):
        """
        Destroy the AI agent session and release resources.

        :param agent_id: Identifier of the agent to destroy.
        :param cleanup: Prompt to remove user data if RAG tools present, cleanup stored docs.
        """
        if hasattr(self.__stack.get_agent(agent_id=agent_id), 'destroy_stack'):
            await self.__stack.destroy_agent(agent_id=agent_id, cleanup=cleanup)
