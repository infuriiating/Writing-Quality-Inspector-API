# Writing Quality Inspector - Python SDK

This is the official Python client for the Writing Quality Inspector API.

## Installation

1.  **Dependencies**:
    ```bash
    pip install requests
    ```
2.  **Usage**: Copy `client.py` into your project.

## Authentication

You must provide your `API_SECRET` when initializing the client.

```python
from client import WritingQualityClient

# Replace with your deployed URL and Secret Key
client = WritingQualityClient(
    base_url="https://your-app-name.onrender.com", 
    api_key="my-super-secret-key-123"
)

# Check connection
if client.check_health():
    print("Connected!")
```

## Methods

### `analyze(text, ...)`
Analyzes text quality. Returns `AnalyzeResponse`.

### `improve(text, ...)`
Improves text. Returns `ImproveResponse`.
