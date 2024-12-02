MARK_UNCOMPLETED = "  "
MARK_COMPLETED_P1 = "* "
MARK_COMPLETED_P2 = "**"

COMPLETION_MARKS = {
    0: MARK_UNCOMPLETED,
    1: MARK_COMPLETED_P1,
    2: MARK_COMPLETED_P2,
}

AoCYear = int
AoCDay = int
NumStars = int
ProgressDict = dict[tuple[AoCYear, AoCDay], NumStars]

from lib import AOC_DAYS, aoc_session, get_event_years
import aiohttp
import asyncio
import bs4


async def request_progress_html(session: aiohttp.ClientSession, year: AoCYear):
    url = f'https://adventofcode.com/{year}'

    async with session.get(url) as resp:
        data = await resp.read()
        html = data.decode()

    return html, year # returning year because the async requests might be returned out of order


def parse_progress_html(html: str, year: AoCYear):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    num_stars: ProgressDict = {}
  
    assert soup.pre 
    for day_a in soup.pre.find_all('a'):
        day_classes = day_a['class']
        day_num = int(day_classes[0].lstrip('calendar-day'))
        
        day_stars = 0
        if 'calendar-complete' in day_classes:
            day_stars = 1
        elif 'calendar-verycomplete' in day_classes:
            day_stars = 2
        
        num_stars[(year, day_num)] = day_stars

    return num_stars


def print_table(num_stars: ProgressDict):
    """
    Print input dictionary as a markdown-formatted table and print it.
    The dictionary must have tuples of (year, day) as keys, and number of stars as values. 
    """
    table_header = " | ".join(["Year", *[str(d) if d > 9 else f" {d}" for d in AOC_DAYS]])
    print(table_header)
    print(":---:|", ":--:|" * 25, sep="")

    years = set(key[0] for key in num_stars.keys())

    for year in sorted(years):
        progress = [COMPLETION_MARKS[num_stars[(year, day)]] for day in AOC_DAYS]
        print(" | ".join([str(year), *progress]))


async def pipeline_completion_table(years=get_event_years()):
    num_stars: ProgressDict = {}

    async with aoc_session() as session:
        download_html_tasks = [request_progress_html(session, year) for year in years]
        
        for task in asyncio.as_completed(download_html_tasks):
            html, year = await task
            year_stars = parse_progress_html(html, year)
            num_stars |= year_stars

    print_table(num_stars)


if __name__ == '__main__':
    pass