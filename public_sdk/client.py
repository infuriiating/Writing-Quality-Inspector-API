import requests
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class AnalyzeResponse:
    overall_score: float
    scores: Dict[str, int]
    ai_likeness: float
    weaknesses: List[str]
    strengths: List[str]
    suggestions: List[str]
    summary: str

@dataclass
class ImproveResponse:
    original_text: str
    improved_text: str
    changes_made: List[str]
    explanation: str

class WritingQualityClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        """
        Initialize the client.
        
        Args:
            base_url: The URL where the API is hosted.
            api_key: The 'API_SECRET' to authenticate requests.
        """
        self.base_url = base_url.rstrip("/")
        self.headers = {}
        if api_key:
            self.headers["x-api-key"] = api_key

    def analyze(self, text: str, purpose: str = "general", audience: str = "general", strict: bool = False) -> AnalyzeResponse:
        """
        Analyze text quality.
        """
        payload = {
            "text": text,
            "purpose": purpose,
            "audience": audience,
            "strict": strict
        }
        
        response = requests.post(f"{self.base_url}/analyze", json=payload, headers=self.headers)
        if response.status_code == 403:
            raise PermissionError("Invalid API Key.")
        response.raise_for_status()
        data = response.json()
        
        return AnalyzeResponse(**data)

    def improve(self, text: str, focus: List[str], preserve_tone: bool = True) -> ImproveResponse:
        """
        Improve text based on specific focus areas.
        """
        payload = {
            "text": text,
            "focus": focus,
            "preserve_tone": preserve_tone
        }
        
        response = requests.post(f"{self.base_url}/improve", json=payload, headers=self.headers)
        if response.status_code == 403:
            raise PermissionError("Invalid API Key.")
        response.raise_for_status()
        data = response.json()
        
        return ImproveResponse(
            original_text=data.get("original_text", ""),
            improved_text=data.get("improvements", data.get("improved_text", "")),
            changes_made=data.get("changes_made", []),
            explanation=data.get("explanation", "")
        )

    def check_health(self) -> bool:
        """Check if the API is running (No auth required)."""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False
