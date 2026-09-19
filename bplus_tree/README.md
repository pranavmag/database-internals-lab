# B+ Tree Visualizer

An interactive B+ tree lab built with Python, Streamlit, and Graphviz.

The goal is to explore B+ tree algorithms without implementing a storage layer, physical pages, or disk I/O.

## Features

* Configurable tree order/fanout
* Unique integer insertion
* Point lookup
* Leaf and internal-node splitting
* Recursive split propagation
* Doubly linked leaves
* Interactive Graphviz visualization
* Random insertion and tree reset

## Run

Install Graphviz and the Python dependencies:

```bash
sudo dnf install graphviz
python -m pip install -r bplus_tree/requirements.txt
```

Start the visualizer from the repository root:

```bash
python -m streamlit run bplus_tree/app.py
```

Run the tests:

```bash
python -m pytest
```

## Structure

```text
bplus_tree/
├── app.py
├── renderer.py
├── tree.py
├── requirements.txt
├── README.md
└── tests/
    └── test_tree.py
```

* `tree.py` — B+ tree nodes and algorithms
* `renderer.py` — Graphviz rendering
* `app.py` — Streamlit interface
* `tests/` — correctness tests

## Current Rules

An order-`m` internal node has at most `m` children and `m - 1` separator keys. Leaf nodes also hold at most `m - 1` keys.

Internal keys provide routing information, while search keys are stored in the linked leaves.

## Next Steps

* Deletion
* Redistribution and merging
* Root collapse
* Search-path highlighting
* Operation playback
