import pytest
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

# Примеры данных для тестирования
TEST_DATA = {"name": "John Doe", "email": "john@example.com"}


@pytest.mark.asyncio
async def test_create(sqlalchemy_repository):
    # Тестирование успешного создания записи
    res_id = await sqlalchemy_repository.create(**TEST_DATA)
    assert res_id is not None

    # Проверяем, что запись была добавлена в базу данных
    res = await sqlalchemy_repository.get(res_id)
    assert res['name'] == TEST_DATA['name']
    assert res['email'] == TEST_DATA['email']


@pytest.mark.asyncio
async def test_get(sqlalchemy_repository):
    # Тестирование получения записи по id
    res_id = await sqlalchemy_repository.create(**TEST_DATA)
    res = await sqlalchemy_repository.get(res_id)
    assert res['name'] == TEST_DATA['name']
    assert res['email'] == TEST_DATA['email']


@pytest.mark.asyncio
async def test_get_not_found(sqlalchemy_repository):
    # Тестирование получения несуществующей записи
    with pytest.raises(HTTPException) as excinfo:
        await sqlalchemy_repository.get(9999)
    assert excinfo.value.status_code == 404


@pytest.mark.asyncio
async def test_get_all(sqlalchemy_repository):
    # Тестирование получения всех записей
    await sqlalchemy_repository.create(**TEST_DATA)
    await sqlalchemy_repository.create(name="Jane Doe", email="jane@example.com")
    res = await sqlalchemy_repository.get_all()
    assert len(res) >= 2


@pytest.mark.asyncio
async def test_update(sqlalchemy_repository):
    # Тестирование обновления записи
    res_id = await sqlalchemy_repository.create(**TEST_DATA)
    new_data = {"name": "John Smith", "email": "john.smith@example.com"}
    await sqlalchemy_repository.update(res_id, **new_data)
    res = await sqlalchemy_repository.get(res_id)
    assert res['name'] == new_data['name']
    assert res['email'] == new_data['email']


@pytest.mark.asyncio
async def test_delete(sqlalchemy_repository):
    # Тестирование удаления записи
    res_id = await sqlalchemy_repository.create(**TEST_DATA)
    await sqlalchemy_repository.delete(res_id)
    with pytest.raises(HTTPException) as excinfo:
        await sqlalchemy_repository.get(res_id)
    assert excinfo.value.status_code == 404


@pytest.mark.asyncio
async def test_create_duplicate(sqlalchemy_repository):
    # Тестирование создания дублирующейся записи
    await sqlalchemy_repository.create(**TEST_DATA)
    with pytest.raises(SQLAlchemyError):
        await sqlalchemy_repository.create(**TEST_DATA)
