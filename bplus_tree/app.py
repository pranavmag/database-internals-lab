import streamlit as st

st.title("B+ Tree Visualizer")

graph = """
digraph {
    root [label="20 | 40"]
    left [label="5 | 10"]
    middle [label="20 | 30"]
    right [label="40 | 50"]

    root -> left
    root -> middle
    root -> right
}
"""

st.graphviz_chart(graph)