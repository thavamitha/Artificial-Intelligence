import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Initialize graph in session state
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()

# Initialize heuristic values in session state (used for heuristic search)
if 'heuristics' not in st.session_state:
    st.session_state.heuristics = {}

# Function to add node with heuristic value
def add_node(node, heuristic_value):
    st.session_state.graph.add_node(node)
    st.session_state.heuristics[node] = heuristic_value

# Function to add edge between two nodes with weight
def add_edge(node1, node2, weight):
    st.session_state.graph.add_edge(node1, node2, weight=weight)

# Branch and Bound with Heuristic algorithm
def branch_and_bound_heuristic(graph, start, goal):
    # Priority queue for paths (based on cost + heuristic value)
    queue = [(0 + st.session_state.heuristics[start], 0, start, [start])]  # (total_cost, actual_cost, current_node, path)
    visited = set()
    best_path = None
    best_cost = float('inf')  # Bound for best solution

    while queue:
        # Pop the path with the lowest cost + heuristic
        total_cost, current_cost, current_node, path = heapq.heappop(queue)

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
                total_estimated_cost = new_cost + st.session_state.heuristics[neighbor]  # Add heuristic to estimate
                new_path = path + [neighbor]
                heapq.heappush(queue, (total_estimated_cost, new_cost, neighbor, new_path))

    return best_path, best_cost if best_path else None

# Streamlit UI
st.title("Branch and Bound with Heuristic Search Visualization")

# Input section to add nodes and edges
st.subheader("Add Nodes and Edges")

# Add new node with heuristic value
new_node = st.text_input("Enter new node:")
heuristic_value = st.number_input(f"Enter heuristic value for {new_node} (estimate to goal):", min_value=0.0, max_value=100.0, value=0.0)
if st.button("Add Node"):
    if new_node:
        add_node(new_node, heuristic_value)

# Add edge between two nodes with weight
node1 = st.text_input("Node 1:")
node2 = st.text_input("Node 2:")
weight = st.number_input(f"Enter weight for the edge between {node1} and {node2}:", min_value=1.0, max_value=100.0, value=1.0)
if st.button("Add Edge"):
    if node1 and node2:
        add_edge(node1, node2, weight)

# Select source and destination for Branch and Bound with Heuristic search
st.subheader("Branch and Bound with Heuristic Search")
start_node = st.selectbox("Select start node", st.session_state.graph.nodes)
goal_node = st.selectbox("Select destination node", st.session_state.graph.nodes)

# Button to start Branch and Bound with Heuristic search
if st.button("Start Branch and Bound with Heuristic Search"):
    if start_node and goal_node:
        path, cost = branch_and_bound_heuristic(st.session_state.graph, start_node, goal_node)
        if path:
            st.write(f"Optimal Path found: {' -> '.join(path)} with cost: {cost}")
        else:
            st.write("No path found!")

# Visualize the graph with heuristic values and edge weights
st.subheader("Graph Visualization")

def draw_graph():
    pos = nx.spring_layout(st.session_state.graph)
    plt.figure(figsize=(8, 6))
    nx.draw(st.session_state.graph, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=16)
    
    # Add heuristic values as node labels
    labels = {node: f"{node}\n(H={st.session_state.heuristics[node]})" for node in st.session_state.graph.nodes}
    nx.draw_networkx_labels(st.session_state.graph, pos, labels, font_size=12)

    # Draw edge weights
    edge_labels = nx.get_edge_attributes(st.session_state.graph, 'weight')
    nx.draw_networkx_edge_labels(st.session_state.graph, pos, edge_labels=edge_labels)
    
    st.pyplot(plt)

draw_graph()
