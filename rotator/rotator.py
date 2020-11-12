import os
from typing import Tuple
from rotator.settings import rotator_settings


class Rotator:

    async def rotate(self, filepath: str) -> Tuple[bool, str]:
        """
        Rotates log file if it's too big.
        Returns True if file was rotated, False otherwise
        :param filepath: str
        :return: bool
        """
        if os.path.getsize(filepath) > rotator_settings.MAX_LOG_SIZE:
            os.rename(filepath, filepath + '_old')
            os.system('kill -USR1 `cat /var/run/nginx.pid`')
            return True, filepath + '_old'
        return False, filepath

