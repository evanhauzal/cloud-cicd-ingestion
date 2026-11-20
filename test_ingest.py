from ingest import fetch_data

def test_fetch_data_returns_list():
    data = fetch_data()
    assert isinstance(data, list)
    assert len(data) > 0