from pydantic import BaseModel


class ListenersCreateSchema(BaseModel):
    owner_id: int
    name: str
    phone: str
    email: str

class ListenersShcema(BaseModel):
    id: int
    owner_id: int
    name: str
    phone: str
    email: str