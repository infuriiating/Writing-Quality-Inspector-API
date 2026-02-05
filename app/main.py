from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.routes import analyze, improve
from app.auth import get_api_key
from fastapi import Depends

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Writing Quality Inspector API",
    description="A strict, rubric-based writing quality evaluator.",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Protect routes with API Key
app.include_router(analyze.router, dependencies=[Depends(get_api_key)])
app.include_router(improve.router, dependencies=[Depends(get_api_key)])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Writing Quality Inspector"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
