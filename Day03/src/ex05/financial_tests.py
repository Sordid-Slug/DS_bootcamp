import pytest
from financil import Financial

def test_total_revenue():
    financial = Financial("MSFT", "Total Revenue")
    data = financial.get_financial_data()

    assert data[0] == 'Total Revenue'
    assert len(data[1]) > 0


def test_return_type():
    financial = Financial("MSFT", "Total Revenue")
    data = financial.get_financial_data()

    assert isinstance(data, tuple), "Return type is not tuple"


def test_invalid_ticker():
    with pytest.raises(Exception):
        financial = Financial("INVALID_TICKER", "Total Revenue")
        data = financial.get_financial_data()
