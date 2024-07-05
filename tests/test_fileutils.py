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
        lines.append(str(line).strip())
    assert len(lines) == 32

    for line in lines:
        assert line.startswith("2024-07-04 13:47:44")


def test_bufferedsearch():
    lines = []
    for line in parse_file("tests/resources/buffered.testlog", 1000, "QB"):
        lines.append(str(line).strip())

    assert len(lines) == 2


def test_limitedbufferedsearch():
    lines = []
    for line in parse_file("tests/resources/buffered.testlog", 1, "QB"):
        lines.append(str(line).strip())

    assert len(lines) == 1


def test_bufferedsinglehitsearch():
    lines = []
    for line in parse_file("tests/resources/buffered.testlog", 1000, "TR"):
        lines.append(str(line).strip())

    assert len(lines) == 1

    for line in lines:
        assert line.startswith("2024-07-04 13:47:44")


def test_bufferednohitsearch():
    lines = []
    for line in parse_file("tests/resources/buffered.testlog", 1000, "MKM"):
        lines.append(str(line))

    assert len(lines) == 0

    for line in lines:
        assert line.startswith("2024-07-04 13:47:44")


def test_nobuffersearch():
    lines = []
    for line in parse_file("tests/resources/test.testlog", 1000, "1"):
        lines.append(str(line).strip())

    assert len(lines) == 3
    assert lines == ["1 test", "21", "321"]


def test_limitednobuffersearch():
    lines = []
    for line in parse_file("tests/resources/test.testlog", 2, "1"):
        lines.append(str(line).strip())

    assert len(lines) == 2
    assert lines == ["1 test", "21"]


def test_crossbuffersearch():
    lines = []
    for line in parse_file("tests/resources/buffered.testlog", 50, "C"):
        lines.append(str(line).strip())

    assert len(lines) == 23
    for line in lines:
        assert line.startswith("2024-07-04 13:47:44")
