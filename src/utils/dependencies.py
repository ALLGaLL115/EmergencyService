from typing import Annotated

from fastapi import Depends

from uow import IUnitOfWork, UnitOfWork



UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
