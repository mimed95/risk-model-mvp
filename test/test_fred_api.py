# test/test_fred_api.py

import pytest
from fredapi import Fred

def test_fred_api():
    api_key = 'e6ff54b98580bf99e260753f23f56682'
    fred_client = Fred(api_key=api_key)

    # Test fetching a series
    series_id = 'UNRATE'
    try:
        data = fred_client.get_series(series_id)
        assert not data.empty, "The fetched data should not be empty."
    except Exception as e:
        pytest.fail(f"Failed to fetch series {series_id}: {e}")

    # Test fetching another series
    series_id = 'GDPC1'
    try:
        data = fred_client.get_series(series_id)
        assert not data.empty, "The fetched data should not be empty."
    except Exception as e:
        pytest.fail(f"Failed to fetch series {series_id}: {e}")

if __name__ == "__main__":
    pytest.main()