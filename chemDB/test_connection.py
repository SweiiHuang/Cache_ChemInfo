import requests
import pytest

urls = [
    "https://flora2.epa.gov.tw/ToxicC/Query/database.aspx",
    "https://flora2.epa.gov.tw/MainSite/Lin/database2.aspx#gsc.tab=0",
    "https://prochem.osha.gov.tw/content/info/DownloadList.aspx?Classify=2",
    "https://prochem.osha.gov.tw/content/info/DownloadList.aspx?Classify=3",
    "https://echa.europa.eu/candidate-list-table"
]

@pytest.mark.parametrize("url", urls)
def test_connection(url):
    response = requests.get(url)
    assert response.status_code == 200

