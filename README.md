# PDF Extractor

Extracts and maps data from roller shutter order PDFs using Gemini AI.

## Run with Docker
```bash
docker pull your-dockerhub-username/pdf-extractor
docker run -e GEMINI_API_KEY=your_key -p 8000:8000 your-dockerhub-username/pdf-extractor
```

Then open http://localhost:8000 in your browser.

## Run locally
```bash
uv sync
GEMINI_API_KEY=your_key uv run uvicorn main:app --reload
```

## Run tests
```bash
uv run pytest
```