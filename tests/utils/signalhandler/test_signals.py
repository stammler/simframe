from simframe.utils.signalhandler import Signal


def test_template_signal_class():
    sig = Signal()
    sig._cleanup()
    assert not sig()