import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Initialize graph object in session state so it persists across interactions
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()

# Function to add node
def add_node(node):
    st.session_state.graph.add_node(node)

# Function to add edge between two nodes
def add_edge(node1, node2):
    st.session_state.graph.add_edge(node1, node2)

# Function for Bidirectional Search (BDS)
def bidirectional_search(graph, start, goal):
    if start == goal:
        return [start]

    # Frontiers for BFS from both directions
    start_queue = deque([start])
    goal_queue = deque([goal])

    # Parents to reconstruct path
    start_parents = {start: None}
    goal_parents = {goal: None}

    while start_queue and goal_queue:
        # Expand from start side
        if start_queue:
            path = expand(graph, start_queue, start_parents, goal_parents)
            if path:
                return path

        # Expand from goal side
        if goal_queue:
            path = expand(graph, goal_queue, goal_parents, start_parents)
            if path:
                return path

    return None  # If no path found

# Helper function for expanding the search frontier
def expand(graph, queue, parents, other_parents):
    current = queue.popleft()

    for neighbor in graph.neighbors(current):
        if neighbor not in parents:
            parents[neighbor] = current
            queue.append(neighbor)

            if neighbor in other_parents:  # Path found
                return construct_path(parents, other_parents, neighbor)
    
    return None

# Helper function to construct the full path from both sides
def construct_path(start_parents, goal_parents, meeting_node):
    # Path from start to meeting node
    path_start = []
    node = meeting_node
    while node:
        path_start.append(node)
        node = start_parents[node]
    path_start.reverse()

    # Path from meeting node to goal
    path_goal = []
    node = goal_parents[meeting_node]
    while node:
        path_goal.append(node)
        node = goal_parents[node]

    return path_start + path_goal

# Streamlit UI
st.title("Bidirectional Search (BDS) Graph Visualization")

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

# Select source and destination for BDS
st.subheader("BDS Search")
start_node = st.selectbox("Select start node", st.session_state.graph.nodes)
goal_node = st.selectbox("Select destination node", st.session_state.graph.nodes)

# Button to start BDS search
if st.button("Start BDS Search"):
    if start_node and goal_node:
        path = bidirectional_search(st.session_state.graph, start_node, goal_node)
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

draw_graph()
