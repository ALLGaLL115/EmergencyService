from fastapi.responses import JSONResponse

from uow import IUnitOfWork




class ListenersService:

    async def get_listener(self, id: int, uow: IUnitOfWork):
        async with uow:
            try:
                listener = await uow.listeners.get(id=id)
                return JSONResponse(content=listener)
            except Exception as e:
                raise 
            
    
 