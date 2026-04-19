from abc import ABC, abstractmethod

class FileSystemComponent(ABC):
    @abstractmethod
    def show_details(self, indent: int = 0) -> None:
        pass

    @abstractmethod
    def get_size(self) -> float:
        pass

class File(FileSystemComponent):
    def __init__(self, name: str, size: float):
        self.name = name
        self.size = size

    def show_details(self, indent: int = 0) -> None:
        print("  " * indent + f"File: {self.name} ({self.size} KB)")

    def get_size(self) -> float:
        return self.size

class Directory(FileSystemComponent):
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, component: FileSystemComponent):
        self.children.append(component)

    def remove(self, component: FileSystemComponent):
        self.children.remove(component)

    def show_details(self, indent: int = 0) -> None:
        print("  " * indent + f"Directory: {self.name} [Total Size: {self.get_size()} KB]")
        for child in self.children:
            child.show_details(indent + 1)

    def get_size(self) -> float:
        total = 0
        for child in self.children:
            total += child.get_size()
        return round(total, 2)

file1 = File("main.py", 12.5)
file2 = File("utils.py", 4.2)
file3 = File("config.json", 1.0)

root = Directory("Project_Root")
src = Directory("src")
    
src.add(file1)
src.add(file2)

root.add(src)
root.add(file3)

root.show_details()