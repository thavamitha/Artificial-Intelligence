import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Initialize graph in session state
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()

# Function to add node
def add_node(node):
    st.session_state.graph.add_node(node)

# Function to add edge
def add_edge(node1, node2):
    st.session_state.graph.add_edge(node1, node2)

# DFS algorithm
def dfs(graph, start, goal, path=None, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()
    
    visited.add(start)
    
    if start == goal:
        return path
    
    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            result = dfs(graph, neighbor, goal, path + [neighbor], visited)
            if result:
                return result
    return None

# Streamlit UI
st.title("Depth-First Search (DFS) Graph Visualization")

# Add Nodes and Edges
st.subheader("Add Nodes and Edges")
new_node = st.text_input("Enter new node:")
if st.button("Add Node"):
    if new_node:
        add_node(new_node)

node1 = st.text_input("Node 1:")
node2 = st.text_input("Node 2:")
if st.button("Add Edge"):
    if node1 and node2:
        add_edge(node1, node2)

# Select source and destination
st.subheader("DFS Search")
start_node = st.selectbox("Select start node", st.session_state.graph.nodes)
goal_node = st.selectbox("Select destination node", st.session_state.graph.nodes)

# Button to start DFS search
if st.button("Start DFS Search"):
    if start_node and goal_node:
        path = dfs(st.session_state.graph, start_node, goal_node)
        if path:
            st.write(f"Path found: {' -> '.join(path)}")
        else:
            st.write("No path found!")

# Visualize the graph
st.subheader("Graph Visualization")
def draw_graph():
    pos = nx.spring_layout(st.session_state.graph)
    plt.figure(figsize=(8, 6))
    nx.draw(st.session_state.graph, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=16)
    st.pyplot(plt)

draw_graph()
