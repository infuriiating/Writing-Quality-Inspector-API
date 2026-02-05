# Writing Quality Inspector API

A high-performance, deterministic API for evaluating and improving writing quality. Built with **FastAPI**, **OpenAI**, and strict architectural patterns.

## 🚀 Features

- **Rubric-Based Evaluation**: Deterministic scoring (0-100) for Clarity, Coherence, Grammar, Originality, and Tone.
- **Strict Mode**: Enforces harsh penalties for vague or amateur writing.
- **AI-Powered Improvements**: Rewrites text to fix specific issues (e.g., "fix grammar but keep the tone") without hallucinations.
- **Production Ready**:
    - **Rate Limiting**: 1 request/minute per IP handling via `slowapi`.
    - **Security**: API Key authentication required for all endpoints.
    - **Validation**: Strict word count limits (1000 words) and Pydantic schema validation.

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **AI Engine**: OpenAI GPT-4o-mini (Temperature 0 for determinism)
- **Validation**: Pydantic v2
- **Rate Limiting**: Slowapi (Redis-ready)
- **Deployment**: Docker-ready

## 📦 Project Structure

```bash
├── app/
│   ├── routes/       # API endpoints (Analyze, Improve)
│   ├── services/     # Core logic (Evaluator, OpenAI Client)
│   ├── schemas/      # Pydantic models
│   ├── prompts/      # LLM System prompts
│   ├── main.py       # App entry point
│   ├── auth.py       # API Key security
│   └── config.py     # Env setup
└── requirements.txt  # Dependencies
```

## 🔐 Security

### Authentication
Requests must include the `x-api-key` header.

#### Python Example
```python
import requests

url = "http://127.0.0.1:8000/analyze"
headers = {"x-api-key": "YOUR_SECRET_KEY"}
payload = {
    "text": "The quick brown fox...",
    "purpose": "academic"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

#### Curl Example
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
     -H "x-api-key: YOUR_SECRET_KEY" \
     -H "Content-Type: application/json" \
     -d '{"text": "Sample text..."}'
```

### Limits
- **Rate Limit**: 1 request per minute per IP.
- **Payload Limit**: 1000 words max.
- **Bot Protection**: Automated bot detection heuristics included.

## 🚀 Getting Started

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/infuriiating/Writing-Quality-Inspector-API.git
    cd Writing-Quality-Inspector-API
    ```

2.  **Environment Setup**:
    Create a `.env` file:
    ```env
    OPENAI_API_KEY=sk-...
    API_SECRET=your-secret-key
    ```

3.  **Virtual Environment (Recommended)**:
    ```bash
    # Create venv
    python -m venv venv
    
    # Activate (Windows)
    .\venv\Scripts\activate
    
    # Activate (Mac/Linux)
    source venv/bin/activate
    ```

4.  **Run Locally**:
    ```bash
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    ```

4.  **Test**:
    Open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## 📊 Scoring Rubrics

The API evaluates text based on the following strict criteria (0-100 scale):

### Clarity
- **90-100**: Precise, concrete, no ambiguity.
- **70-89**: Mostly clear, minor vague phrasing.
- **50-69**: Understandable but unfocused.
- **<50**: Confusing or abstract.

### Coherence
- **90-100**: Seamless logical flow.
- **70-89**: Generally logical, weak transitions.
- **50-69**: Choppy narrative.
- **<50**: Disjointed/Random.

### Grammar
- **90-100**: Professional standard.
- **70-89**: Minor errors (commas, agreement).
- **50-69**: Distracting errors.
- **<50**: Riddled with errors.

### Originality
- **90-100**: Unique voice, avoids clichés.
- **70-89**: Solid but standard phrasing.
- **50-69**: Derivative/Generic.
- **<50**: Robotic or Plagiarized.

### Verbosity
*Note: Higher score = Perfect Conciseness.*
- **90-100**: Zero fluff.
- **70-89**: Generally concise.
- **50-69**: Wordy/Passive.
- **<50**: Bloated/Redundant.

### Tone Consistency
- **90-100**: Perfectly consistent.
- **70-89**: Mostly consistent.
- **50-69**: Fluctuates wildly.
- **<50**: Erratic/Inappropriate.

## 📄 License

MIT License.
