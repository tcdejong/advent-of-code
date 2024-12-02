"""
Miscellaneous shortlived helper functions to reorganize the files and folders in this directory.
"""

import datetime as dt
from pathlib import Path
import asyncio
import aiohttp
import aiofiles
import bs4

from lib import get_event_years, read_session_token, AOC_DAYS


def get_event_year_folders():
    return (Path(str(year)) for year in get_event_years())


def get_all_day_folders():
    for year in get_event_year_folders():
        year_folder = Path(str(year))
        if not year_folder.exists():
            continue

        for f in year_folder.iterdir():
            if f.is_dir and f.name.startswith('day'):
                yield f


def create_year_and_day_folders():
    for year in get_event_year_folders():
        year_folder = Path(str(year))
        if not year_folder.exists():
            year_folder.mkdir()
            print(f'Created folder for {year}')

        for day in AOC_DAYS:
            day = str(day).zfill(2)
            day_folder = year_folder / f'day{day}'
            if not day_folder.exists():
                day_folder.mkdir()
                

def remove_txt_files():
    year_folders = get_event_year_folders()
    
    for yf in year_folders:
        if not yf.exists():
            continue

        txt_files = yf.glob("*.txt")
        for f in txt_files:
            f.unlink()
            print(f.absolute())


# When using iPython there already is an event loop, so just await.
# Otherwise, import asyncio and use asyncio.run()
async def download_missing_inputs():
    tasks = [download_and_write_day_input(folder) for folder in get_all_day_folders()]

    for task in asyncio.as_completed(tasks):
        await task


async def download_and_write_day_input(day_folder: Path):
    session_token = read_session_token()

    if not session_token:
        raise ValueError('Failed to read session token!')

    async with aiohttp.ClientSession(cookies={'session': session_token}) as session:
        input_file = day_folder / 'input.txt'
        if input_file.exists():
            return

        url = get_input_url_from_day_folder_path(day_folder)
        if not isinstance(url, str):
            return
        
        async with session.get(url) as resp:
            data = await resp.read()
            data = data.decode()
            
            async with aiofiles.open(input_file, 'w+') as f:
                await f.write(data)

            print(f'Downloaded {day_folder.name}!')


def get_input_url_from_day_folder_path(day_folder: Path):
    day = int(day_folder.stem[3:])
    year = int(day_folder.parent.name)

    if dt.date(year,12,day) > dt.datetime.now().date():
        return

    return f'https://adventofcode.com/{year}/day/{day}/input'

