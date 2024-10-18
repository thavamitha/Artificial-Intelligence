import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

# Initialize graph in session state
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()

# Initialize heuristic values (for Beam Search) in session state
if 'heuristics' not in st.session_state:
    st.session_state.heuristics = {}

# Function to add node
def add_node(node, heuristic_value):
    st.session_state.graph.add_node(node)
    st.session_state.heuristics[node] = heuristic_value

# Function to add edge between two nodes
def add_edge(node1, node2):
    st.session_state.graph.add_edge(node1, node2)

# Beam Search algorithm
def beam_search(graph, start, goal, beam_width):
    current_nodes = [(start, [start])]  # List of tuples (node, path)
    
    while current_nodes:
        next_nodes = []

        # Expand each node in the current beam
        for node, path in current_nodes:
            if node == goal:
                return path  # Path found

            neighbors = list(graph.neighbors(node))
            for neighbor in neighbors:
                if neighbor not in path:  # Prevent cycles
                    new_path = path + [neighbor]
                    next_nodes.append((neighbor, new_path))

        # Sort by heuristic value and keep only the top beam_width nodes
        next_nodes = sorted(next_nodes, key=lambda x: st.session_state.heuristics[x[0]])[:beam_width]

        if not next_nodes:
            break  # No more nodes to explore

        current_nodes = next_nodes

    return None  # No path found

# Streamlit UI
st.title("Beam Search Visualization")

# Input section to add nodes and edges
st.subheader("Add Nodes and Edges")

# Add new node with heuristic value
new_node = st.text_input("Enter new node:")
heuristic_value = st.number_input(f"Enter heuristic value for {new_node}:", min_value=0.0, max_value=100.0, value=50.0)
if st.button("Add Node"):
    if new_node:
        add_node(new_node, heuristic_value)

# Add edge between two nodes
node1 = st.text_input("Node 1:")
node2 = st.text_input("Node 2:")
if st.button("Add Edge"):
    if node1 and node2:
        add_edge(node1, node2)

# Select source, destination, and beam width for Beam Search
st.subheader("Beam Search")
start_node = st.selectbox("Select start node", st.session_state.graph.nodes)
goal_node = st.selectbox("Select destination node", st.session_state.graph.nodes)
beam_width = st.slider("Select Beam Width", min_value=1, max_value=10, value=2)

# Button to start Beam Search
if st.button("Start Beam Search"):
    if start_node and goal_node:
        path = beam_search(st.session_state.graph, start_node, goal_node, beam_width)
        if path:
            st.write(f"Path found: {' -> '.join(path)}")
        else:
            st.write("No path found!")

# Visualize the graph with heuristic values
st.subheader("Graph Visualization")

def draw_graph():
    pos = nx.spring_layout(st.session_state.graph)
    plt.figure(figsize=(8, 6))
    nx.draw(st.session_state.graph, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=16)

    # Add heuristic values as node labels
    labels = {node: f"{node}\n(H={st.session_state.heuristics[node]})" for node in st.session_state.graph.nodes}
    nx.draw_networkx_labels(st.session_state.graph, pos, labels, font_size=12)
    
    st.pyplot(plt)

draw_graph()
