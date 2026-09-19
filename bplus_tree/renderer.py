from graphviz import Digraph

from bplus_tree.tree import BPlusTree, InternalNode, LeafNode


TreeNode = LeafNode | InternalNode


def render_tree(
    tree: BPlusTree,
    show_leaf_links: bool = True,
) -> Digraph:
    graph = Digraph("bplus_tree")

    graph.attr(
        rankdir="TB",
        bgcolor="transparent",
        ordering="out",
        center="true",
        margin="0",
        pad="0.25",
        nodesep="0.5",
        ranksep="0.8",
        splines="polyline",
        outputorder="edgesfirst",
    )

    graph.attr(
        "edge",
        color="#94a3b8",
        penwidth="1.4",
        arrowsize="0.7",
    )

    _render_subtree(graph, tree.root)

    if show_leaf_links:
        _render_leaf_links(graph, tree.root)

    return graph


def _render_subtree(
    graph: Digraph,
    node: TreeNode,
) -> None:
    current_id = _node_id(node)

    if isinstance(node, LeafNode):
        graph.node(
            current_id,
            label=_html_label(
                node,
                background="#0f766e",
                border="#2dd4bf",
            ),
            shape="plain",
        )
        return

    graph.node(
        current_id,
        label=_html_label(
            node,
            background="#1d4ed8",
            border="#60a5fa",
        ),
        shape="plain",
    )

    for child in node.children:
        _render_subtree(graph, child)

        graph.edge(
            current_id,
            _node_id(child),
        )


def _render_leaf_links(
    graph: Digraph,
    root: TreeNode,
) -> None:
    leaf = _leftmost_leaf(root)

    while leaf.next_leaf is not None:
        graph.edge(
            _node_id(leaf),
            _node_id(leaf.next_leaf),
            style="dashed",
            color="#f59e0b",
            penwidth="1.6",
            dir="both",
            arrowhead="vee",
            arrowtail="vee",
            weight="0",
            constraint="false",
        )

        leaf = leaf.next_leaf


def _leftmost_leaf(node: TreeNode) -> LeafNode:
    current = node

    while isinstance(current, InternalNode):
        current = current.children[0]

    return current


def _node_id(node: TreeNode) -> str:
    return f"node_{id(node)}"


def _html_label(
    node: TreeNode,
    background: str,
    border: str,
) -> str:
    values = [str(key) for key in node.keys]

    if not values:
        values = ["∅"]

    cells = "".join(
        (
            '<TD CELLPADDING="10">'
            f'<FONT FACE="DejaVu Sans" COLOR="white">{value}</FONT>'
            "</TD>"
        )
        for value in values
    )

    return (
        "<<TABLE "
        'BORDER="1" '
        'CELLBORDER="1" '
        'CELLSPACING="0" '
        f'COLOR="{border}" '
        f'BGCOLOR="{background}">'
        f"<TR>{cells}</TR>"
        "</TABLE>>"
    )