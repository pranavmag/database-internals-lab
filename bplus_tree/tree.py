from __future__ import annotations

from bisect import bisect_left, bisect_right

class LeafNode:
    def __init__(self) -> None:
        self.keys: list[int] = []
        self.next_leaf: LeafNode | None = None
        self.previous_leaf: LeafNode | None = None
        self.parent: InternalNode | None = None

class InternalNode:
    def __init__(self) -> None:
        self.keys: list[int] = []
        self.children: list[LeafNode | InternalNode] = []
        self.parent: InternalNode | None = None

class BPlusTree:
    def __init__(self, order: int) -> None:
        if order < 3:
            raise ValueError("B+ tree order must be at least 3")

        self.order = order
        self.root: LeafNode | InternalNode = LeafNode()

    @property
    def max_keys(self) -> int:
        return self.order - 1

    def search(self, key: int) -> bool:
        leaf = self._find_leaf(key)
        index = bisect_left(leaf.keys, key)

        return index < len(leaf.keys) and leaf.keys[index] == key

    def insert(self, key: int) -> bool:
        leaf = self._find_leaf(key)
        index = bisect_left(leaf.keys, key)

        if index < len(leaf.keys) and leaf.keys[index] == key:
            return False

        leaf.keys.insert(index, key)

        if len(leaf.keys) > self.max_keys:
            if leaf is self.root:
                self._split_root_leaf(leaf)
            else:
                self._split_non_root_leaf(leaf)

        return True

    def root_has_overflowed(self) -> bool:
        return len(self.root.keys) > self.max_keys

    def _find_leaf(self, key: int) -> LeafNode:
        current = self.root

        while isinstance(current, InternalNode):
            child_index = bisect_right(current.keys, key)
            current = current.children[child_index]

        return current

    def _split_root_leaf(self, leaf: LeafNode) -> None:
        split_index = len(leaf.keys) // 2

        right_leaf = LeafNode()
        right_leaf.keys = leaf.keys[split_index:]

        leaf.keys = leaf.keys[:split_index]

        right_leaf.next_leaf = leaf.next_leaf
        right_leaf.previous_leaf = leaf

        leaf.next_leaf = right_leaf

        new_root = InternalNode()
        new_root.keys = [right_leaf.keys[0]]
        new_root.children = [leaf, right_leaf]

        leaf.parent = new_root
        right_leaf.parent = new_root

        self.root = new_root

    def _split_non_root_leaf(self, leaf: LeafNode) -> None:
        parent = leaf.parent
        assert parent is not None

        split_index = len(leaf.keys) // 2

        right_leaf = LeafNode()
        right_leaf.keys = leaf.keys[split_index:]
        leaf.keys = leaf.keys[:split_index]

        old_next = leaf.next_leaf

        right_leaf.next_leaf = old_next
        right_leaf.previous_leaf = leaf

        leaf.next_leaf = right_leaf

        if old_next is not None:
            old_next.previous_leaf = right_leaf

        right_leaf.parent = parent

        leaf_index = parent.children.index(leaf)
        separator = right_leaf.keys[0]

        parent.keys.insert(leaf_index, separator)
        parent.children.insert(leaf_index + 1, right_leaf)

        if len(parent.keys) > self.max_keys:
            self._split_internal(parent)

    def _split_internal(self, internal: InternalNode) -> None:
        parent = internal.parent

        if parent is None:
            parent = InternalNode()
            parent.children = [internal]

            internal.parent = parent
            self.root = parent

        split_index = len(internal.keys) // 2

        promoted_key = internal.keys[split_index]

        right_internal = InternalNode()

        right_internal.keys = internal.keys[split_index + 1:]
        internal.keys = internal.keys[:split_index]

        right_internal.children = internal.children[split_index + 1:]
        internal.children = internal.children[:split_index + 1]

        for child in right_internal.children:
            child.parent = right_internal

        right_internal.parent = parent

        internal_index = parent.children.index(internal)

        parent.keys.insert(internal_index, promoted_key)
        parent.children.insert(internal_index + 1, right_internal)

        if len(parent.keys) > self.max_keys:
            self._split_internal(parent)

