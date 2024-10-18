import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Initialize graph in session state
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()

# Function to add node
def add_node(node):
    st.session_state.graph.add_node(node)

# Function to add edge between two nodes
def add_edge(node1, node2, weight):
    st.session_state.graph.add_edge(node1, node2, weight=weight)

# Branch and Bound algorithm
def branch_and_bound(graph, start, goal):
    # Priority queue for holding paths (based on their total cost)
    queue = [(0, start, [start])]  # (cost, current_node, path)
    visited = set()
    best_path = None
    best_cost = float('inf')  # Bound for best solution

    while queue:
        # Pop the path with the lowest cost
        current_cost, current_node, path = heapq.heappop(queue)

        # If we reached the goal, update the best path
        if current_node == goal:
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = path

        # If current path exceeds best known cost, prune (bound)
        if current_cost >= best_cost:
            continue

        # Explore neighbors (branch)
        for neighbor in graph.neighbors(current_node):
            if neighbor not in path:
                new_cost = current_cost + graph[current_node][neighbor]['weight']
                new_path = path + [neighbor]
                heapq.heappush(queue, (new_cost, neighbor, new_path))

    return best_path, best_cost if best_path else None

# Streamlit UI
st.title("Branch and Bound Search Visualization")

# Input section to add nodes and edges
st.subheader("Add Nodes and Edges")

# Add new node
new_node = st.text_input("Enter new node:")
if st.button("Add Node"):
    if new_node:
        add_node(new_node)

# Add edge between two nodes with weight
node1 = st.text_input("Node 1:")
node2 = st.text_input("Node 2:")
weight = st.number_input(f"Enter weight for the edge between {node1} and {node2}:", min_value=1.0, max_value=100.0, value=1.0)
if st.button("Add Edge"):
    if node1 and node2:
        add_edge(node1, node2, weight)

# Select source and destination for Branch and Bound search
st.subheader("Branch and Bound Search")
start_node = st.selectbox("Select start node", st.session_state.graph.nodes)
goal_node = st.selectbox("Select destination node", st.session_state.graph.nodes)

# Button to start Branch and Bound search
if st.button("Start Branch and Bound Search"):
    if start_node and goal_node:
        path, cost = branch_and_bound(st.session_state.graph, start_node, goal_node)
        if path:
            st.write(f"Optimal Path found: {' -> '.join(path)} with cost: {cost}")
        else:
            st.write("No path found!")

# Visualize the graph with edge weights
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
