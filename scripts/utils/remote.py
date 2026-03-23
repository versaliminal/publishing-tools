import os
import urllib.request
from . import format

GSHEETS_URL_FMT = '{url}/gviz/tq?tqx=out:csv&sheet={sheet}'
TABLE_PATH_FMT = '{project_dir}/tables/{table}'


def refresh_sources(project_dir, config):
    """
    Refreshes local tables from sheets in Google Sheets.
    """
    try:
        os.mkdir(project_dir)
        os.mkdir(TABLE_PATH_FMT.format(""))
    except FileExistsError:
        pass
    if config.get('gsheets_url'):
        refresh_sources_from_gsheets(project_dir, config)


def refresh_sources_from_gsheets(project_dir, config):
    gsheets_url = config.get('gsheets_url')
    format.print_subheader("Refreshing sources from Google Sheets...")
    for entry in config['mappings']:
        url = GSHEETS_URL_FMT.format(url=gsheets_url, sheet=entry['sheet'])
        output = TABLE_PATH_FMT.format(
            project_dir=project_dir, table=entry['table'])
        try:
            urllib.request.urlretrieve(url, output)
            format.print_item_success(
                "Downloaded {0} sheet to {1}".format(entry['sheet'], output), indent=1)
        except Exception as e:
            format.print_item_failure(
                "Error downloading file: {0}".format(e), indent=1)
