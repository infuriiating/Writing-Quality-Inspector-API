from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="The text content to analyze")
    purpose: Optional[str] = Field("general", description="The intended purpose (e.g., academic, email, blog, casual)")
    audience: Optional[str] = Field("general", description="The target audience")
    strict: bool = Field(False, description="Whether to apply stricter scoring criteria")

    @field_validator('text')
    def check_word_count(cls, v):
        word_count = len(v.split())
        if word_count > 1000:
            raise ValueError(f"Text too long. Limit is 1000 words. (Submitted: {word_count})")
        return v

class ImproveRequest(BaseModel):
    text: str = Field(..., description="The text to improve")
    focus: List[str] = Field(..., description="List of areas to focus improvement on (e.g., clarity, grammar)")
    preserve_tone: bool = Field(True, description="Whether to preserve the original tone")

    @field_validator('text')
    def check_word_count(cls, v):
        word_count = len(v.split())
        if word_count > 1000:
            raise ValueError(f"Text too long. Limit is 1000 words. (Submitted: {word_count})")
        return v
