import secrets
import uuid

from kiss_ai_stack_types.enums import SessionScope
from tortoise import fields, models


class Session(models.Model):
    id = fields.IntField(pk=True)
    client_id = fields.CharField(max_length=255, unique=True, null=False, default=lambda: str(uuid.uuid4()))
    client_secret = fields.CharField(max_length=255, null=False, default=lambda: secrets.token_urlsafe(32))
    scope = fields.CharEnumField(SessionScope)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    status = fields.BooleanField(default=True)

    class Meta:
        table = 'sessions'

    def verify_secret(self, secret: str) -> bool:
        """Verify the client secret"""
        return self.client_secret == secret
