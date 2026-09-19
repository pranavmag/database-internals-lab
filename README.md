# Database Internals Labs

A collection of small, focused experiments for exploring how database systems work internally.

This repository is intentionally **not one integrated database management system**. Each lab isolates a particular database concept so that its algorithms, invariants, and tradeoffs can be studied without first building an entire storage engine around it.

The labs complement my larger C++ database engine project. The C++ project emphasizes systems concerns such as storage, memory management, concurrency, and correctness. These Python labs provide a faster playground for investigating individual database techniques and visualizing how they behave.

## Labs

| Lab | Focus | Status |
| --- | --- | --- |
| [B+ Tree Visualizer](./bplus_tree/) | Search, insertion, node splitting, leaf links, and interactive tree visualization | In progress |
| Slotted Page | Variable-length records inside fixed-size database pages | Planned |
| External Merge Sort | Sorting data under a restricted memory budget | Planned |
| Volcano Executor | Composable query operators using `open`, `get_next`, and `close` | Planned |
| Join Algorithms | Nested-loop, hash, and merge join behavior | Planned |
| Join Optimizer | Join ordering, cardinality estimation, and plan cost comparison | Planned |
| Concurrency Control | Locks, transaction schedules, and deadlock detection | Planned |
| Write-Ahead Logging | Logging, simulated crashes, redo, and undo | Planned |

## Philosophy

Each lab should answer one clear question and deliberately omit unrelated machinery. For example, the query executor may operate on in-memory Python rows instead of reading binary heap pages. That simplification keeps the experiment centered on execution rather than storage.

Every lab should aim to include:

- a small, readable implementation
- tests for its important invariants
- a demonstration or visualization
- a README explaining the modeled problem

Some labs may eventually be combined in separate integration experiments, but reuse between them is not a requirement.

## Running a Lab

Each lab contains its own setup and usage instructions. In general, clone the repository, enter the desired lab directory, install its dependencies, and follow that lab's README.

## What This Repository Is For

The goal is not to reproduce a production database in Python. It is to develop a deeper understanding of database internals by building small models, observing their behavior, testing their invariants, and recording the reasoning behind their design.

Topics of particular interest include:

- storage layouts and indexing;
- query execution and optimization;
- memory-aware algorithms;
- transaction processing and concurrency; and
- logging and crash recovery.

Each lab is a focused investigation into one part of that larger system.
