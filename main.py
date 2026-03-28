import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from google import genai
from google.genai import types
from pydantic import BaseModel

# ── Models ────────────────────────────────────────────────────────────────────

load_dotenv()


class Header(BaseModel):
	col1: str
	col2: str
	col3: str
	col4: str
	col5: str
	col6: str
	col7: str
	col8: str
	col9: str
	col10: str
	col11: int


class PositionRow(BaseModel):
	col1: int  # Line number
	col2: int  # Stück
	col3: int  # Breite
	col4: int  # Höhe
	col5: str  # L flag
	col6: str  # R flag
	col7: str  # Antrieb
	col8: str  # POS
	col9: str  # Bemerkung
	col10: str  # Bemerkung number


class ExtractionResult(BaseModel):
	header: Header
	positions: list[PositionRow]


# ── Gemini

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

MAPPING_PROMPT = """
Extract data from this PDF and map it according to these rules:

HEADER (one row per document):
- col1: Lieferanschrift company name
- col2: Kamsttoflesster für BV value
- col3: The number next to the big "Roll" heading
- col4: Date under Liefertermin
- col5: Rolladen value → "Aluminium Silber" = SILBER | \
	"Aluminium Anthrazit" = ANTHRAZIT | "Aluminium Weiß" = WEISS
- col6: Konstruktion type only (e.g. Erhöht, Standard)
- col7: Konstruktion wall number only (e.g. 2750er)
- col8: Aussenschürze value (e.g. 140 mm Hartschaum)
- col9: Endleiste → ends with 9006 = hwf9006 | ends with 7016 = hwf7016 | ends with 9016 = hwf9016
- col10: Antrieb → contains SMI = SMI | contains IO = IO
- col11: Total Stück (Gesamt number at bottom)

POSITIONS (one row per table entry):
- col1: Running line number starting at 1
- col2: Stück value
- col3: Breite value
- col4: Höhe value
- col5: L column contains L = "1" else "0"
- col6: R column contains R = "1" else "0"
- col7: Antrieb cell contains Elektro AND header \
	  Antrieb contains IO = "1" | contains Elektro AND header contains SMI = "2" | else "0"
- col8: POS value (e.g. EG1, DG4)
- col9: Bemerkung → contains Notkurbel = "8" | contains Rolladenkasten = "Rolladenkasten" | else "0"
- col10: Bemerkung number (e.g. 180mm) else "0"
"""


def extract_from_pdf(pdf_bytes: bytes) -> ExtractionResult:
	response = client.models.generate_content(
		model='gemini-2.5-flash-lite',
		contents=[
			types.Part.from_text(text=MAPPING_PROMPT),
			types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf'),
		],
		config=types.GenerateContentConfig(
			response_mime_type='application/json',
			response_schema=ExtractionResult,
		),
	)
	return ExtractionResult.model_validate_json(response.text)


# ── TXT ───────────────────────────────────────────────────────────────────────


def generate_txt(result: ExtractionResult) -> str:
	h = result.header
	header_row = (
		f'{h.col1}|{h.col2}|{h.col3}|{h.col4}|{h.col5}|'
		f'{h.col6}|{h.col7}|{h.col8}|{h.col9}|{h.col10}|{h.col11}'
	)
	position_rows = [
		f'{p.col1}|{p.col2}|{p.col3}|{p.col4}|{p.col5}|{p.col6}|{p.col7}|{p.col8}|{p.col9}|{p.col10}'
		for p in result.positions
	]
	return '\n'.join([header_row] + position_rows)


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post('/extract')
async def extract(file: UploadFile = File(...)):  # noqa: B008
	pdf_bytes = await file.read()
	result = extract_from_pdf(pdf_bytes)
	return {'result': result, 'txt': generate_txt(result)}
