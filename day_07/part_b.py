from __future__ import annotations
from dataclasses import dataclass, field
from itertools import chain
from typing import Dict, List
import sys


@dataclass
class File:
    filename: str
    size: int


@dataclass
class Directory:
    parent_directory: Directory
    subdirectories: Dict[str, Directory] = field(default_factory=dict)
    files: List[File] = None

    def size(self) -> int:
        return sum([file.size for file in self.files]) + sum([subdir.size() for subdir in self.subdirectories.values()])

    def all_directories(self) -> List[Directory]:
        return [self] + list(chain.from_iterable([subdir.all_directories() for subdir in self.subdirectories.values()]))


root_directory = Directory(parent_directory=None)
current_directory = root_directory


line = sys.stdin.readline().strip('\n')
while line:
    if line.startswith('$ cd '):
        _prompt, _cd, directory_name = line.split(' ')
        if directory_name == '/':
            current_directory = root_directory
        elif directory_name == '..':
            current_directory = current_directory.parent_directory
        else:
            if directory_name in current_directory.subdirectories.keys():
                current_directory = current_directory.subdirectories[directory_name]
            else:
                new_directory = Directory(parent_directory=current_directory)
                current_directory.subdirectories[directory_name] = new_directory
                current_directory = new_directory
        line = sys.stdin.readline().strip('\n')
    elif line == '$ ls':
        line = sys.stdin.readline().strip('\n')
        files = []
        while line and not line.startswith('$ '):
            size, name = line.split(' ')
            # Ignore directories, we will have to cd into them to learn anything about them
            if size != 'dir':
                files.append(File(filename=name, size=int(size)))
            line = sys.stdin.readline().strip('\n')
        current_directory.files = files
    else:
        raise Exception(f"Unexpected input {line}")

file_system_size = 70_000_000
used_space_size = root_directory.size()
free_space_size = file_system_size - used_space_size
required_update_free_size = 30_000_000
required_delete_size = required_update_free_size - free_space_size
all_directories = root_directory.all_directories()
sizes = [directory.size() for directory in all_directories]
big_enough = [size for size in sizes if size >= required_delete_size]
print(min(big_enough))
