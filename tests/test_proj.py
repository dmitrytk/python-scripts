from proj import deg2dec, dec2deg
import pytest


params = [
    ('10 00 00.0', '10.0'),
    ('256 53 24.0', '256.89'),
    ('-180 35 24.0', '-180.59'),
    ('00 59 24.0', '0.99'),
    ('00 00 00.0', '0.0'),
]

reverse_params = [(row[1], row[0]) for row in params]


@pytest.mark.parametrize("test_input, expected", params)
def test_deg2dec_param(test_input, expected):
    assert deg2dec(test_input) == expected


@pytest.mark.parametrize("test_input, expected", reverse_params)
def test_dec2deg_params(test_input, expected):
    assert dec2deg(test_input) == expected
