from typing import List, Dict, Any, Optional
from functools import lru_cache

from kiss_ai_stack.core.agent import AgentStack


@lru_cache(maxsize=1)
def kiss_ai_agent_service():
    """
    Cached singleton factory function for AIAgentService.
    """
    return KissAIAgentService()


class KissAIAgentService:
    def __init__(self):
        """
        Initialize the service.
        """
        self.__agent = AgentStack()
        self.__is_initialized = False

    def initialize(self):
        """
        Initialize the AI agent stack.
        """
        if not self.__is_initialized:
            self.__agent.initialize_stack()
            self.__is_initialized = True

    def store(self, files: List[str], query: Optional[str], metadata: Optional[Dict[str, Any]]):
        """
        Store documents using the AI agent stack core.

        :param
            files: List of file paths to store
            metadata:
        :return: Result of storing documents
        """
        return self.__agent.store_documents(files=files)

    def process(self, query: any):
        """
        Process a query using the AI agent stack.

        :param query: Query inputs
        :return: Result of processed inputs
        """
        return self.__agent.process_query(query=query)

    def close(self):
        """
        Destroy the AI agent service and release resources.
        Resets the service to an uninitialized state.
        """
        if hasattr(self.__agent, 'close'):
            self.__agent.close()

        self.__is_initialized = False
        self.__agent = AgentStack()

    def __del__(self):
        self.close()
