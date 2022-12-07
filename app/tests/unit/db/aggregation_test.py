import pytest
from app.db import aggregation


@pytest.mark.parametrize(
    'region_slug,expected',
    [
        ('uk_sub', ['GBIMM', 'GBGRK', 'GBSSH', 'GBTHP', 'GBGOO', 'GBBRS', 'GBLIV', 'GBGRG', 'GBLGP', 'GBBEL', 'GBHUL', 'GBMNC', 'GBTEE', 'GBLTP', 'GBLON', 'GBTIL', 'GBPME']),
        ('china_main', ['CNYAT', 'CNNBO', 'CNSGH', 'CNQIN', 'CNLYG', 'CNXAM', 'CNCWN', 'CNSNZ', 'CNSHK', 'HKHKG', 'CNHDG', 'CNGGZ', 'CNYTN', 'CNDAL', 'CNTXG']),
        ('does_not_exists', []),
    ],
)
def test_get_ports(region_slug: str, expected: list[str]):
    result = aggregation.get_ports(region_slug)

    result.sort()
    expected.sort()

    assert result == expected
