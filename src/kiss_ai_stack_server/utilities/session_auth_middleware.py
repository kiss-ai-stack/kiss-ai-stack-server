from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

from kiss_ai_stack_server.services.session_service import SessionService
from kiss_ai_stack_server.services.token_service import TokenService


class SessionAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.scope['type'] == 'websocket':
            return await call_next(request)

        if request.url.path == '/auth' or request.method == 'OPTIONS':
            return await call_next(request)

        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer' not in auth_header:
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={'detail': 'Authorization header missing'}
            )

        try:
            token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else None
            if not token:
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={'detail': 'Invalid token format'}
                )
            payload = TokenService.decode_token(token)
            session = await SessionService.get_active_session_by_client_id(
                client_id=payload['sub']
            )
            if not session:
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={'detail': 'Invalid or inactive session'}
                )
            request.state.session = session

        except HTTPException as http_exc:
            return JSONResponse(
                status_code=http_exc.status_code,
                content={'detail': http_exc.detail}
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={'detail': 'Authentication failed'}
            )
        return await call_next(request)
