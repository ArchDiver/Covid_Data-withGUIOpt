import datetime
from unittest.mock import MagicMock, patch
import pandas as pd
import sys

sys.path.append("./covid_no_GUI")
import covid_main


def test_api_url():
    base = "http://something.com/"
    item = covid_main.InputItem(iso_country="USA", date=datetime.date(2020, 4, 30))
    got = covid_main.api_url(base, item)
    assert got == "http://something.com/reports/total?date=2020-04-30&iso=USA"


@patch("requests.get")
def test_api_request(get_mock):
    item = covid_main.InputItem(iso_country="USA", date=datetime.date(2020, 4, 30))
    covid_main.api_request("base/", item)
    get_mock.assert_called_with("base/reports/total?date=2020-04-30&iso=USA")


def test_get_input_items():
	pass


def test_build_excel_dataframe():
	pass