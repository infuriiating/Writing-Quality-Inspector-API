import logging
from openai import AsyncOpenAI, APIError, APIConnectionError, RateLimitError
from app.config import OPENAI_API_KEY
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        self.client = None
        if OPENAI_API_KEY:
            self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        else:
            logger.warning("OPENAI_API_KEY is not set. Helper services will fail.")

    async def get_completion(self, system_prompt: str, user_content: str, temperature: float = 0.2, model: str = "gpt-4o-mini") -> str:
        """
        Fetch completion from OpenAI with standard error handling.
        """
        if not self.client:
             logger.error("Attempted to call OpenAI without API Key.")
             raise HTTPException(status_code=500, detail="Server configuration error.")

        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0,
                seed=42, # Ensure deterministic results
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content

        except RateLimitError:
            logger.error("OpenAI Rate Limit Exceeded")
            raise HTTPException(status_code=503, detail="Service unavailable (Rate Limit).")
        except APIConnectionError:
            logger.error("OpenAI Connection Error")
            raise HTTPException(status_code=503, detail="Upstream connection failed.")
        except APIError as e:
            logger.error(f"OpenAI API Error: {str(e)}")
            raise HTTPException(status_code=502, detail="Upstream service error.")
        except Exception as e:
            logger.critical(f"Unexpected Error in OpenAI Client: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error.")

openai_client = OpenAIClient()
