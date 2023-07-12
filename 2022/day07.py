from typing import NamedTuple


ROOT = '/'


class File(NamedTuple):
    size: int
    name: str


class Folder(NamedTuple):
    name: str
    subfolders: set['Folder']
    files: set[File]
    totalsize: int


class FileSystem:
    def __init__(self, terminal_output):
        self.folders: dict[tuple, Folder] = {}
        self.map_file_system(terminal_output)


    def map_file_system(self, terminal_output: list[str]):
        current_path = [ROOT]
        self.register_folder(current_path)

        for line in terminal_output:
            if line[0].isnumeric():
                size, name = line.split()
                file = File(int(size), name)
                self.register_file(current_path, file)

            elif line == "$ cd /":
                current_path = [ROOT]

            elif line == "$ cd ..":
                current_path = current_path[:-1]
                if len(current_path) == 0:
                    current_path = [ROOT]

            elif line.startswith("$ cd "):
                subdir_name = line[5:]
                current_path.append(subdir_name)
                self.register_folder(current_path)

            elif line.startswith('dir'):
                dir_name = line[4:]
                dir_path = [*current_path, dir_name]
                self.register_folder(dir_path)


    def register_file(self, path, file: File):
        path = tuple(path)
        assert path in self.folders

        folder = self.folders[path]
        folder.files.add(file)


    def register_folder(self, path):
        path = tuple(path)
        if path in self.folders:
            return 
        
        path = tuple(path)
        folder = Folder(path[-1], set(), set(), -1)
        self.folders[path] = folder

        if len(path) > 1:
            parent_folder = self.folders[path[:-1]]
            parent_folder.subfolders.add(path)


    def get_dir_size(self, path):
        path = tuple(path)
        folder = self.folders[path]

        if folder.totalsize >=0:
            return folder.totalsize

        size_files = sum(f.size for f in folder.files)
        size_subdirs = sum(self.get_dir_size(d) for d in folder.subfolders)
        totalsize = size_files + size_subdirs

        updated_folder = Folder(folder.name, folder.subfolders, folder.files, totalsize)
        self.folders[path] = updated_folder
    
        return totalsize
    

    def find_folders_of_max_total_size(self, max_size=100_000):
        self.get_dir_size([ROOT])

        open_paths = {tuple(ROOT)}
        examined_paths = set()
        valid_paths = set()

        while open_paths:
            path = open_paths.pop()
            examined_paths.add(path)

            folder = self.folders[path]
            open_paths = (open_paths | folder.subfolders) - examined_paths

            if folder.totalsize <= max_size:
                valid_paths.add(path)

        return valid_paths



    def print_folders(self):
        for path, folder in self.folders.items():
            print(f'Folder name:\t{folder.name}')
            print(f'Full path: {path}')
            print(f'Total size: {folder.totalsize}')
            print('\tSubfolders:')
            for sub in folder.subfolders:
                print(f'\t\t{sub}')
            print('\tFiles:')
            for f in folder.files:
                print(f'\t\t{f}')



def read_input(filename: str = 'day07.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    return data


def part_one(puzzle_input):
    fs = FileSystem(puzzle_input)
    valid_paths = fs.find_folders_of_max_total_size()
    folders = [fs.folders[path] for path in valid_paths]
    total_size = sum(f.totalsize for f in folders)

    return total_size


def part_two(puzzle_input):
    pass


if __name__ == '__main__':
    # puzzle_input = read_input('day07ex1.txt')
    puzzle_input = read_input()


    print(f'Part one: {part_one(puzzle_input)}')
    # print(f'Part two: {part_two(puzzle_input)}')