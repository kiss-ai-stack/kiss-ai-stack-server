import base64

from fastapi import Depends, HTTPException

from events.event_handlers import on_store
from models.documents import DocumentsRequestBody
from services.kiss_ai_agent_service import kiss_ai_agent_service, KissAIAgentService
from utilities.temp_file_manager import TemporaryFileManager, temp_file_manager


@on_store
async def handle_store(data: DocumentsRequestBody, agent: KissAIAgentService = Depends(kiss_ai_agent_service),
                       temp_files: TemporaryFileManager = Depends(temp_file_manager)):
    temp_dir = temp_files.create_temp_dir()

    try:
        file_paths = []

        for file_data in data.files:
            filename = file_data.get('name', 'unnamed_file')
            content = file_data.get('content', '')
            safe_filename = temp_files.safe_file_path(temp_dir, filename)

            try:
                file_content = base64.b64decode(content)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid base64 content for file {filename}: {str(e)}"
                )
            with open(safe_filename, "wb") as buffer:
                buffer.write(file_content)
            file_paths.append(safe_filename)

        metadata = data.metadata or {}

        try:
            result = agent.store(
                files=file_paths,
                metadata=metadata
            )
            return {
                "status": "success",
                "files_stored": len(file_paths),
                "result": result
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error storing documents: {str(e)}"
            )
    finally:
        temp_files.cleanup_dir(temp_dir)
