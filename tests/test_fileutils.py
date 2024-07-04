from app.utils.fileutils import read_file

def test_readfile():
    lines = []
    for line in read_file("tests/resources/test.log", 4):
        lines.append(str(line).strip())
    assert(lines == ['0', '1 test','21','321'])

def test_readfile_limited():
    lines = []
    for line in read_file("tests/resources/test.log", 3):
        lines.append(str(line).strip())
    assert(lines == ['0', '1 test','21'])

def test_emptyfile():
    lines = []
    for line in read_file("tests/resources/empty.log", 1):
        lines.append(str(line).strip())
    assert(len(lines) == 0)