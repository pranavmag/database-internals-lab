from __future__ import annotations

from bisect import bisect_left

class LeafNode:
    def __init__(self) -> None:
        self.keys: list[int] = []
        self.next_leaf: LeafNode | None = None

class BPlusTree:
    def __init__(self, order: int) -> None:
        if order < 3:
            raise ValueError("B+ tree order must be at least 3")

        self.order = order
        self.root = LeafNode()

    @property
    def max_keys(self) -> int:
        return self.order - 1

    def search(self, key: int) -> bool:
        index = bisect_left(self.root.keys, key)

        return (
            index < len(self.root.keys)
            and self.root.keys[index] == key
        )

    def insert(self, key: int) -> bool:
        index = bisect_left(self.root.keys, key)

        if index < len(self.root.keys) and self.root.keys[index] == key:
            return False

        self.root.keys.insert(index, key)
        return True

    def root_has_overflowed(self) -> bool:
        return len(self.root.keys) > self.max_keys