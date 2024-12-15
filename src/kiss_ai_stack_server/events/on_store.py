import base64

from fastapi import HTTPException
from kiss_ai_stack.core.utilities.logger import LOG
from kiss_ai_stack_server.events.event_handlers import on_store
from kiss_ai_stack_server.models.db.session import Session
from kiss_ai_stack_server.services.kiss_ai_agent_service import KissAIAgentService
from kiss_ai_stack_server.utilities.temp_file_manager import temp_file_manager
from kiss_ai_stack_types.models import DocumentsRequestBody, GenericResponseBody


@on_store
async def handle_store(data: DocumentsRequestBody, session: Session = None) -> GenericResponseBody:
    stack = KissAIAgentService()
    temp_files = temp_file_manager()
    temp_dir = temp_files.create_temp_dir()
    files_stored = None

    try:
        file_paths = []

        for file_data in data.files:
            filename = file_data.name
            content = file_data.content
            safe_filename = temp_files.safe_file_path(temp_dir, filename)

            try:
                file_content = base64.b64decode(content)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f'StoreEventHandler :: Agent session {session.client_id} Invalid base64 content for file {filename}: {str(e)}'
                )
            with open(safe_filename, "wb") as buffer:
                buffer.write(file_content)
            file_paths.append(safe_filename)
        metadata = data.metadata or {}

        try:
            files_stored = await stack.store_data(
                agent_id=session.client_id,
                files=file_paths,
                metadata=metadata
            )
            LOG.info(f'StoreEventHandler :: Agent session {session.client_id} documents stored')
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Error storing documents: Agent session {session.client_id} {str(e)}'
            )
    except Exception as e:
        LOG.error(f'StoreEventHandler :: Agent session {session.client_id} {str(e)}')
    finally:
        temp_files.cleanup_dir(temp_dir)
        LOG.info(f'StoreEventHandler :: Agent session {session.client_id} temporary files cleaned')
        return GenericResponseBody(
            agent_id=session.client_id,
            result='Files stored',
            extras=files_stored
        )
