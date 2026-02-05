import json
import os
import logging
from app.services.openai_client import openai_client
from app.schemas.request import AnalyzeRequest, ImproveRequest
from app.schemas.response import AnalyzeResponse, ImproveResponse
from fastapi import HTTPException
from pydantic import ValidationError

# Configure structured logging
logger = logging.getLogger(__name__)

SCORING_RUBRICS = """
# Scoring Rubrics

## Clarity (0-100)
- **90-100**: Precise, concrete, no ambiguity. Concepts are explained simply and directly.
- **70-89**: Mostly clear, but contains minor vague phrasing or unnecessary jaundice.
- **50-69**: Understandable but unfocused. Reader has to reread sentences to grasp meaning.
- **<50**: Confusing, abstract, or poorly structured. Meaning is lost.

## Coherence (0-100)
- **90-100**: Logical flow is seamless. Transitions between ideas are smooth and effective.
- **70-89**: Generally logical, but some transitions are abrupt or weak.
- **50-69**: Ideas are connected but the overall argument or narrative is choppy.
- **<50**: Disjointed. Sentences feel random or unrelated.

## Grammar (0-100)
- **90-100**: Flawless grammar, punctuation, and usage. Professional standard.
- **70-89**: A few minor errors (e.g., missing commas, slight agreement issues) but nothing distracting.
- **50-69**: Noticeable errors that interrupt the reading flow.
- **<50**: Riddled with errors. hard to read.

## Originality (0-100)
- **90-100**: Unique voice, fresh perspectives, and creative phrasing. Avoids clichés completely.
- **70-89**: Solid writing but relies on some common phrases or standard structures.
- **50-69**: Derivative. Heavily reliant on clichés and generic expressions.
- **<50**: Feels robotic, plagiarized, or entirely devoid of personality.

## Verbosity (0-100)
(Note: Higher score (90-100) means *perfect* conciseness, NOT high word count.)
- **90-100**: Every word serves a purpose. No fluff.
- **70-89**: Generally concise, but a few sentences could be tighter.
- **50-69**: Wordy. Uses "in order to" instead of "to", "make a decision" instead of "decide".
- **<50**: Bloated. Filled with filler words and redundancy.

## Tone Consistency (0-100)
- **90-100**: Perfectly maintains the intended tone (e.g., academic, professional) throughout.
- **70-89**: Mostly consistent, with one or two slips in formality.
- **50-69**: Fluctuates wildly (e.g., formal start, slang in middle).
- **<50**: tone is erratic or inappropriate for the context.
"""

class EvaluatorService:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # TODO: Move prompts to a database or external config for easier A/B testing
        self.prompts_dir = os.path.join(self.base_dir, "prompts")

    def _load_file(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Critical resource missing: {path}")
            raise FileNotFoundError(f"Required file not found: {path}")

    async def _clean_json(self, raw_text: str) -> str:
        """
        Strip markdown fencing from LLM response.
        """
        text = raw_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    async def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        # Load static resources
        sys_template = self._load_file(os.path.join(self.prompts_dir, "analyze.txt"))

        # Inject context
        system_prompt = sys_template.replace("{{purpose}}", request.purpose or "general") \
                                    .replace("{{audience}}", request.audience or "general") \
                                    .replace("{{strict}}", str(request.strict)) \
                                    .replace("{{rubrics}}", SCORING_RUBRICS)

        response_json = await openai_client.get_completion(
            system_prompt=system_prompt,
            user_content=request.text
        )

        try:
            cleaned_payload = await self._clean_json(response_json)
            analysis_result = json.loads(cleaned_payload)
            return AnalyzeResponse(**analysis_result)
        except (json.JSONDecodeError, ValueError, ValidationError) as e:
            logger.error(f"Analysis failed. Error: {str(e)} | Raw Output: {response_json[:200]}...")
            raise HTTPException(status_code=502, detail=f"Invalid JSON/Schema from AI: {str(e)}")

    async def improve(self, request: ImproveRequest) -> ImproveResponse:
        sys_template = self._load_file(os.path.join(self.prompts_dir, "improve.txt"))

        system_prompt = sys_template.replace("{{focus}}", ", ".join(request.focus)) \
                                    .replace("{{preserve_tone}}", str(request.preserve_tone))

        response_json = await openai_client.get_completion(
            system_prompt=system_prompt,
            user_content=request.text
        )

        try:
            cleaned_payload = await self._clean_json(response_json)
            improvement_result = json.loads(cleaned_payload)
            return ImproveResponse(**improvement_result)
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Improvement failed. Error: {str(e)} | Raw Output: {response_json[:200]}...")
            raise HTTPException(status_code=502, detail="Invalid JSON response from AI model.")

evaluator = EvaluatorService()
