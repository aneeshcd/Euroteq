import dash
from dash import dcc, html, Input, Output, State
import dash_cytoscape as cyto
import json
import random

# Initialize the Dash application framework
app = dash.Dash(__name__)

# -----------------------------------------------------------------------------
# Simulated Data Generation (representing parsed ReqIF and AI Analysis)
# -----------------------------------------------------------------------------

# Define nodes representing project requirements across different subsystems
# In production, this data is extracted from the <SPEC-OBJECT> tags in the ReqIF file.
nodes_data = []

# Define edges representing <SPEC-RELATIONS> traceability links.
# Data includes AI-generated criticality (Red/Yellow/Green) and confidence scores.
edges_data = []

# Construct the elements dictionary required by the Cytoscape component
elements =
for node in nodes_data:
    elements.append({
        'data': {'id': node['id'], 'label': f"{node['id']}\n{node['label']}", 'subsystem': node['subsystem']},
        'classes': 'standard-node'
    })

for edge in edges_data:
    elements.append({
        'data': {
            'source': edge['source'], 
            'target': edge['target'],
            'criticality': edge['criticality'],
            'confidence': edge['confidence']
        },
        # Assign CSS classes based on AI criticality assessment
        'classes': f"edge-{edge['criticality'].lower()}"
    })

# -----------------------------------------------------------------------------
# Stylesheet Definition for Visual Ergonomics and Hierarchy
# -----------------------------------------------------------------------------
cyto_stylesheet =

# -----------------------------------------------------------------------------
# Application Layout Architecture
# -----------------------------------------------------------------------------
app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'row', 'height': '100vh', 'fontFamily': 'Arial, sans-serif'}, children=),

    # Right Panel: Human-in-the-Loop AI Chatbox & SDG KPI Dashboard
    html.Div(style={'width': '35%', 'padding': '20px', 'backgroundColor': '#34495E', 'color': '#ECF0F1', 'display': 'flex', 'flexDirection': 'column'}, children=),

        # AI Prediction Outputs (Cost, Time, and SDG Metrics)
        html.Div(id='ai-impact-estimation', style={'padding': '15px', 'backgroundColor': '#2C3E50', 'marginBottom': '20px', 'borderRadius': '8px', 'flex': '1', 'borderLeft': '5px solid #E74C3C'}, children=),

        # Interactive Human-in-the-Loop Chatbox
        html.Div(style={'display': 'flex', 'flexDirection': 'column', 'marginTop': 'auto', 'backgroundColor': '#2C3E50', 'padding': '15px', 'borderRadius': '8px'}, children=)
    ])
])

# -----------------------------------------------------------------------------
# Callbacks for Interactivity (Node Selection, Isolation, AI Generation)
# -----------------------------------------------------------------------------

@app.callback(
    [Output('impact-network', 'stylesheet'),
     Output('selected-node-display', 'children'),
     Output('ai-impact-estimation', 'children')],
    # Triggered natively by clicking a node in Cytoscape
)
def handle_node_click(node_data):
    # Default state if nothing is clicked
    if not node_data:
        return cyto_stylesheet, html.Div(), dash.no_update

    node_id = node_data['id']
    node_label = node_data['label']
    subsystem = node_data['subsystem']

    # Algorithmic logic to find all connected edges and nodes (upstream and downstream)
    connected_edges = [e for e in edges_data if e['source'] == node_id or e['target'] == node_id]
    connected_nodes = set([node_id])
    for e in connected_edges:
        connected_nodes.add(e['source'])
        connected_nodes.add(e['target'])

    # Build a dynamic stylesheet based on the selection to reduce visual clutter
    dynamic_stylesheet = cyto_stylesheet.copy()
    
    # 1. Fade out all nodes and edges globally
    dynamic_stylesheet.append({
        'selector': 'node, edge',
        'style': {'opacity': 0.15}
    })
    
    # 2. Highlight the selected node and its direct topological neighbors
    for n in connected_nodes:
        dynamic_stylesheet.append({
            'selector': f'node[id = "{n}"]',
            'style': {
                'opacity': 1.0,
                'border-width': '4px' if n == node_id else '2px',
                'border-color': '#E67E22' if n == node_id else '#3498DB',
                'width': '160px' if n == node_id else '140px',
                'height': '70px' if n == node_id else '60px'
            }
        })

    # 3. Highlight connected edges, overriding the fade, based on original class
    for e in connected_edges:
        dynamic_stylesheet.append({
            'selector': f'edge[source = "{e["source"]}"][target = "{e["target"]}"]',
            'style': {
                'opacity': 1.0,
                'width': 6,
                'z-index': 10
            }
        })

    # Simulate AI Calculation based on node selection and historical metadata
    simulated_cost = random.randint(25, 250) * 1000
    simulated_delay = random.randint(2, 21)
    # Calculate average confidence of the cascading impact
    avg_confidence = sum([e['confidence'] for e in connected_edges]) / len(connected_edges) if connected_edges else 0
    
    # SDG Calculation: Converting financial waste into Prevented Embodied Carbon (kg CO2e)
    embodied_carbon_saved = round(simulated_cost * 0.042, 2) 

    # Construct the UI elements for the right panel updates
    selection_panel =

    ai_estimation_panel =),
        html.H5("Sustainability Metrics (SDG 12 & 13)", style={'color': '#27AE60', 'marginBottom': '5px', 'marginTop': '15px'}),
        html.Ul()
    ]

    return dynamic_stylesheet, selection_panel, ai_estimation_panel

# Callback for Chatbox Interaction
@app.callback(
    Output('chat-history', 'children'),
    [Input('send-btn', 'n_clicks')],
   
)
def update_chat(n_clicks, user_input, existing_chat):
    if n_clicks > 0 and user_input:
        existing_chat = existing_chat or
        # Append User Message to history
        existing_chat.append(html.Div(f"Engineer: {user_input}", style={'fontWeight': 'bold', 'color': '#2980B9', 'marginBottom': '8px'}))
        
        # Simulate AI Response Contextualized by the HITL paradigm
        ai_response = f"AI Agent: Based on my analysis of historical commits from similar thermal subsystem changes, modifying this requirement highly correlates with a failure in HW-REQ-021. I recommend increasing the cooling fan RPM thresholds before approving this change."
        existing_chat.append(html.Div(ai_response, style={'color': '#2C3E50', 'marginBottom': '15px', 'fontStyle': 'italic', 'backgroundColor': '#EAECEE', 'padding': '8px', 'borderRadius': '4px'}))
        
        return existing_chat
    return existing_chat

if __name__ == '__main__':
    # Run the Dash server
    app.run_server(debug=True)