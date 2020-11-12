import os
from rotator.rotator import (
    Rotator,
    rotator_settings
)
import pytest

@pytest.mark.asyncio
async def test_rotator_must_raise_exception_if_file_does_not_exist():
    with pytest.raises(FileNotFoundError):
        await Rotator().rotate('not/a/real/file/path.log')


@pytest.mark.asyncio
async def test_rotator_must_not_rotate_small_log_file(
    tmp_log,
):
    open(tmp_log, 'a').close()
    rotation_result = await Rotator().rotate(tmp_log)
    assert rotation_result == (False, tmp_log)


@pytest.mark.asyncio
async def test_rotator_must_rotate_big_log_file(
    mocker,
    tmp_log,
):
    with open(tmp_log, 'w') as log:
        log.write(
            str(os.urandom(rotator_settings.MAX_LOG_SIZE + 1))
        )
    from rotator.rotator import os as rotator_os
    rename = mocker.patch.object(rotator_os, 'rename', mocker.Mock())
    system = mocker.patch.object(rotator_os, 'system', mocker.Mock())
    rotation_result = await Rotator().rotate(tmp_log)
    assert rotation_result == (True, tmp_log + '_old')
    assert rename.called_once_with(tmp_log, tmp_log + '_old')
    assert system.called_once_with('kill -USR1 `cat /var/run/nginx.pid`')
