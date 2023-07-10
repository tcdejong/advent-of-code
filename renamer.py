"""
Add leading zeros to files in the solution folders 2015, 2016, ...
"""

DRY_RUN = False

from pathlib import Path

folders = [Path(str(year)) for year in range(2015,2022)]
folders = [folder for folder in folders if folder.exists()]

for folder in folders:
    for file in folder.iterdir():
        
        if not file.name.startswith("day"):
            continue

        if file.suffix != ".py":
            continue

        if len(file.name) >= len("day##.py"):
            continue

        day_number = file.name[3]
        new_filepath = file.parent / f'day0{day_number}.py'
        
        if DRY_RUN:
            print(folder, file.name, new_filepath)
            continue
        
        file.rename(new_filepath)
