from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, ExtractionResult, Header, PositionRow
import io

client = TestClient(app)

FAKE_RESULT = ExtractionResult(
    header=Header(
        col1="Musterbau & Holztechnik GmbH",
        col2="K2026-77195",
        col3="0805260933",
        col4="20.06.2026",
        col5="WEISS",
        col6="Standard",
        col7="2500er",
        col8="140 mm Hartschaum",
        col9="hwf9016",
        col10="IO",
        col11=13,
    ),
    positions=[
        PositionRow(col1=1, col2=2, col3=880, col4=1390, col5="0", col6="1", col7="1", col8="EG1", col9="0", col10="0"),
    ],
)


def test_extract_returns_expected_shape():
    with patch("main.extract_from_pdf", return_value=FAKE_RESULT):
        response = client.post(
            "/extract",
            files={"file": ("test.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
        )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "txt" in data
    assert "header" in data["result"]
    assert "positions" in data["result"]


def test_extract_txt_is_string():
    with patch("main.extract_from_pdf", return_value=FAKE_RESULT):
        response = client.post(
            "/extract",
            files={"file": ("test.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
        )
    assert isinstance(response.json()["txt"], str)


def test_extract_position_count():
    with patch("main.extract_from_pdf", return_value=FAKE_RESULT):
        response = client.post(
            "/extract",
            files={"file": ("test.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")},
        )
    positions = response.json()["result"]["positions"]
    assert len(positions) == len(FAKE_RESULT.positions)