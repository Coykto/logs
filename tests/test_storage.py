from storage import (
    Storage,
    storage_settings,
)
import pytest
import time

@pytest.fixture
def storage():
    storage = Storage()
    storage.log_collection.clear()
    yield storage


@pytest.mark.asyncio
async def test_storage_must_save_valid_log_entry_to_collection(
    storage,
):
    assert storage.log_collection == []
    log_data = {
        'timestamp': str(time.time()),
        'type': '.ts',
        'status': '200',
        'bytes': '537412',
        'connection': '8831',
    }
    storage.save(log_data)
    assert storage.log_collection == [log_data]


@pytest.mark.asyncio
async def test_storage_must_not_save_old_log_entry_to_collection(
    storage,
):
    assert storage.log_collection == []
    t = time.time()
    log_data = {
        'timestamp': str(time.time() - storage_settings.LOG_TTL - 1),
        'type': '.ts',
        'status': '200',
        'bytes': '537412',
        'connection': '8831',
    }
    storage.save(log_data)
    assert storage.log_collection == []


@pytest.mark.asyncio
async def test_storage_must_rotate_old_log_entry_in_collection(
    storage,
):
    storage.log_collection = [
        {
            'timestamp': str(time.time() - storage_settings.LOG_TTL - 1),
            'type': '.ts',
            'status': '200',
            'bytes': '537412',
            'connection': '8831',
        }
    ]
    assert len(storage.log_collection) == 1
    log_data = {
        'timestamp': str(time.time()),
        'type': '.ts',
        'status': '200',
        'bytes': '537412',
        'connection': '8831',
    }
    storage.save(log_data)
    assert len(storage.log_collection) == 1
    assert storage.log_collection == [log_data]
