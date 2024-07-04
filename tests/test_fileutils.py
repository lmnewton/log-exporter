from app.utils.fileutils import parse_file


def test_readfile():
    lines = []
    for line in parse_file("tests/resources/test.testlog", 4):
        lines.append(str(line).strip())
    assert lines == ["0", "1 test", "21", "321"]


def test_readfile_limited():
    lines = []
    for line in parse_file("tests/resources/test.testlog", 3):
        lines.append(str(line).strip())
    assert lines == ["0", "1 test", "21"]


def test_emptyfile():
    lines = []
    for line in parse_file("tests/resources/empty.testlog", 1):
        lines.append(str(line).strip())
    assert len(lines) == 0


def test_bufferedread():
    lines = []
    for line in parse_file("tests/resources/buffered.testlog", 32):
        lines.append(str(line))
    assert len(lines) == 32

    for line in lines:
        assert line.startswith("2024-07-04 13:47:44")
