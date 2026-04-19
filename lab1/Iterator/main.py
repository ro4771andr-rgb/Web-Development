from abc import ABC, abstractmethod
from typing import List, Any

class Iterator(ABC):
    @abstractmethod
    def __next__(self) -> Any:
        pass

    @abstractmethod
    def has_next(self) -> bool:
        pass

class Aggregate(ABC):
    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass

class ListIterator(Iterator):
    def __init__(self, collection: List[Any]):
        self._collection = collection
        self._position = 0

    def __next__(self) -> Any:
        try:
            value = self._collection[self._position]
            self._position += 1
            return value
        except IndexError:
            raise StopIteration()

    def has_next(self) -> bool:
        return self._position < len(self._collection)

class WordsCollection(Aggregate):
    def __init__(self, collection: List[Any] = []):
        self._collection = collection

    def create_iterator(self) -> ListIterator:
        return ListIterator(self._collection)

    def add_item(self, item: Any):
        self._collection.append(item)

if __name__ == "__main__":
    collection = WordsCollection()
    collection.add_item("First")
    collection.add_item("Second")
    collection.add_item("Third")

    iterator = collection.create_iterator()

    while iterator.has_next():
        print(next(iterator))