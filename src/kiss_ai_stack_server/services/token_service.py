import os
from datetime import datetime, timedelta, UTC
from typing import Optional, Dict

import jwt
from fastapi import HTTPException
from kiss_ai_stack_types.enums import SessionScope


class TokenService:
    SECRET_KEY = os.getenv('ACCESS_TOKEN_SECRET_KEY', 'your-secret-key')
    ALGORITHM = os.getenv('ACCESS_TOKEN_ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

    @classmethod
    def generate_token(
            cls,
            client_id: str,
            scope: SessionScope,
            expires_delta: Optional[timedelta] = None
    ) -> str:
        payload = {
            'sub': client_id,
            'scope': scope.value,
            'exp': datetime.now(UTC) + (expires_delta or timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES))
        }
        return jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_token(cls, token: str) -> Dict:
        """Decode and validate JWT token"""
        try:
            return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
