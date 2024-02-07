from simframe import Frame
from simframe import writers


def test_simplenamespace_iter():
    f = Frame()
    f.writer = writers.namespacewriter()
    f.addfield("A", 0.)
    f.addfield("B", 1.)
    f.writeoutput(0)
    data = f.writer.read.all()
    for name, field in data:
        if name == "A":
            assert field == 0.
        if name == "B":
            assert field == 1.
