from pydantic import BaseModel
from typing import List, Optional

class Scores(BaseModel):
    clarity: int
    coherence: int
    grammar: int
    originality: int
    verbosity: int
    tone_consistency: int

class AnalyzeResponse(BaseModel):
    overall_score: float
    scores: Scores
    ai_likeness: float
    weaknesses: List[str]
    strengths: List[str]
    suggestions: List[str]
    summary: str

class ImproveResponse(BaseModel):
    original_text: str
    improved_text: str
    changes_made: List[str]
    explanation: str
