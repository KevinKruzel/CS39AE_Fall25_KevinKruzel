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

# --- Build graph ---
G = nx.Graph()
G.add_edges_from(data)

# --- Layout (computed once) ---
pos = nx.spring_layout(G, seed=42)

# --- Communities ---
communities = greedy_modularity_communities(G)

palette = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
node_to_comm = {}
for c_index, comm in enumerate(communities):
    for node in comm:
        node_to_comm[node] = c_index

# Base colors: by community
community_colors = [palette[node_to_comm[n] % len(palette)] for n in G.nodes()]

# --- Centrality measures ---
st.subheader("Centrality Measures")

degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G, weight="weight")
closeness_centrality = nx.closeness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)

centrality_df = pd.DataFrame({
    "Degree": degree_centrality,
    "Betweenness": betweenness_centrality,
    "Closeness": closeness_centrality,
    "Eigenvector": eigenvector_centrality,
})
centrality_df = centrality_df.round(3)
centrality_df.index.name = "Node"

st.dataframe(centrality_df)

# --- Identify most influential node (by betweenness) ---
most_influential = max(betweenness_centrality, key=betweenness_centrality.get)
most_influential_score = betweenness_centrality[most_influential]

st.markdown(
    f"**Most influential person (for spreading information, via betweenness centrality):** "
    f":star2: `{most_influential}` (score = {most_influential_score:.3f})"
)

# Build final node color list: highlight most influential in yellow
node_colors = []
for node, base_color in zip(G.nodes(), community_colors):
    if node == most_influential:
        node_colors.append("yellow")  # highlight color
    else:
        node_colors.append(base_color)

# --- Graph visualization ---
st.subheader("Graph Visualization (Communities + Most Influential Highlighted)")

fig, ax = plt.subplots(figsize=(8, 6))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3000,
    node_color=node_colors,
    edge_color="gray",
    font_size=10,
    font_weight="bold",
    ax=ax,
)
ax.set_title("Network Colored by Community\n(Most Influential in Yellow)")
st.pyplot(fig)

# --- Communities text output ---
st.subheader("Communities (Greedy Modularity)")

for i, community in enumerate(communities, 1):
    st.write(f"**Community {i}:** {', '.join(sorted(community))}")
