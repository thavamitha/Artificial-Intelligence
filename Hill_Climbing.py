import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

# Initialize graph in session state
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()

# Initialize heuristic values (for hill climbing) in session state
if 'heuristics' not in st.session_state:
    st.session_state.heuristics = {}

# Function to add node
def add_node(node, heuristic_value):
    st.session_state.graph.add_node(node)
    st.session_state.heuristics[node] = heuristic_value

# Function to add edge between two nodes
def add_edge(node1, node2):
    st.session_state.graph.add_edge(node1, node2)

# Hill Climbing algorithm
def hill_climbing(graph, start, goal):
    current_node = start
    path = [current_node]

    while current_node != goal:
        neighbors = list(graph.neighbors(current_node))

        if not neighbors:
            return None  # No path found

        # Choose the neighbor with the best (lowest) heuristic value
        next_node = min(neighbors, key=lambda n: st.session_state.heuristics[n])

        if st.session_state.heuristics[next_node] >= st.session_state.heuristics[current_node]:
            break  # Reached a peak (local maxima)

        current_node = next_node
        path.append(current_node)

    if current_node == goal:
        return path
    else:
        return None

# Streamlit UI
st.title("Hill Climbing Search Visualization")

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

# Select source and destination for Hill Climbing search
st.subheader("Hill Climbing Search")
start_node = st.selectbox("Select start node", st.session_state.graph.nodes)
goal_node = st.selectbox("Select destination node", st.session_state.graph.nodes)

# Button to start Hill Climbing search
if st.button("Start Hill Climbing Search"):
    if start_node and goal_node:
        path = hill_climbing(st.session_state.graph, start_node, goal_node)
        if path:
            st.write(f"Path found: {' -> '.join(path)}")
        else:
            st.write("No path found or stuck at local maxima!")

# Visualize graph with heuristic values
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
