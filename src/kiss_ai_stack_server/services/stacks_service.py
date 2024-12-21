from typing import List, Dict, Any, Optional

from kiss_ai_stack import Stacks


class StacksService:
    _instance = None

    def __new__(cls):
        """
        Ensure only one instance of the class is created.

        :returns: The singleton instance of the class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__stacks = Stacks()
        return cls._instance

    def __init__(self):
        pass

    async def bootstrap_stack(self, stack_id: str, temporary: Optional[bool] = True):
        """
        Initialize the AI stack.

        :param stack_id: Stack session's unique id, preferably client Id
        :param temporary: Whether to keep or cleanup stored docs
        """
        await self.__stacks.bootstrap_stack(stack_id=stack_id, temporary=temporary)

    async def store_data(self, stack_id: str, files: List[str], metadata: Optional[Dict[str, Any]]):
        """
        Store documents using the AI stacks' core.

        :param stack_id: Stack's unique id, preferably client Id
        :param files: List of file paths to store
        :param metadata: Metadata for files/documents
        :returns: Status of storing documents
        """
        return await self.__stacks.store_data(stack_id=stack_id, files=files, metadata=metadata)

    async def generate_answer(self, stack_id: str, query: any):
        """
        Process a query using AI stacks.

        :param stack_id: Stack session's unique id, preferably client Id
        :param query: User query/prompt input
        :returns: Answer for user prompt or query.
        """
        return await self.__stacks.generate_answer(stack_id=stack_id, query=query)

    async def destroy_stack(self, stack_id: str, cleanup: bool = False):
        """
        Destroy the AI stack's session and release resources.

        :param stack_id: Identifier of the stack to destroy.
        :param cleanup: Prompt to remove user data if RAG tools present, cleanup stored docs.
        """
        if hasattr(self.__stacks.get_stack(stack_id=stack_id), 'destroy_stack'):
            await self.__stacks.destroy_stack(stack_id=stack_id, cleanup=cleanup)
