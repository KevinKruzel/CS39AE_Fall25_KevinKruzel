import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities

st.set_page_config(page_title="Network Analysis Demo", page_icon="🕸️", layout="wide")

st.title("Network Visualization and Analysis Assignment")

data = [
    ("Alice", "Bob",),
    ("Alice", "Charlie",),
    ("Bob", "Charlie",),
    ("Charlie", "Diana",),
    ("Diana", "Eve",),
    ("Bob", "Diana",),
    ("Frank", "Eve",),
    ("Eve", "Ian",),
    ("Diana", "Ian"),
    ("Ian", "Grace"),
    ("Grace", "Hannah"),
    ("Hannah", "Jack"),
    ("Grace", "Jack"),
    ("Charlie", "Frank"),
    ("Alice", "Eve"),
    ("Bob", "Jack"),
]

G = nx.Graph()
G.add_edges_from(data)

st.subheader("Graph Visualization")

fig, ax = plt.subplots(figsize=(6, 4))
pos = nx.spring_layout(G, seed=42)
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightgreen",
    edge_color="gray",
    node_s_

