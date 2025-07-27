from pydantic import BaseModel


class MessagePayload(BaseModel):
    topic: str
    message: str