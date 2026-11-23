"""
Tests for parameter tables.
As data is added, update the expected counts.
"""


def test_modeled_parameters(db):
    t = db.query(db.ModeledParameters.c.parameter).astropy()
    n_parameters = 0
    assert (
        len(t) == n_parameters
    ), f"Found {len(t)} entries in ModeledParameters, expected {n_parameters}"
