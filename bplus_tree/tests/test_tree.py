from bplus_tree.tree import BPlusTree


def test_insertion_keeps_keys_sorted() -> None:
    tree = BPlusTree(order=4)

    tree.insert(30)
    tree.insert(10)
    tree.insert(20)

    assert tree.root.keys == [10, 20, 30]
    assert not tree.root_has_overflowed()


def test_fourth_key_causes_overflow() -> None:
    tree = BPlusTree(order=4)

    for key in [30, 10, 40, 20]:
        tree.insert(key)

    assert tree.root.keys == [10, 20, 30, 40]
    assert tree.root_has_overflowed()


def test_duplicate_is_rejected() -> None:
    tree = BPlusTree(order=4)

    assert tree.insert(20)
    assert not tree.insert(20)
    assert tree.root.keys == [20]