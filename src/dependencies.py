from typing import Annotated

from fastapi import Depends

from utils.uow import IUnitOfWork, UnitOfWork




UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]

