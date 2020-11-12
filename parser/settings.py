class Settings:

    TIMESTAMP_KEY = 'time'
    RESCHEDULE_TIME = 5

    REGEX = [
        r'((?P<time_key>.+\"time\").+\| (?P<timestamp>\d+\.?\d+))?',
        r'((?P<uri_key>.+\"uri\").+(?P<type>\.ts|\.m3u8))?',
        r'((?P<status_key>.+\"status\": ")(?P<status>\d+))?',
        r'((?P<bytes_key>.+\"bytes_sent\": ")(?P<bytes>\d+))?',
        r'((?P<connection_key>.+\"connection\" : ")(?P<connection>\d+))?',
    ]


parser_settings = Settings()
