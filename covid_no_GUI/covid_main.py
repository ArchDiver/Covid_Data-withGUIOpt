import pandas as pd
import datetime
import os
import requests
from typing import NamedTuple
from pathvalidate import ValidationError, validate_filename, sanitize_filename
import yaml
from datetime import date
import sys
import logging as log
import click


class InputItem(NamedTuple):
    """
    A pair representing the input for a query against a country. Contains ISO code and
    date.
    """

    iso_country: str
    date: datetime.date


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
    output = pd.DataFrame(
        columns=["date", "iso", "num_confirmed", "num_deaths", "num_recovered"]
    )
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
        output = output.append(new_row, ignore_index=True)
    return output


@click.command()
@click.option(
    "--output", default="output.xlsx", help="Output filename", show_default=True
)
@click.option(
    "--config", default="config.yaml", help="Configuration file", show_default=True
)
@click.option("--log-to", default="covid_main.log", help="Log file", show_default=True)
def main(output, config, log_to):
    log.basicConfig(
        filename=log_to,
        level=log.DEBUG,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )

    try:
        validate_filename(output)
    except ValidationError:
        log.error("Invalid output file %s: %s")
        return -1

    try:
        validate_filename(config)
    except ValidationError:
        log.error("Invalid config file %s: %s")
        return -1

    api_url = "https://covid-api.com/api/"

    # brings in the yaml config file to get the path to the base_covid.xlsx file
    log.debug("Opening configuration file %s", config)
    with open(config) as fp:
        config2 = yaml.safe_load(fp)

    base_excel = config2["excel_path"]
    input_items = get_input_items(pd.read_excel(base_excel))

    try:
        output_df = build_excel_dataframe(api_url, input_items)
    except requests.HTTPError as e:
        log.exception("Failed to make API request")
        return -1

    output_df.to_excel(output)
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.exception("Unexpected error")