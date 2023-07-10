AOC_YEARS = [str(y) for y in range(2015, 2023)]
AOC_DAYS = range(1,26)


def print_table(data: dict):
    table_header = " | ".join(["Year ", *[str(d) if d > 9 else f" {d}" for d in AOC_DAYS]])
    print(table_header)
    print(":---:|" * 26)

    for year,val in data.items():
        print(" | ".join([year, *val]))


if __name__ == '__main__':
    completion_data = {year: ["--" for _ in AOC_DAYS] for year in AOC_YEARS}

    # year: list[completed days]
    # 0 indexed, off by one
    completed_p1_only = {
        2021: [16]
    }

    # year: list[completed days]
    # 0 indexed, off by one
    completed_p1p2 = {
        2015: list(range(0, 8)),
        2016: list(range(0, 10)),
        2018: list(range(0, 7)),
        2019: list(range(0, 13)),
        2020: list(range(0, 18)),
        2021: list(range(0, 16)),
    }

    for k, v in completed_p1p2.items():
        for i in v:
            completion_data[str(k)][i] = "**"

    for k, v in completed_p1_only.items():
        for i in v:
            completion_data[str(k)][i] = "*"

    print_table(completion_data)
