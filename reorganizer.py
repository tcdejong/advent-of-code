"""
Miscellaneous shortlived helper functions to reorganize the files and folders in this directory.
"""

import datetime as dt
from pathlib import Path
from typing import Iterable

def get_event_years():
    FIRST_YEAR = 2015
    
    now = dt.datetime.now()
    LAST_YEAR = now.year if now.month >= 11 else now.year - 1

    return range(FIRST_YEAR, LAST_YEAR + 1)


def get_event_year_folder_paths():
    return (Path(str(year)) for year in get_event_years())


def get_all_day_folders():
    for year in get_event_year_folder_paths():
        year_folder = Path(str(year))

        for f in year_folder.iterdir():
            if f.is_dir and f.name.startswith('day'):
                yield f


def create_year_and_day_folders():
    for year in get_event_year_folder_paths():
        year_folder = Path(str(year))
        if not year_folder.exists():
            year_folder.mkdir()
            print(f'Created folder for {year}')

        for day in range(1,26):
            day = str(day).zfill(2)
            day_folder = year_folder / f'day{day}'
            if not day_folder.exists():
                day_folder.mkdir()
                

def remove_txt_files():
    year_folders = get_event_year_folder_paths()
    
    for yf in year_folders:
        if not yf.exists():
            continue

        txt_files = yf.glob("*.txt")
        for f in txt_files:
            f.unlink()
            print(f.absolute())


def download_inputs():
    ...
