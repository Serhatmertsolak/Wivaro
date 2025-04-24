import os
import csv

class FileLogger:
    def __init__(self, filepath):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # Add header row if file does not exist
        if not os.path.exists(filepath):
            with open(filepath, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "status"])
        self.filepath = filepath

    def log(self, status, timestamp):
        """
        status: True/False
        timestamp: datetime object
        """
        with open(self.filepath, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp.isoformat(), "UP" if status else "DOWN"])
