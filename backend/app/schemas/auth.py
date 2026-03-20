from datetime import datetime

from pydantic import BaseModel


class LoginResponse(BaseModel):
    authorization_url: str
    state: str
    demo_mode: bool


class AuthStatusResponse(BaseModel):
    connected: bool
    demo_mode: bool
    token_expires_at: datetime | None
    scopes: list[str]
    refresh_supported: bool
    issues: list[str]
