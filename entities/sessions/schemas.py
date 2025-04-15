from pydantic import BaseModel
from datetime import datetime

class SessionBase(BaseModel):
    token: str
    expires_at: datetime

class SessionCreate(SessionBase):
    pass

class SessionOut(SessionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class VerifyCodeRequest(BaseModel):
    code: str
