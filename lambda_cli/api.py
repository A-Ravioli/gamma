import json
import requests
from typing import List, Dict, Any, Optional
from . import config

class LambdaAPIClient:
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.auth = config.get_auth()
        self.headers = config.get_headers()

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make a request to the Lambda Labs API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.request(
            method=method,
            url=url,
            auth=self.auth,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def list_instances(self) -> Dict:
        """List all instances"""
        return self._make_request("GET", "/instances")

    def get_instance(self, instance_id: str) -> Dict:
        """Get details of a specific instance"""
        return self._make_request("GET", f"/instances/{instance_id}")

    def launch_instance(self, region_name: str, instance_type: str, 
                       ssh_keys: List[str], filesystem_names: List[str] = None,
                       quantity: int = 1) -> Dict:
        """Launch a new instance"""
        data = {
            "region_name": region_name,
            "instance_type_name": instance_type,
            "ssh_key_names": ssh_keys,
            "file_system_names": filesystem_names or [],
            "quantity": quantity
        }
        return self._make_request("POST", "/instance-operations/launch", data)

    def restart_instances(self, instance_ids: List[str]) -> Dict:
        """Restart specified instances"""
        data = {"instance_ids": instance_ids}
        return self._make_request("POST", "/instance-operations/restart", data)

    def terminate_instances(self, instance_ids: List[str]) -> Dict:
        """Terminate specified instances"""
        data = {"instance_ids": instance_ids}
        return self._make_request("POST", "/instance-operations/terminate", data)

    def list_instance_types(self) -> Dict:
        """List available instance types"""
        return self._make_request("GET", "/instance-types")

    def list_ssh_keys(self) -> Dict:
        """List all SSH keys"""
        return self._make_request("GET", "/ssh-keys")

    def add_ssh_key(self, name: str, public_key: Optional[str] = None) -> Dict:
        """Add an SSH key or generate a new one"""
        data = {"name": name}
        if public_key:
            data["public_key"] = public_key
        return self._make_request("POST", "/ssh-keys", data)

    def delete_ssh_key(self, key_id: str) -> Dict:
        """Delete an SSH key"""
        return self._make_request("DELETE", f"/ssh-keys/{key_id}")

    def list_filesystems(self) -> Dict:
        """List all filesystems"""
        return self._make_request("GET", "/file-systems") 