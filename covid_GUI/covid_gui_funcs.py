import pandas as pd
import tkinter as tk
import os
import requests
import sys
from pathvalidate import ValidationError, validate_filename, sanitize_filename
import datetime
from typing import NamedTuple


CWD = os.getcwd()

import logging as log

log.basicConfig(
    filename="covid_gui.log",
    level=log.DEBUG,
    format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s",
)



class InputItem(NamedTuple):
    """
    A pair representing the input for a query against a country. Contains ISO code and
    date.
    """

    iso_country: str
    date: datetime.date


# def get_filepath(input_name=(CWD + "covid_base.xlsx")):
#     fp = input_name
#     return fp


def api_url(base_url, input_item):
    """
    Constructs the URL to retrieve data for the given country and date
    """
    return (
        f"{base_url}reports/total?date={input_item.date}&iso={input_item.iso_country}"
    )


def api_request(base_url, input_item):
    """
    Perform an API request for a single input item. Returns the JSON response, or raises
    an HTTPError if the call failed.
    """
    log.info("Making request for %s", input_item)
    response = requests.get(api_url(base_url, input_item))
    response.raise_for_status()
    return response.json()


def get_input_items(input_excel_dataframe):
    """
    Given a dataframe representing the input dataframe, return a list of (country_iso, date)
    pairs.
    """
    return [
        InputItem(
            iso_country=input_excel_dataframe["iso"].iloc[i],
            date=input_excel_dataframe["date"].iloc[i].date(),
        )
        for i in input_excel_dataframe.index
    ]


def build_excel_dataframe(base_url, input_items):
    """
    Builds the output excel dataframe by calling the API against each of the input
    items
    """
    df_new = pd.DataFrame(
        columns=["date", "iso", "num_confirmed", "num_deaths", "num_recovered"]
    )

    # This part of the function goes through rows of the excel file and request the specific date for each pair and adds it to the new dataframe
    for item in input_items:
        js = api_request(base_url, item)
        data = js["data"]
        new_row = {
            "date": item.date,
            "iso": item.iso_country,
            "num_confirmed": data["confirmed"],
            "num_deaths": data["deaths"],
            "num_recovered": data["recovered"],
        }
        df_new = df_new.append(new_row, ignore_index=True)
    return df_new


def save_excel(df_save, save_name):
    out_path = f"{CWD}\\OUTPUT\\{save_name}.xlsx"
    df_save.to_excel(out_path)
