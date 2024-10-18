import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Initialize graph in session state
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()

# Function to add node
def add_node(node):
    st.session_state.graph.add_node(node)

# Function to add edge between two nodes
def add_edge(node1, node2, weight):
    st.session_state.graph.add_edge(node1, node2, weight=weight)

# Oracle Search (simulated by finding the shortest path)
def oracle_search(graph, start, goal):
    try:
        # Since the "oracle" knows the exact solution, we use NetworkX's shortest path function
        return nx.shortest_path(graph, source=start, target=goal, weight='weight')
    except nx.NetworkXNoPath:
        return None  # No path exists between the start and goal

# Streamlit UI
st.title("Oracle Search Visualization")

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
weight = st.number_input(f"Enter weight for the edge between {node1} and {node2}:", min_value=1.0, max_value=100.0, value=1.0)
if st.button("Add Edge"):
    if node1 and node2:
        add_edge(node1, node2, weight)

# Select source and destination for Oracle Search
st.subheader("Oracle Search")
start_node = st.selectbox("Select start node", st.session_state.graph.nodes)
goal_node = st.selectbox("Select destination node", st.session_state.graph.nodes)

# Button to start Oracle Search
if st.button("Start Oracle Search"):
    if start_node and goal_node:
        path = oracle_search(st.session_state.graph, start_node, goal_node)
        if path:
            st.write(f"Oracle path found: {' -> '.join(path)}")
        else:
            st.write("No path found!")

# Visualize graph with edge weights
st.subheader("Graph Visualization")

def draw_graph():
    pos = nx.spring_layout(st.session_state.graph)
    plt.figure(figsize=(8, 6))
    nx.draw(st.session_state.graph, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=16)
    
    # Draw edge weights
    edge_labels = nx.get_edge_attributes(st.session_state.graph, 'weight')
    nx.draw_networkx_edge_labels(st.session_state.graph, pos, edge_labels=edge_labels)
    
    st.pyplot(plt)

draw_graph()
