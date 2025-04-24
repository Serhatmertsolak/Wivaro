

import time
import subprocess
import os
import csv
import sys
from datetime import datetime

class PingMonitor:
    def __init__(self, target, interval=5):
        self.target = target
        self.interval = interval
        # Determine ping command based on OS
        if sys.platform.startswith("win"):
            self.ping_args = ["ping", "-n", "1", self.target]
        else:
            self.ping_args = ["ping", "-c", "1", self.target]

    def ping(self):
        """Send a single ping, return True if host is reachable."""
        try:
            result = subprocess.run(
                self.ping_args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception:
            return False

    def run(self):
        """
        Every self.interval seconds, send a ping and yield a tuple:
        (status: bool, timestamp: datetime).
        """
        while True:
            status = self.ping()
            timestamp = datetime.now()
            yield status, timestamp
            time.sleep(self.interval)

class FileLogger:
    def __init__(self, filepath):
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # If file doesn't exist, write CSV header
        if not os.path.exists(filepath):
            with open(filepath, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "status"])
        self.filepath = filepath

    def log(self, status, timestamp):
        """Append a log entry with ISO timestamp and status ("UP"/"DOWN")."""
        with open(self.filepath, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp.isoformat(), "UP" if status else "DOWN"])

def main():
    target   = "8.8.8.8"      # Address to monitor
    interval = 5              # Seconds between pings
    # Path: logs/internet_log.csv in the script's directory
    base = os.path.dirname(__file__)
    log_path = os.path.join(base, "logs", "internet_log.csv")

    monitor = PingMonitor(target, interval)
    logger  = FileLogger(log_path)

    print(f"\n👉 Started: pinging {target} every {interval}s.")
    print(f"👉 Logging to: {log_path}\n(Press CTRL+C to stop)\n")

    prev_status    = True
    downtime_start = None

    try:
        for status, ts in monitor.run():
            logger.log(status, ts)
            # Downtime begins
            if not status and prev_status:
                downtime_start = ts
                print(f"[{ts.strftime('%H:%M:%S')}] ⛔ Downtime started")
            # Service restored
            if status and not prev_status and downtime_start:
                duration = ts - downtime_start
                print(f"[{ts.strftime('%H:%M:%S')}] ✅ Back up (duration: {duration})")
                downtime_start = None
            prev_status = status
    except KeyboardInterrupt:
        print("\n❚❚ Stopped. Goodbye!")

if __name__ == "__main__":
    main()
