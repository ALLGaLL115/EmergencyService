from pydantic import BaseModel


class ListenersShcema(BaseModel):
    id: int
    name: str
    phone: str
    email: str