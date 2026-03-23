import os
import urllib.request

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
    print("  * Refreshing sources from Google Sheets...")
    for entry in config['mappings']:
        url = GSHEETS_URL_FMT.format(url=gsheets_url, sheet=entry['sheet'])
        output = TABLE_PATH_FMT.format(
            project_dir=project_dir, table=entry['table'])
        print(
            "    * Downloading {0} sheet to {1}".format(entry['sheet'], output))
        try:
            urllib.request.urlretrieve(url, output)
        except Exception as e:
            print("\t- Error downloading file:", e)
