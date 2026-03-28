# PDF Extractor

Extracts and maps data from roller shutter order PDFs using Gemini API.

## Run with Docker
```bash
docker pull iamuchihadaniel/pdf-extractor
docker run -e GEMINI_API_KEY=your_key -p 8000:8000 iamuchihadaniel/pdf-extractor
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