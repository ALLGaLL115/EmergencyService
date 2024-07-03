from fastapi import APIRouter

from dependencies import UOWDep
from services.listeners_services import ListenersService



router = APIRouter(
    prefix="/listeners"
)


@router.get('/{id}')
async def listener(id: int,  uow: UOWDep):
    response = await ListenersService().get_listener(id, uow)
    return response