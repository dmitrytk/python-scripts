from proj import deg2dec, dec2deg
import pytest


def test_deg2dec():
    assert deg2dec('60 00 00') == '60.0'
    assert deg2dec('00 00 00') == '0.0'
    assert deg2dec('-180 00 00') == '-180.0'
    assert float(deg2dec('50 10 20.56')) == pytest.approx(50.172378, rel=1e-3)


def test_dec2deg():
    assert dec2deg(60.58) == '60 34 48.0'
    assert dec2deg(0) == '00 00 00.0'
    assert dec2deg(-60) == '-60 00 00.0'
