import os
import json
import datetime
from pathlib import Path

class TimeManager:
    def __init__(self):
        self.data_dir = Path.home() / ".time_tracker"
        self.metadata_file = self.data_dir / "metadata.json"
        self._ensure_data_dir()
        
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)
        if not self.metadata_file.exists():
            self._save_metadata({"is_tracking": False, "start_time": None})
            
    def _load_metadata(self):
        """Load tracking metadata"""
        with open(self.metadata_file, "r") as f:
            return json.load(f)
            
    def _save_metadata(self, data):
        """Save tracking metadata"""
        with open(self.metadata_file, "w") as f:
            json.dump(data, f)
            
    def start_tracking(self):
        """Start time tracking"""
        now = datetime.datetime.now()
        self._save_metadata({"is_tracking": True, "start_time": now.isoformat()})
        return now
        
    def stop_tracking(self):
        """Stop time tracking and return start and end times"""
        metadata = self._load_metadata()
        start_time = datetime.datetime.fromisoformat(metadata["start_time"])
        end_time = datetime.datetime.now()
        self._save_metadata({"is_tracking": False, "start_time": None})
        return start_time, end_time
        
    def is_tracking(self):
        """Check if tracking is active"""
        metadata = self._load_metadata()
        return metadata.get("is_tracking", False)