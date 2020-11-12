from unittest.mock import MagicMock
import pytest


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


@pytest.fixture
async def tmp_log(tmpdir):
    tmp_file = tmpdir.mkdir("sub").join("tmp_log.log")
    open(tmp_file, 'a').close()
    yield tmp_file

