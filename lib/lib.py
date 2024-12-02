import aiohttp
import datetime as dt
from pathlib import Path

AOC_DAYS = range(1,26)

def aoc_session(*, session=None):
    if not session:
        session_token = read_session_token()

        if not session_token:
            raise ValueError('Failed to read session token!')
        
        session = aiohttp.ClientSession(cookies={'session': session_token})

    return session

def read_session_token():
    token_path = Path('.session_token')

    if not token_path.exists():
        return ask_session_token()

    with open('.session_token') as f:
        return f.read().strip()
    

def ask_session_token():
    token = input('Please provide session token:')
    token_path = Path('.session_token')

    with open(token_path, 'w+') as f:
        f.write(token)

    return token


def get_event_years():
    FIRST_YEAR = 2015
    now = dt.datetime.now()
    LAST_YEAR = now.year if now.month == 12 else now.year - 1
    return range(FIRST_YEAR, LAST_YEAR + 1)


async def profile_async(func, *args, **kwargs):
    import cProfile
    import pstats
    import datetime as dt

    with cProfile.Profile() as pr:
        await func(*args, **kwargs)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    
    timestamp = dt.datetime.now().isoformat().replace(':', '_')
    stats.dump_stats(filename=f'profile_async_{timestamp}.prof')