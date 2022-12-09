from __future__ import annotations
from dataclasses import dataclass, field
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

    def sizes_less_100kb(self) -> List[int]:
        sizes = []
        size = self.size()
        if size <= 100_000:
            sizes.append(size)
        for subdir in self.subdirectories.values():
            sizes.extend(subdir.sizes_less_100kb())
        return sizes


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

sizes = root_directory.sizes_less_100kb()
print(sum(sizes))
