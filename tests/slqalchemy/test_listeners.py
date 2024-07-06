
import pytest
from schemas.listeners_schemas import ListenersCreateSchema, ListenersShcema
from tests.slqalchemy.conftest import set_up_db
from utils.uow import IUnitOfWork

dd = ListenersCreateSchema(name='', phone='88888888888', email='sdfsd@mail.ru')
ddu = ListenersShcema(id=1, name='1', phone='88888888888', email='sdfsd@mail.ru')
ddr = ListenersShcema(id=1, name='', phone='88888888888', email='sdfsd@mail.ru')

async def test_create(tuow: IUnitOfWork):
    async with tuow:
        res = await tuow.listeners.create(**dd.model_dump())

        assert res == 1 


async def test_get(tuow: IUnitOfWork):
    async with tuow:
        await tuow.listeners.create(**dd.model_dump())
        res = await tuow.listeners.get(1)
        assert res == ddr


async def test_get_all(tuow: IUnitOfWork):
    async with tuow:
        res = await tuow.listeners.get_all()
    pass





async def test_update(tuow: IUnitOfWork):
    async with tuow:
        await tuow.listeners.create(**dd.model_dump())
        res = await tuow.listeners.update(id=1, name='1')
        assert res == 1


async def test_delete(tuow: IUnitOfWork):
    async with tuow:
        await tuow.listeners.create(**dd.model_dump())

        res = await tuow.listeners.delete(id=1)
        assert res == 1


