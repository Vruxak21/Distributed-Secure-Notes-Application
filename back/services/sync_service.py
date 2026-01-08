import requests
import os
from typing import Dict, Any


class SyncService:

    @staticmethod
    def get_replica_url():
        return os.getenv("REPLICA_URL", "http://localhost:5001")
    
    @staticmethod
    def sync_to_replica(operation: str, data: Dict[Any, Any]) -> None:
        replica_url = SyncService.get_replica_url()
        endpoint = f"{replica_url}/api/sync/{operation}"
        
        try:
            response = requests.post(endpoint, json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to sync with replica: {e}")