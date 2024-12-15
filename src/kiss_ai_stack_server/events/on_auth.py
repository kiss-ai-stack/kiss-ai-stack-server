from fastapi import HTTPException
from kiss_ai_stack.core.utilities.logger import LOG
from kiss_ai_stack_server.events.event_handlers import on_auth
from kiss_ai_stack_server.models.db.session import Session
from kiss_ai_stack_server.services.session_service import SessionService
from kiss_ai_stack_server.services.token_service import TokenService
from kiss_ai_stack_types.enums import SessionScope
from kiss_ai_stack_types.models import SessionRequest, SessionResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST


@on_auth
async def handle_auth(data: SessionRequest, session: Session = None) -> SessionResponse:
    scope = SessionScope(data.scope) if data.scope else None
    client_id = data.client_id
    client_secret = data.client_secret

    if (client_id and client_secret) or scope:
        session = await SessionService.create_or_get_session(
            scope=scope,
            client_id=client_id,
            client_secret=client_secret
        )
        if not session:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Invalid session request.'
            )
        access_token = TokenService.generate_token(client_id=session.client_id, scope=session.scope)
        LOG.info(f'AuthEventHandler :: Client {session.client_id} authorized')
        return SessionResponse(
            client_id=session.client_id,
            client_secret=session.client_secret,
            access_token=access_token
        )
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Value error, Either `scope` or both `client_id` and `client_secret` must be provided.'
        )
