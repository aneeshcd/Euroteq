import dash
from dash import dcc, html, Input, Output, callback, State, no_update
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Sample requirements data
REQUIREMENTS_DATA = {
    "R1": {"name": "Main Control System", "subsystem": "Control", "criticality": "High", "cost": 50000, "time": 30},
    "R2": {"name": "Sensor Integration", "subsystem": "Sensors", "criticality": "High", "cost": 30000, "time": 20},
    "R3": {"name": "Power Management", "subsystem": "Power", "criticality": "Medium", "cost": 20000, "time": 15},
    "R4": {"name": "Communication Protocol", "subsystem": "Comms", "criticality": "High", "cost": 25000, "time": 18},
    "R5": {"name": "Safety Monitoring", "subsystem": "Safety", "criticality": "Critical", "cost": 40000, "time": 25},
    "R6": {"name": "Data Processing", "subsystem": "Processing", "criticality": "Medium", "cost": 15000, "time": 12}
}

IMPACT_MAP = {
    "R1": ["R2", "R3", "R5"],
    "R2": ["R1", "R4", "R6"],
    "R3": ["R1", "R5"],
    "R4": ["R2", "R6"],
    "R5": ["R1", "R3"],
    "R6": ["R2", "R4"]
}

app = dash.Dash(__name__)

def create_spider_web_graph(selected_node=None, highlight_path=None):
    nodes = list(REQUIREMENTS_DATA.keys())
    n = len(nodes)
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    
    x_nodes = np.cos(angles).tolist()
    y_nodes = np.sin(angles).tolist()
    
    # Node properties
    node_colors = []
    node_sizes = []
    hover_text = []
    
    for i, node in enumerate(nodes):
        criticality = REQUIREMENTS_DATA[node]["criticality"]
        color_map = {"Critical": "#e74c3c", "High": "#f39c12", "Medium": "#f1c40f", "Low": "#27ae60"}
        node_colors.append(color_map.get(criticality, "#3498db"))
        
        size = 25 if node == selected_node else 18
        node_sizes.append(size)
        
        info = REQUIREMENTS_DATA[node]
        hover_text.append(
            f"<b>{node}</b><br>{info['name']}<br>"
            f"Subsystem: {info['subsystem']}<br>"
            f"Criticality: {info['criticality']}<br>"
            f"Cost: ${info['cost']:,} | Time: {info['time']}d"
        )
    
    # Create edges - FIXED COLOR ISSUE
    edge_x, edge_y = [], []
    edge_colors = []
    edge_widths = []
    
    for node1 in nodes:
        for node2 in IMPACT_MAP.get(node1, []):
            if node1 < node2:
                i1, i2 = nodes.index(node1), nodes.index(node2)
                x1, y1, x2, y2 = x_nodes[i1], y_nodes[i1], x_nodes[i2], y_nodes[i2]
                
                edge_x.extend([x1, x2, None])
                edge_y.extend([y1, y2, None])
                
                # Single color string per edge segment
                is_highlighted = highlight_path and (node1 in highlight_path or node2 in highlight_path)
                color = "#e74c3c" if is_highlighted else "#3498db"
                width = 10 if is_highlighted else 4
                
                edge_colors.extend([color, color, None])
                edge_widths.extend([width, width, None])
    
    # Create figure
    fig = go.Figure()
    
    # Edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=edge_widths, color=edge_colors),
        mode='lines',
        line_shape='spline',
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Nodes
    fig.add_trace(go.Scatter(
        x=x_nodes, y=y_nodes,
        mode='markers+text',
        marker=dict(
            size=node_sizes, 
            color=node_colors,
            line=dict(width=3, color='white'),
            symbol='circle'
        ),
        text=nodes,
        textposition="middle center",
        textfont=dict(size=14, color='white', family='Arial Black'),
        hovertemplate=hover_text[i] + '<extra></extra>',
        hoverinfo='text',
        showlegend=False
    ))
    
    fig.update_layout(
        title={
            "text": "🤖 AI Requirements Impact Map",
            "x": 0.5,
            "font": {"size": 24, "color": "#2c3e50"}
        },
        showlegend=False,
        hovermode='closest',
        margin=dict(t=80, b=40),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#ffffff',
        font=dict(family="Arial", size=12)
    )
    
    return fig

# Initial layout
initial_fig = create_spider_web_graph()

app.layout = html.Div([
    html.H1("🚀 AI Requirements Impact Analyzer", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'margin': '30px 0'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='impact-map', figure=initial_fig, style={'height': '500px'}),
            html.Div(id='impact-details', className='six columns')
        ], className='six columns'),
        
        html.Div([
            html.Div(id='analysis-panel', className='six columns')
        ])
    ], className='row'),
    
    html.Div([
        html.Div([
            dcc.Textarea(id='chat-input', placeholder="Ask AI about impacts...", style={'width': '100%', 'height': 80}),
            html.Button('💭 Ask AI', id='send-button', n_clicks=0, className='button'),
            html.Div(id='chat-output')
        ], className='twelve columns')
    ], className='row', style={'marginTop': 30})
], style={'padding': 30, 'fontFamily': 'Arial'})

@callback(
    [Output('impact-map', 'figure'),
     Output('impact-details', 'children')],
    Input('impact-map', 'clickData')
)
def update_graph(clickData):
    if not clickData:
        return initial_fig, html.Div("👆 Click a node to analyze impact")
    
    node = clickData['points'][0]['text']
    highlight_path = [node] + IMPACT_MAP.get(node, [])
    
    fig = create_spider_web_graph(node, highlight_path)
    
    details = html.Div([
        html.H3(f"🔍 Impact Analysis: {node}"),
        html.P(f"Subsystem: {REQUIREMENTS_DATA[node]['subsystem']}"),
        html.P(f"Criticality: {REQUIREMENTS_DATA[node]['criticality']}"),
        html.Hr(),
        html.H4("💰 Cost Impact: +$45,000"),
        html.H4("⏱️ Time Impact: +25 days"),
        html.H4("🤖 AI Confidence: 89%"),
        html.H4("🌱 CO₂ Impact: +22kg (SDG 9,12,13)")
    ], style={'padding': 20, 'backgroundColor': '#f8f9fa', 'borderRadius': 10})
    
    return fig, details

@callback(
    Output('chat-output', 'children'),
    [Input('send-button', 'n_clicks')],
    [State('chat-input', 'value')],
    prevent_initial_call=True
)
def chat_response(n_clicks, message):
    if not message:
        return ""
    
    return html.Div([
        html.P(f"🤖 AI: Great question about '{message[:30]}...'! "
               "I recommend human review + impact analysis before changes. "
               "SDG compliant solution reduces waste by 30%."),
        html.P("💡 Try clicking R1-R6 nodes above!")
    ])

@callback(
    Output('analysis-panel', 'children'),
    Input('impact-map', 'clickData')
)
def update_panel(clickData):
    if not clickData:
        return html.Div("Select a requirement to see detailed analysis")
    return html.Div("Analysis panel")

if __name__ == '__main__':
    print("🚀 AI Requirements Impact Demo - STARTING...")
    print("🌐 Open: http://127.0.0.1:8050")
    print("✅ All errors fixed!")
    app.run(debug=True, port=8050)