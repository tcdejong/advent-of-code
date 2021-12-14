from typing import Union


AOC_YEARS = [str(y) for y in range(2015, 2020)]
AOC_DAYS = range(1,26)

MODES = {
    "1": 'Single specific day',
    "2": 'Range of consecutive days',
    "3": 'All days, one by one',
    None: 'End input.'
}


def choose_mode() -> Union[int, None]:
    while True:
        # Ask user for year of entry
        print("Choose an input mode:")
        [print(f"    {key} - {val}") for key,val in MODES.items()]

        choice = input()

        if choice == "":
            return None

        if choice in MODES:
            return choice
        else:
            print(f"\nInvalid choice ({choice}), please try again.")
            continue

    

def choose_year() -> str:
    while True:
        # Ask user for year of entry
        print("Choose a year:")
        [print(f"    {year}") for year in AOC_YEARS]
        print("(Empty input to quit)")

        choice = input()

        if choice == "":
            break

        if choice in AOC_YEARS:
            return choice
        else:
            print(f"\nInvalid year ({choice}), please try again.")
            continue

    return ""


def enter_data(mode, current_data: list):
    assert mode in MODES
    assert mode != None
    assert len(current_data) == 25




def generate_completion_table(completion_dict: dict) -> str:
    pass
    # Verify input

    # Generate headers

    # Per key in dict, generate markdown table row displaying completion based on input


def generate_completion_dict() -> dict:
    "Function to generate a data structure containing the completion state"

    data = {year: ["--" for _ in AOC_DAYS] for year in AOC_YEARS}
    
    while True:
        print("Current data:")
        print_data(data)

        year = choose_year()

        if year:
            mode = choose_mode()
            enter_data(mode, data[year])

        else:
            choice = input("Enter more data? y/n:")
            if choice == "y":
                continue
            elif choice == "n":
                break
            else:
                "Unrecognized entry, try again"



    # Proces input, 
    # Ask for more input

    # Return dict
    return data




def make_table(data: dict):
    header = " | ".join(["&nbsp;", *[str(d) if d > 9 else f" {d}" for d in AOC_DAYS]])
    print(header)

    sep = "---:|" * 25
    print(sep)

    for year,val in data.items():
        print(" | ".join([year, *val]))


if __name__ == '__main__':
    # main()

    data = {year: ["--" for _ in AOC_DAYS] for year in AOC_YEARS}

    completed = {
        2015: list(range(0, 7)),
        2018: list(range(0, 7)),
        2019: list(range(0, 13)),
    }

    for k, v in completed.items():
        for i in v:
            data[str(k)][i] = "**"

    make_table(data)
