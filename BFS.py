import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Initialize graph object as session state so it persists across interactions
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()

# Function to add node
def add_node(node):
    st.session_state.graph.add_node(node)

# Function to add edge between two nodes
def add_edge(node1, node2):
    st.session_state.graph.add_edge(node1, node2)

# BFS algorithm to search the graph
def bfs(graph, start, goal):
    visited = set()
    queue = deque([[start]])  # Store paths instead of just nodes

    if start == goal:
        return [start]

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            neighbors = graph[node]

            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

                if neighbor == goal:
                    return new_path

            visited.add(node)

    return None  # If no path found

# Streamlit UI
st.title("BFS Graph Search Visualization")

# Input section to add nodes and edges
st.subheader("Add Nodes and Edges")

# Add new node
new_node = st.text_input("Enter new node:")
if st.button("Add Node"):
    if new_node:
        add_node(new_node)

# Add edge between two nodes
node1 = st.text_input("Node 1:")
node2 = st.text_input("Node 2:")
if st.button("Add Edge"):
    if node1 and node2:
        add_edge(node1, node2)

# Select source and destination for BFS
st.subheader("BFS Search")
start_node = st.selectbox("Select start node", st.session_state.graph.nodes)
goal_node = st.selectbox("Select destination node", st.session_state.graph.nodes)

# Button to start BFS search
if st.button("Start BFS Search"):
    if start_node and goal_node:
        path = bfs(st.session_state.graph, start_node, goal_node)
        if path:
            st.write(f"Path found: {' -> '.join(path)}")
        else:
            st.write("No path found!")

# Visualize graph
st.subheader("Graph Visualization")

# Draw the graph
def draw_graph():
    pos = nx.spring_layout(st.session_state.graph)  # Layout for visualization
    plt.figure(figsize=(8, 6))
    nx.draw(st.session_state.graph, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=16)
    st.pyplot(plt)

