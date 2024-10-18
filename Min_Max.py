import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Initialize graph in session state
if 'graph' not in st.session_state:
    st.session_state.graph = nx.DiGraph()  # Directed graph for the game tree

# Initialize scores for leaf nodes in session state
if 'scores' not in st.session_state:
    st.session_state.scores = {}

# Function to add a node
def add_node(node, is_leaf=False, score=None):
    st.session_state.graph.add_node(node)
    if is_leaf:
        st.session_state.scores[node] = score

# Function to add an edge between two nodes
def add_edge(parent, child):
    st.session_state.graph.add_edge(parent, child)

# Minimax algorithm implementation
def minimax(node, is_maximizing):
    # If the node is a leaf, return its score
    if node in st.session_state.scores:
        return st.session_state.scores[node]

    # Get all children of the current node
    children = list(st.session_state.graph.successors(node))

    if is_maximizing:
        max_eval = float('-inf')
        for child in children:
            eval = minimax(child, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for child in children:
            eval = minimax(child, True)
            min_eval = min(min_eval, eval)
        return min_eval

# Streamlit UI
st.title("Minimax Theorem Visualization")

# Input section to add nodes and edges
st.subheader("Add Nodes and Edges")

# Add new node
new_node = st.text_input("Enter new node:")
is_leaf = st.checkbox("Is this a leaf node?")
score = None
if is_leaf:
    score = st.number_input(f"Enter score for leaf node {new_node}:", min_value=-100.0, max_value=100.0, value=0.0)
if st.button("Add Node"):
    if new_node:
        add_node(new_node, is_leaf, score)

# Add edge between two nodes
parent_node = st.text_input("Parent Node:")
child_node = st.text_input("Child Node:")
if st.button("Add Edge"):
    if parent_node and child_node:
        add_edge(parent_node, child_node)

# Select root node for Minimax search
st.subheader("Run Minimax Search")
root_node = st.selectbox("Select root node", st.session_state.graph.nodes)

# Button to start Minimax search
if st.button("Start Minimax Search"):
    if root_node:
        result = minimax(root_node, True)  # True represents the maximizing player
        st.write(f"The optimal value for the root node {root_node} is: {result}")

# Visualize the game tree
st.subheader("Game Tree Visualization")

def draw_tree():
    pos = nx.spring_layout(st.session_state.graph)
    plt.figure(figsize=(8, 6))
    nx.draw(st.session_state.graph, pos, with_labels=True, node_color='lightgreen', node_size=1500, font_size=16)
    
    # Add leaf node scores as labels
    labels = {node: f"{node}\n({st.session_state.scores[node]})" if node in st.session_state.scores else node for node in st.session_state.graph.nodes}
    nx.draw_networkx_labels(st.session_state.graph, pos, labels, font_size=12)

    # Draw edges
    nx.draw_networkx_edges(st.session_state.graph, pos)
    
    st.pyplot(plt)

draw_tree()
