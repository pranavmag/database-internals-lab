import random

import streamlit as st

from bplus_tree.renderer import render_tree
from bplus_tree.tree import BPlusTree, InternalNode, LeafNode


st.set_page_config(
    page_title="B+ Tree Visualizer",
    page_icon="🌳",
    layout="wide",
)


if "inserted_keys" not in st.session_state:
    st.session_state.inserted_keys = []


def build_tree(order: int, keys: list[int]) -> BPlusTree:
    tree = BPlusTree(order=order)

    for key in keys:
        tree.insert(key)

    return tree


def tree_height(tree: BPlusTree) -> int:
    height = 1
    current = tree.root

    while isinstance(current, InternalNode):
        height += 1
        current = current.children[0]

    return height


def count_nodes(node: LeafNode | InternalNode) -> int:
    if isinstance(node, LeafNode):
        return 1

    return 1 + sum(
        count_nodes(child)
        for child in node.children
    )


# Sidebar configuration

st.sidebar.header("Tree configuration")

order = st.sidebar.slider(
    "Order / maximum fanout",
    min_value=3,
    max_value=10,
    value=4,
    help=(
        "An order-m internal node can have at most m children "
        "and m-1 separator keys."
    ),
)

show_leaf_links = st.sidebar.toggle(
    "Show leaf links",
    value=True,
)

st.sidebar.caption(
    f"Maximum keys per node: {order - 1}"
)

st.sidebar.divider()


# Insert controls

st.sidebar.subheader("Insert a key")

with st.sidebar.form(
    "insert_form",
    clear_on_submit=True,
):
    inserted_value = st.number_input(
        "Integer key",
        value=0,
        step=1,
    )

    insert_submitted = st.form_submit_button(
        "Insert"
    )

if insert_submitted:
    key = int(inserted_value)

    if key in st.session_state.inserted_keys:
        st.sidebar.warning(
            f"Key {key} already exists."
        )
    else:
        st.session_state.inserted_keys.append(key)
        st.sidebar.success(
            f"Inserted key {key}."
        )


if st.sidebar.button("Insert random key"):
    existing_keys = set(
        st.session_state.inserted_keys
    )

    available_keys = [
        key
        for key in range(0, 1000)
        if key not in existing_keys
    ]

    if available_keys:
        random_key = random.choice(available_keys)
        st.session_state.inserted_keys.append(
            random_key
        )

        st.sidebar.success(
            f"Inserted random key {random_key}."
        )
    else:
        st.sidebar.warning(
            "No unused random keys remain."
        )


if st.sidebar.button("Reset tree"):
    st.session_state.inserted_keys.clear()
    st.sidebar.success("Tree reset.")


# The insertion history is the source of truth.
# Changing the order automatically rebuilds the tree.

tree = build_tree(
    order=order,
    keys=st.session_state.inserted_keys,
)


# Lookup controls

st.sidebar.divider()
st.sidebar.subheader("Lookup")

with st.sidebar.form("lookup_form"):
    lookup_value = st.number_input(
        "Search key",
        value=0,
        step=1,
        key="lookup_value",
    )

    lookup_submitted = st.form_submit_button(
        "Search"
    )

if lookup_submitted:
    lookup_key = int(lookup_value)

    if tree.search(lookup_key):
        st.sidebar.success(
            f"Key {lookup_key} was found."
        )
    else:
        st.sidebar.error(
            f"Key {lookup_key} was not found."
        )


# Insertion history

st.sidebar.divider()
st.sidebar.subheader("Insertion history")

if st.session_state.inserted_keys:
    history = ", ".join(
        str(key)
        for key in st.session_state.inserted_keys
    )

    st.sidebar.code(history)
else:
    st.sidebar.caption(
        "The tree is currently empty."
    )


# Main page

st.markdown(
    """
    <h1 style="text-align: center; margin-bottom: 0;">
        B+ Tree Visualizer
    </h1>

    <p style="
        text-align: center;
        color: #94a3b8;
        margin-top: 0.4rem;
        margin-bottom: 1.5rem;
    ">
        Blue nodes are internal routing nodes.
        Green nodes are linked leaf nodes.
    </p>
    """,
    unsafe_allow_html=True,
)


metric_left, metric_middle, metric_right = st.columns(3)

metric_left.metric(
    "Keys",
    len(st.session_state.inserted_keys),
)

metric_middle.metric(
    "Tree height",
    tree_height(tree),
)

metric_right.metric(
    "Nodes",
    count_nodes(tree.root),
)


left_space, graph_column, right_space = st.columns(
    [1, 12, 1]
)

with graph_column:
    graph = render_tree(
        tree,
        show_leaf_links=show_leaf_links,
    )

    st.graphviz_chart(
        graph,
        width="stretch",
    )