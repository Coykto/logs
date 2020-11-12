import os
import re
from parser.settings import parser_settings
from rotator import Rotator
from storage import Storage


class Parser:

    def __init__(self, config):
        self.log_file = config.get('log_file')
        self.read_point = 0
        self.regex = self._compile_regex()
        self.rotator = Rotator()
        self.storage = Storage()

    def _compile_regex(self):
        regex_str = r''.join(parser_settings.REGEX)
        return re.compile(regex_str)

    async def _parse_line(self, line: str) -> dict:
        return self.regex.search(line).groupdict()

    async def rotate_log(self):
        rotated, self.log_file = await self.rotator.rotate(self.log_file)
        if rotated:
            self.read_point = 0

    async def parse(self):
        await self.rotate_log()

        if not os.path.isfile(self.log_file):
            raise FileNotFoundError(
                f'Log file {self.log_file} not found!'
            )

        with open(self.log_file, 'r') as log:
            for _ in range(self.read_point):
                next(log)
            for line in log.readlines():
                log_data = await self._parse_line(line)
                self.storage.save(
                    {
                        'timestamp': log_data.get('timestamp'),
                        'type': log_data.get('type'),
                        'status': log_data.get('status'),
                        'bytes': log_data.get('bytes'),
                        'connection': log_data.get('connection'),
                    }
                )
                self.read_point += 1
