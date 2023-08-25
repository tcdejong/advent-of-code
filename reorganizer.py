"""
Add leading zeros to files in the solution folders 2015, 2016, ...
"""

import datetime as dt
from pathlib import Path
from typing import Iterable

def get_event_years():
    FIRST_YEAR = 2015
    
    now = dt.datetime.now()
    LAST_YEAR = now.year if now.month >= 11 else now.year - 1

    return range(FIRST_YEAR, LAST_YEAR + 1)


def create_folders(years: Iterable[int]):
    for year in years:
        year_folder = Path(str(year))
        if not year_folder.exists():
            year_folder.mkdir()
            print(f'Created folder for {year}')

        for day in range(1,26):
            day = str(day).zfill(2)
            day_folder = year_folder / f'day{day}'
            if not day_folder.exists():
                day_folder.mkdir()
                

def move_solutions_from_year_folders_to_day_folders():
    years = (str(y) for y in get_event_years())

    for year in years:
        p = Path(str(year))

        py_files = p.glob("*.py")
        for file in py_files:



# def renamer():
#     for folder in folders:
#         for file in folder.iterdir():
            
#             if not file.name.startswith("day"):
#                 continue

#             if file.suffix != ".py":
#                 continue

#             if len(file.name) >= len("day##.py"):
#                 continue

#             day_number = file.name[3]
#             new_filepath = file.parent / f'day0{day_number}.py'
            
#             file.rename(new_filepath)
