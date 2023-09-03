AOC_YEARS = [str(y) for y in range(2015, 2023)]
AOC_DAYS = range(1,26)

MARK_UNCOMPLETED = "  "
MARK_COMPLETED_P1 = "* "
MARK_COMPLETED_P2 = "**"


def print_table(data: dict):
    table_header = " | ".join(["Year", *[str(d) if d > 9 else f" {d}" for d in AOC_DAYS]])
    print(table_header)
    print(":---:|", ":--:|" * 25, sep="")

    for year,val in data.items():
        print(" | ".join([year, *val]))


def generate_completion_dict():
    completion_data = {year: [MARK_UNCOMPLETED for _ in AOC_DAYS] for year in AOC_YEARS}

    # year: list[completed days]
    # 0 indexed
    completed_p1 = {
        2021: [16]
    }

    # year: list[completed days]
    # 0 indexed
    completed_p2 = {
        2015: list(range(0, 8)),
        2016: list(range(0, 10)),
        2018: list(range(0, 7)),
        2019: list(range(0, 13)),
        2020: list(range(0, 18)),
        2021: list(range(0, 16)),
        2022: list(range(0, 11)),
    }

    for k, v in completed_p1.items():
        for i in v:
            completion_data[str(k)][i] = MARK_COMPLETED_P1
    
    for k, v in completed_p2.items():
        for i in v:
            completion_data[str(k)][i] = MARK_COMPLETED_P2

    return completion_data

if __name__ == '__main__':
    completion_data = generate_completion_dict()
    print_table(completion_data)
