from bplus_tree.tree import BPlusTree, InternalNode, LeafNode


def test_insertion_keeps_keys_sorted() -> None:
    tree = BPlusTree(order=4)

    tree.insert(30)
    tree.insert(10)
    tree.insert(20)

    assert tree.root.keys == [10, 20, 30]
    assert not tree.root_has_overflowed()

def test_root_leaf_split() -> None:
    tree = BPlusTree(order=4)

    for key in [30, 10, 40, 20]:
        tree.insert(key)

    assert isinstance(tree.root, InternalNode)
    assert tree.root.keys == [30]
    assert len(tree.root.children) == 2

    left = tree.root.children[0]
    right = tree.root.children[1]

    assert isinstance(left, LeafNode)
    assert isinstance(right, LeafNode)

    assert left.keys == [10, 20]
    assert right.keys == [30, 40]
    assert left.next_leaf is right
    assert right.next_leaf is None

    assert left.previous_leaf is None
    assert left.next_leaf is right

    assert right.previous_leaf is left
    assert right.next_leaf is None

def test_duplicate_is_rejected() -> None:
    tree = BPlusTree(order=4)

    assert tree.insert(20)
    assert not tree.insert(20)
    assert tree.root.keys == [20]

def test_search_after_root_split() -> None:
    tree = BPlusTree(order=4)

    for key in [30, 10, 40, 20]:
        tree.insert(key)

    assert tree.search(10)
    assert tree.search(30)
    assert tree.search(40)
    assert not tree.search(25)

def test_non_root_leaf_split() -> None:
    tree = BPlusTree(order=4)

    for key in [30, 10, 40, 20, 50, 60]:
        tree.insert(key)

    assert isinstance(tree.root, InternalNode)
    assert tree.root.keys == [30, 50]

    left, middle, right = tree.root.children

    assert isinstance(left, LeafNode)
    assert isinstance(middle, LeafNode)
    assert isinstance(right, LeafNode)

    assert left.keys == [10, 20]
    assert middle.keys == [30, 40]
    assert right.keys == [50, 60]

    assert left.next_leaf is middle
    assert middle.previous_leaf is left

    assert middle.next_leaf is right
    assert right.previous_leaf is middle

    assert left.previous_leaf is None
    assert right.next_leaf is None

    assert left.parent is tree.root
    assert middle.parent is tree.root
    assert right.parent is tree.root

def test_internal_root_split() -> None:
    tree = BPlusTree(order=4)

    for key in range(10, 101, 10):
        tree.insert(key)

    assert isinstance(tree.root, InternalNode)
    assert tree.root.keys == [70]
    assert len(tree.root.children) == 2

    left = tree.root.children[0]
    right = tree.root.children[1]

    assert isinstance(left, InternalNode)
    assert isinstance(right, InternalNode)

    assert left.keys == [30, 50]
    assert right.keys == [90]

    assert left.parent is tree.root
    assert right.parent is tree.root

def test_search_after_internal_split() -> None:
    tree = BPlusTree(order=4)

    keys = list(range(10, 101, 10))

    for key in keys:
        tree.insert(key)

    for key in keys:
        assert tree.search(key)

    assert not tree.search(55)