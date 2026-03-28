from main import generate_txt, ExtractionResult, Header, PositionRow

def make_result() -> ExtractionResult:
    return ExtractionResult(
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
            PositionRow(col1=2, col2=1, col3=880, col4=1390, col5="0", col6="1", col7="1", col8="EG2", col9="0", col10="0"),
            PositionRow(col1=3, col2=1, col3=2510, col4=2310, col5="0", col6="1", col7="1", col8="EG4", col9="8", col10="0"),
            PositionRow(col1=4, col2=1, col3=855, col4=600, col5="1", col6="0", col7="1", col8="DG1", col9="Rolladenkasten", col10="180mm"),
        ],
    )


def test_header_row_format():
    result = make_result()
    txt = generate_txt(result)
    header_row = txt.splitlines()[0]
    assert header_row == (
        "Musterbau & Holztechnik GmbH|K2026-77195|0805260933|20.06.2026|WEISS|"
        "Standard|2500er|140 mm Hartschaum|hwf9016|IO|13"
    )


def test_position_row_count():
    result = make_result()
    txt = generate_txt(result)
    lines = txt.splitlines()
    assert len(lines) == 1 + len(result.positions)


def test_position_row_format():
    result = make_result()
    txt = generate_txt(result)
    second_line = txt.splitlines()[1]
    assert second_line == "1|2|880|1390|0|1|1|EG1|0|0"


def test_notkurbel_mapped():
    result = make_result()
    txt = generate_txt(result)
    notkurbel_row = txt.splitlines()[3]
    assert notkurbel_row.split("|")[8] == "8"


def test_rolladenkasten_mapped():
    result = make_result()
    txt = generate_txt(result)
    rolladenkasten_row = txt.splitlines()[4]
    fields = rolladenkasten_row.split("|")
    assert fields[8] == "Rolladenkasten"
    assert fields[9] == "180mm"