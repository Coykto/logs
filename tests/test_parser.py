from parser import (
    Parser,
    parser_settings,
)
import pytest
import json
import time
from parser.parser import (
    Rotator,
    Storage,
)
from tests.conftest import AsyncMock


@pytest.fixture
def rotator(
    mocker,
    tmp_log,
):
    rotator = mocker.patch.object(
        Rotator,
        'rotate',
        AsyncMock()
    )
    rotator.return_value = (False, tmp_log)
    yield rotator


@pytest.fixture
def save(
    mocker,
):
    save = mocker.patch.object(
        Storage,
        'save',
        mocker.Mock()
    )
    yield save


@pytest.mark.asyncio
async def test_parser_raises_error_if_log_does_not_exists():
    parser_config = {
        'log_file': 'not/a/real/file/path.log'
    }
    with pytest.raises(FileNotFoundError):
        await Parser(parser_config).parse()


@pytest.mark.asyncio
async def test_given_empty_file_parser_must_not_increases_read_point(
    tmp_log,
):
    open(tmp_log, 'a').close()
    parser = Parser({
        'log_file': tmp_log
    })
    assert parser.read_point == 0
    await parser.parse()
    assert parser.read_point == 0


@pytest.mark.asyncio
async def test_given_log_with_lines_parser_must_increase_read_point(
    tmp_log,
):
    with open(tmp_log, 'w') as log:
        for _ in range(10):
            line = json.dumps({
                parser_settings.TIMESTAMP_KEY:
                    "| " + str(time.time())
            })
            log.write(line + "\n")

    parser = Parser({
        'log_file': tmp_log
    })
    assert parser.read_point == 0
    await parser.parse()
    assert parser.read_point == 10


@pytest.mark.asyncio
async def test_parser_must_start_on_read_point(
    tmp_log,
    mocker,
):
    with open(tmp_log, 'w') as log:
        for _ in range(10):
            timestamp = time.time()
            line = json.dumps({
                parser_settings.TIMESTAMP_KEY: "| " + str(timestamp)
            })
            log.write(line + "\n")

    parse_line = mocker.patch.object(
        Parser,
        '_parse_line',
        AsyncMock()
    )
    parser = Parser({
        'log_file': tmp_log
    })
    parser.read_point = 9
    await parser.parse()
    parse_line.assert_called_once_with(line + "\n")


@pytest.mark.asyncio
async def test_parser_must_handle_file_to_rotator_and_update_read_point_if_needed(
    tmp_log,
    rotator,
):
    rotator.return_value = (True, tmp_log)
    parser = Parser({
        'log_file': tmp_log
    })
    parser.read_point = 9
    await parser.parse()
    assert parser.read_point == 0


@pytest.mark.asyncio
async def test_parsing(
    tmp_log,
    save,
):
    with open(tmp_log, 'w') as log:
        log.write('{"level": "http", "time": "2020-11-03T09:23:58+00:00 | 1604395438.982", "msg": streamer-default-7b6b975fc5-6h9fw, "details" : { "remote_addr": "10.233.65.0", "remote_user": "", "method" : "GET" ,"uri" : "/content/9/1414909267_160439534_9.ts?media_format=hls&media_type=live&content_id=123", "protocol": "HTTP/1.1", "status": "200", "cid": "", "bytes_sent": "537412", "referer": , "user_agent": "VLC/3.0.11.1 LibVLC/3.0.11.1", "time_request": "0.020", "request_length" : "517", "upstream_addr": "10.233.50.72:84 : 127.0.0.1:82", "upstream_connect_time": "0.004 : 0.000", "hwid": "", "ext_id" : "8893a74c79fbd5f9a259e993e3ba73e2", "connection" : "8831" , "connection_requests" : "3" , "complete" : "OK", "connections_active" : "2" ,"upstream_cache_status" : MISS, "cache_control": "no-store, no-cache, must-revalidate", "x_forwarded_for": "10.9.0.212", "x_serial_number": "", "x_session_token": ""}}')

    parser = Parser({
        'log_file': tmp_log
    })
    await parser.parse()
    save.assert_called_once_with(
        {
            'timestamp': '1604395438.982',
            'type': '.ts',
            'status': '200',
            'bytes': '537412',
            'connection': '8831',
        }
    )


@pytest.mark.asyncio
async def test_parsing_no_uri(
    tmp_log,
    save,
):
    with open(tmp_log, 'w') as log:
        log.write('{"level": "http", "time": "2020-11-03T09:23:58+00:00 | 1604395438.982", "msg": streamer-default-7b6b975fc5-6h9fw, "details" : { "remote_addr": "10.233.65.0", "remote_user": "", "method" : "GET" ,"protocol": "HTTP/1.1", "status": "200", "cid": "", "bytes_sent": "537412", "referer": , "user_agent": "VLC/3.0.11.1 LibVLC/3.0.11.1", "time_request": "0.020", "request_length" : "517", "upstream_addr": "10.233.50.72:84 : 127.0.0.1:82", "upstream_connect_time": "0.004 : 0.000", "hwid": "", "ext_id" : "8893a74c79fbd5f9a259e993e3ba73e2", "connection" : "8831" , "connection_requests" : "3" , "complete" : "OK", "connections_active" : "2" ,"upstream_cache_status" : MISS, "cache_control": "no-store, no-cache, must-revalidate", "x_forwarded_for": "10.9.0.212", "x_serial_number": "", "x_session_token": ""}}')

    parser = Parser({
        'log_file': tmp_log
    })
    await parser.parse()
    save.assert_called_once_with(
        {
            'timestamp': '1604395438.982',
            'type': None,
            'status': '200',
            'bytes': '537412',
            'connection': '8831',
        }
    )
