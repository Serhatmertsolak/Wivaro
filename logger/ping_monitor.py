import time
import subprocess
from datetime import datetime

class PingMonitor:
    def __init__(self, target, interval=5):
        self.target = target
        self.interval = interval
        self.last_status = True  # assume connection is up by default

    def ping(self):
        """Send a single ping; return True if reachable, False otherwise."""
        try:
            # Linux/Mac: use '-c 1'; for Windows, use ['ping', '-n', '1', ...]
            result = subprocess.run(
                ["ping", "-c", "1", self.target],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception:
            return False

    def run(self):
        """
        Infinite loop that pings every interval seconds.
        Yields a tuple (status, timestamp).
        """
        while True:
            status = self.ping()
            timestamp = datetime.now()
            yield status, timestamp
            time.sleep(self.interval)
