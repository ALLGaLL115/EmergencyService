from pydantic import BaseModel


class ListenersCreateSchema(BaseModel):
    name: str
    phone: str
    email: str

class ListenersShcema(BaseModel):
    id: int
    user_id: int
    name: str
    phone: str
    email: str