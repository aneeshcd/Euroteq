import dash
from dash import dcc, html, Input, Output, State, callback, no_update, ctx
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
], suppress_callback_exceptions=True)

REQUIREMENTS = {
    "R1": {"name": "Flight Control System", "level": "SYSTEM", "color": "red"},
    "R2": {"name": "Avionics Sensors", "level": "SUBSYSTEM", "color": "orange"},
    "R3": {"name": "Power System", "level": "SUBSYSTEM", "color": "yellow"},
    "R4": {"name": "Comm System", "level": "SUBSYSTEM", "color": "blue"},
    "R5": {"name": "Safety System", "level": "SUBSYSTEM", "color": "red"},
    "R6": {"name": "Data Processing", "level": "SUBSYSTEM", "color": "purple"},
    "R7": {"name": "Actuation System", "level": "SUBSYSTEM", "color": "green"},
    "R8": {"name": "Navigation", "level": "SUBSYSTEM", "color": "cyan"}
}

SPIDER_POS = {
    "R1": (0, 0),
    "R2": (0.5, 0.4),
    "R3": (0.5, -0.4),
    "R5": (-0.5, 0.4),
    "R7": (-0.5, -0.4),
    "R4": (0.9, 0.7),
    "R6": (0.9, -0.7),
    "R8": (-0.9, 0)
}

EDGES = [
    ("R1", "R2", "Sensor Data"),
    ("R1", "R3", "Power Feed"),
    ("R1", "R5", "Safety Check"),
    ("R1", "R7", "Actuator Cmd"),
    ("R2", "R4", "Data Link"),
    ("R2", "R6", "Processing"),
    ("R3", "R5", "Emergency Power"),
    ("R7", "R1", "Feedback"),
    ("R4", "R6", "Comm Data"),
    ("R5", "R3", "Power Monitor"),
    ("R8", "R1", "Nav Data")
]

IMPACT_METRICS = {
    "R1": {"cost": "$125K", "time": "45d", "confidence": "92%", "risk": "CRITICAL"},
    "R2": {"cost": "$65K", "time": "22d", "confidence": "88%", "risk": "HIGH"},
    "R3": {"cost": "$35K", "time": "15d", "confidence": "85%", "risk": "MEDIUM"},
    "R4": {"cost": "$45K", "time": "18d", "confidence": "87%", "risk": "HIGH"},
    "R5": {"cost": "$80K", "time": "30d", "confidence": "95%", "risk": "CRITICAL"},
    "R6": {"cost": "$25K", "time": "12d", "confidence": "82%", "risk": "MEDIUM"},
    "R7": {"cost": "$40K", "time": "16d", "confidence": "89%", "risk": "HIGH"},
    "R8": {"cost": "$30K", "time": "14d", "confidence": "84%", "risk": "MEDIUM"}
}

CARD_STYLE = {
    'background': 'rgba(255,255,255,0.96)',
    'borderRadius': '22px',
    'boxShadow': '0 18px 40px rgba(15,23,42,0.14)',
    'border': '1px solid rgba(226,232,240,0.9)',
    'padding': '22px',
    'fontFamily': 'Inter'
}

SECTION_TITLE_STYLE = {
    'fontSize': '18px',
    'fontWeight': 700,
    'color': '#1a202c',
    'marginBottom': '14px',
    'paddingBottom': '10px',
    'borderBottom': '1px solid #e2e8f0'
}

def create_spider_web(selected=None):
    nodes = list(REQUIREMENTS.keys())
    x_nodes = [SPIDER_POS[n][0] for n in nodes]
    y_nodes = [SPIDER_POS[n][1] for n in nodes]
    fig = go.Figure()

    outer_nodes = ["R8", "R5", "R2", "R4", "R6", "R7"]
    outer_points = np.array([SPIDER_POS[n] for n in outer_nodes], dtype=float)

    ring_scales = [0.2, 0.4, 0.6, 0.8, 1.0]
    for scale in ring_scales:
        scaled = outer_points * scale
        ring_x = list(scaled[:, 0]) + [scaled[0, 0]]
        ring_y = list(scaled[:, 1]) + [scaled[0, 1]]
        fig.add_trace(go.Scatter(
            x=ring_x,
            y=ring_y,
            mode='lines',
            line=dict(color='rgba(70,70,70,0.55)', width=1.6),
            hoverinfo='skip',
            showlegend=False,
            name=''
        ))

    for node in outer_nodes:
        x2, y2 = SPIDER_POS[node]
        fig.add_trace(go.Scatter(
            x=[0, x2],
            y=[0, y2],
            mode='lines',
            line=dict(color='rgba(80,80,80,0.48)', width=1.4),
            hoverinfo='skip',
            showlegend=False,
            name=''
        ))

    label_offsets = {
        ("R1", "R2", "Sensor Data"): (0.03, 0.05),
        ("R1", "R3", "Power Feed"): (0.10, -0.05),
        ("R1", "R5", "Safety Check"): (-0.08, 0.05),
        ("R1", "R7", "Actuator Cmd"): (-0.10, -0.06),
        ("R2", "R4", "Data Link"): (0.06, 0.05),
        ("R2", "R6", "Processing"): (0.06, -0.02),
        ("R3", "R5", "Emergency Power"): (0.02, 0.02),
        ("R7", "R1", "Feedback"): (-0.03, -0.02),
        ("R4", "R6", "Comm Data"): (0.10, 0.00),
        ("R5", "R3", "Power Monitor"): (0.00, 0.08),
        ("R8", "R1", "Nav Data"): (-0.05, 0.02)
    }

    for edge in EDGES:
        x1, y1 = SPIDER_POS[edge[0]]
        x2, y2 = SPIDER_POS[edge[1]]
        label = edge[2]

        is_highlighted = selected and (edge[0] == selected or edge[1] == selected)
        line_color = '#8b0000' if is_highlighted else '#8f8f8f'
        line_width = 8 if is_highlighted else 3.2

        fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode='lines',
            line=dict(color=line_color, width=line_width),
            hoverinfo='skip',
            showlegend=False,
            name=''
        ))

        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = label_offsets.get(edge, (0, 0))

        fig.add_annotation(
            x=mid_x + dx,
            y=mid_y + dy,
            text=label,
            showarrow=False,
            font=dict(size=11, color='#2d3748', family='Inter'),
            bgcolor='rgba(255,255,255,0.96)',
            bordercolor='#a0aec0',
            borderwidth=1,
            borderpad=2
        )

    node_sizes = []
    node_colors = []
    hover_texts = []

    for node in nodes:
        is_selected = node == selected
        is_connected = selected and any(
            e[0] == node or e[1] == node
            for e in EDGES if e[0] == selected or e[1] == selected
        )

        size = 40 if is_selected else (30 if is_connected else 25)
        color = 'darkred' if is_selected else ('orange' if is_connected else 'steelblue')

        node_sizes.append(size)
        node_colors.append(color)

        metrics = IMPACT_METRICS[node]
        hover_texts.append(
            f"<b>{node}</b><br>{REQUIREMENTS[node]['name']}<br>"
            f"Level: {REQUIREMENTS[node]['level']}<br>"
            f"💰 {metrics['cost']} | ⏱️ {metrics['time']}<br>"
            f"🤖 {metrics['confidence']} | ⚠️ {metrics['risk']}"
        )

    fig.add_trace(go.Scatter(
        x=x_nodes,
        y=y_nodes,
        mode='markers+text',
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=4, color='white'),
            symbol='circle'
        ),
        text=nodes,
        textposition='middle center',
        textfont=dict(size=14, color='white', family='Inter'),
        hovertext=hover_texts,
        hovertemplate='%{hovertext}<extra></extra>',
        showlegend=False
    ))

    fig.update_layout(
        title=dict(
            text='AI Powered Impact Analysis Net',
            x=0.5,
            font=dict(size=24, color='#1a202c', family='Inter')
        ),
        showlegend=False,
        height=860,
        xaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            range=[-1.0, 1.0],
            fixedrange=True
        ),
        yaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            range=[-0.78, 0.78],
            fixedrange=True,
            scaleanchor='x',
            scaleratio=1
        ),
        plot_bgcolor='white',
        paper_bgcolor='#f7fafc',
        margin=dict(t=80, b=10, l=10, r=10),
        font=dict(family='Inter')
    )

    return fig

def build_chat_response(question):
    q_lower = question.lower().strip() if question else ''
    req_id = None

    for r in REQUIREMENTS.keys():
        if r.lower() in q_lower:
            req_id = r
            break

    subsystem_responses = {
        'R1': {
            'default': '🚨 R1 Flight Control System change is CRITICAL. It can propagate across sensor, actuation, power, and safety interfaces. Full control-law regression, integration testing, and downstream verification are recommended before approval.',
            'risk': '⚠️ R1 Flight Control System is flight-critical. A change here should be treated as a major design-change candidate because it can affect controllability, aircraft behavior, and system interactions.',
            'cert': '🛩️ R1 Flight Control System changes may trigger deeper certification scrutiny because the FAA has increased focus on major flight-control design changes and system interactions. Expect stronger design disclosure, traceability, and re-verification evidence requirements.',
            'mitigation': '🧩 For R1, isolate the control-law change, freeze impacted interfaces early, and run phased regression with actuator, sensor, and degraded-mode scenarios before release.',
            'sustainability': '🌱 Sustainability impact is moderate because flight-control changes increase simulation, regression effort, and engineering rework. Even so, if the change improves controllability or reduces downstream failure risk, it is recommended to proceed with a tightly scoped implementation and full verification.'
        },
        'R2': {
            'default': '📡 R2 Avionics Sensors change mainly affects data quality, calibration integrity, and signal trust. It can influence flight control, navigation, and processing performance through incorrect or unstable inputs.',
            'risk': '⚠️ R2 Avionics Sensors carries HIGH risk because sensor changes can introduce latent downstream errors that are difficult to detect early. Calibration drift, interface mismatches, and false confidence are the main concerns.',
            'cert': '🛠️ R2 sensor changes typically require calibration evidence, interface validation, and verification that dependent subsystems still meet their functional assumptions after the modification.',
            'mitigation': '🔍 For R2, perform recalibration, fault-injection testing, and sensor cross-check validation before approving the change into the integrated baseline.',
            'sustainability': '🌱 Sustainability impact is moderate because recalibration and repeated validation create additional test effort and bench time. However, if the sensor change improves data reliability and reduces future defect churn, it is still the more sustainable lifecycle choice overall.'
        },
        'R3': {
            'default': '🔋 R3 Power System change affects power availability, resilience, and emergency continuity across connected subsystems. It has strong implications for degraded-mode operation and recovery behavior.',
            'risk': '⚠️ R3 Power System is operationally significant because a design change here can cascade under abnormal or emergency conditions. The main risks are reduced redundancy margin, transfer instability, or hidden power-budget violations.',
            'cert': '🔌 R3 changes should be reviewed for power budgeting, redundancy logic, emergency-power continuity, and evidence that critical functions remain supportable under failure conditions.',
            'mitigation': '🛡️ For R3, verify redundancy paths, emergency transfer behavior, and brownout or power-fail recovery before freezing the design.',
            'sustainability': '🌱 Sustainability impact is mixed because power-system changes may increase component usage and test effort, but they can also improve long-term efficiency and reduce operational waste. If the change improves reliability and lowers lifecycle power loss, it is recommended.'
        },
        'R4': {
            'default': '📶 R4 Communication System change affects message timing, link integrity, and interface reliability between connected subsystems. The main concern is propagation of stale, delayed, or malformed data.',
            'risk': '⚠️ R4 Communication System is HIGH risk when protocols, timing, or interface assumptions change. Dependent subsystems may continue operating incorrectly even when the communication fault is not immediately visible.',
            'cert': '📨 R4 communication changes generally require interface-control validation, latency and timeout checks, and evidence that dependent functions remain robust under degraded-link conditions.',
            'mitigation': '🔗 For R4, revalidate protocol handling, retry logic, timeout behavior, and degraded-link performance with connected processing and control subsystems.',
            'sustainability': '🌱 Sustainability impact is low-to-moderate because communication updates usually increase integration and regression effort. However, if the change reduces retransmissions, interface failures, or repeated troubleshooting, it supports better long-term system efficiency.'
        },
        'R5': {
            'default': '🚨 R5 Safety System change is CRITICAL. It directly affects hazard controls, fail-safe behavior, and compliance evidence, so any modification here requires strict change governance.',
            'risk': '⚠️ R5 Safety System is the highest-risk area in the model. A change here should trigger formal hazard reassessment, independent safety review, and strict approval before implementation.',
            'cert': '🛩️ R5 Safety System changes may require FAA-facing certification evidence or equivalent compliance review because they can affect airworthiness, failure handling, and overall system safety assessment.',
            'mitigation': '🧯 For R5, update the hazard analysis, verify fail-safe logic, involve independent reviewers, and avoid bundling unrelated changes into the same certification package.',
            'sustainability': '🌱 Sustainability impact is not ideal because safety changes increase certification work, documentation overhead, and repeated verification. Even so, the change is still recommended because hazard reduction, compliance, and fail-safe integrity take priority over sustainability tradeoffs.'
        },
        'R6': {
            'default': '🧠 R6 Data Processing change affects transformation logic, decision quality, and consistency of outputs consumed by other subsystems. Errors here may propagate quietly before becoming visible at system level.',
            'risk': '⚠️ R6 Data Processing is MEDIUM risk, but it becomes high if algorithm, filtering, or decision logic changes alter assumptions used by safety, control, or communication functions.',
            'cert': '💻 R6 processing changes should preserve strong traceability, requirements alignment, and verification coverage, especially where software outputs influence safety-relevant decisions.',
            'mitigation': '🧪 For R6, use regression datasets, edge-case testing, and interface replay scenarios to confirm outputs remain stable and traceable after the change.',
            'sustainability': '🌱 Sustainability impact is generally positive if the processing change reduces duplicated computation, rework, or maintenance burden. Although short-term testing effort increases, the long-term engineering footprint can improve if the logic becomes cleaner and more robust.'
        },
        'R7': {
            'default': '⚙️ R7 Actuation System change affects command execution, physical response, and closed-loop behavior with flight control. Even localized changes can alter aircraft response characteristics and fault tolerance.',
            'risk': '⚠️ R7 Actuation System is HIGH risk because actuator dynamics directly affect controllability, timing, and recovery behavior under failure or degraded modes.',
            'cert': '🛠️ R7 actuation changes generally require integrated testing with the control chain, including response timing, feedback consistency, redundancy behavior, and degraded-mode performance.',
            'mitigation': '🔧 For R7, verify actuator timing, command saturation behavior, feedback stability, and reconfiguration performance in realistic control scenarios.',
            'sustainability': '🌱 Sustainability impact is moderate because actuation changes may add hardware effort, mechanical retesting, and integration complexity. Even so, the change is justified when it improves reliability or reduces lifecycle maintenance, provided the solution is kept as simple as possible.'
        },
        'R8': {
            'default': '🧭 R8 Navigation change affects reference accuracy, guidance quality, and the trustworthiness of upstream position or route inputs used by connected subsystems. The main concern is hidden propagation of inaccurate guidance information.',
            'risk': '⚠️ R8 Navigation is MEDIUM risk on its own, but it becomes more serious when control or mission functions depend heavily on its outputs. The biggest concern is consistency under degraded or conflicting input conditions.',
            'cert': '🛰️ R8 navigation changes should be checked for sensor-fusion assumptions, route and guidance integrity, and downstream consistency with flight-control and avionics functions.',
            'mitigation': '📍 For R8, validate navigation-source consistency, degraded-signal handling, and cross-check performance against expected guidance behavior before approving the change.',
            'sustainability': '🌱 Sustainability impact is favorable when the navigation update improves guidance accuracy, reduces correction effort, and lowers downstream operational inefficiency. It may require extra verification upfront, but it can reduce long-term waste if complexity is kept under control.'
        }
    }

    intent = 'default'
    if any(k in q_lower for k in ['risk', 'critical', 'safe', 'safety', 'danger', 'hazard']):
        intent = 'risk'
    elif any(k in q_lower for k in ['cert', 'certification', 'faa', 'approval', 'compliance', 'airworthiness']):
        intent = 'cert'
    elif any(k in q_lower for k in ['mitigation', 'mitigate', 'reduce', 'recovery', 'action', 'recommend']):
        intent = 'mitigation'
    elif any(k in q_lower for k in ['sustainability', 'sustainable', 'green', 'co2', 'carbon', 'waste', 'emissions']):
        intent = 'sustainability'

    if req_id:
        return subsystem_responses[req_id][intent]

    keyword_map = {
        'flight control': 'R1',
        'control system': 'R1',
        'sensor': 'R2',
        'sensors': 'R2',
        'power': 'R3',
        'power system': 'R3',
        'comm': 'R4',
        'communication': 'R4',
        'communications': 'R4',
        'safety': 'R5',
        'safety system': 'R5',
        'processing': 'R6',
        'data processing': 'R6',
        'actuation': 'R7',
        'actuator': 'R7',
        'actuators': 'R7',
        'navigation': 'R8',
        'nav': 'R8'
    }

    for k, v in keyword_map.items():
        if k in q_lower:
            return subsystem_responses[v][intent]

    return '🤖 Please ask about a specific requirement or subsystem, such as R1 Flight Control, R5 Safety, R7 Actuation, or R8 Navigation. You can also ask about risk, certification, mitigation, or sustainability.'

def build_decision_output(question, decision):
    q_lower = question.lower().strip() if question else ''
    req_id = None

    for r in REQUIREMENTS.keys():
        if r.lower() in q_lower:
            req_id = r
            break

    keyword_map = {
        'flight control': 'R1',
        'control system': 'R1',
        'sensor': 'R2',
        'sensors': 'R2',
        'power': 'R3',
        'power system': 'R3',
        'comm': 'R4',
        'communication': 'R4',
        'communications': 'R4',
        'safety': 'R5',
        'safety system': 'R5',
        'processing': 'R6',
        'data processing': 'R6',
        'actuation': 'R7',
        'actuator': 'R7',
        'actuators': 'R7',
        'navigation': 'R8',
        'nav': 'R8'
    }

    if not req_id:
        for k, v in keyword_map.items():
            if k in q_lower:
                req_id = v
                break

    next_steps_map = {
        'R1': [
            'Raise a formal change request for the Flight Control subsystem.',
            'Perform control-law impact analysis across sensor and actuator interfaces.',
            'Run regression testing for nominal, degraded, and fail-safe modes.',
            'Prepare certification traceability and verification evidence before implementation.'
        ],
        'R2': [
            'Update the sensor change request and affected calibration baseline.',
            'Re-run calibration and sensor consistency verification.',
            'Validate downstream interfaces with flight control, navigation, and processing.',
            'Document any data-quality deviations before approval.'
        ],
        'R3': [
            'Review the power architecture change against redundancy and load margins.',
            'Validate emergency-power continuity and degraded-mode behavior.',
            'Re-test brownout, failover, and recovery scenarios.',
            'Approve implementation only after power-budget evidence is complete.'
        ],
        'R4': [
            'Review the communication-interface change request.',
            'Validate protocol timing, retry logic, and timeout handling.',
            'Test connected systems for stale-data and dropped-message behavior.',
            'Freeze the updated interface-control assumptions before release.'
        ],
        'R5': [
            'Open a formal safety-impact review and update the hazard assessment.',
            'Initiate certification/compliance review for the Safety subsystem.',
            'Re-verify fail-safe behavior and safety interlocks.',
            'Obtain human approval before implementation and release.'
        ],
        'R6': [
            'Review the processing logic change against current requirements traceability.',
            'Run regression datasets and edge-case test scenarios.',
            'Validate downstream outputs consumed by control and communication functions.',
            'Approve the change only after verification evidence is complete.'
        ],
        'R7': [
            'Review the actuator change against timing and response requirements.',
            'Test feedback consistency, saturation behavior, and degraded modes.',
            'Validate integration with the flight-control chain.',
            'Approve implementation after closed-loop verification is complete.'
        ],
        'R8': [
            'Review the navigation change and impacted guidance assumptions.',
            'Validate degraded-signal and conflicting-source scenarios.',
            'Cross-check outputs against connected control and mission functions.',
            'Approve the change after route and guidance integrity tests pass.'
        ]
    }

    if decision == 'proceed':
        if req_id and req_id in next_steps_map:
            steps = next_steps_map[req_id]
            return html.Div([
                html.P('✅ Decision: Proceed with Change', style={'fontWeight': 700, 'color': '#166534', 'marginBottom': 10}),
                html.P(f'Recommended next steps for {req_id}:', style={'fontWeight': 600, 'marginBottom': 8}),
                html.Ol([html.Li(step, style={'marginBottom': 6}) for step in steps],
                        style={'paddingLeft': '20px', 'lineHeight': 1.6})
            ], style={
                'background': 'rgba(255,255,255,0.12)',
                'padding': '16px',
                'borderRadius': '12px',
                'marginTop': '8px'
            })

        return html.Div([
            html.P('✅ Decision: Proceed with Change', style={'fontWeight': 700, 'color': '#166534', 'marginBottom': 10}),
            html.Ol([
                html.Li('Raise a formal change request.'),
                html.Li('Perform subsystem impact analysis.'),
                html.Li('Run verification and regression testing.'),
                html.Li('Obtain approval before implementation.')
            ], style={'paddingLeft': '20px', 'lineHeight': 1.6})
        ], style={
            'background': 'rgba(255,255,255,0.12)',
            'padding': '16px',
            'borderRadius': '12px',
            'marginTop': '8px'
        })

    if decision == 'reject':
        return html.Div([
            html.P('❌ Decision: Do Not Proceed', style={'fontWeight': 700, 'color': '#991b1b', 'marginBottom': 10}),
            html.P(
                'Recommended action: keep the current baseline, document the rejection rationale, and request further human review if the change becomes necessary later.',
                style={'lineHeight': 1.6}
            )
        ], style={
            'background': 'rgba(255,255,255,0.12)',
            'padding': '16px',
            'borderRadius': '12px',
            'marginTop': '8px'
        })

    return no_update

app.layout = html.Div([
    html.Div([
        html.H1('Requirement Change Impact Map',
                style={
                    'textAlign': 'center',
                    'color': '#1a202c',
                    'fontFamily': 'Inter',
                    'fontWeight': 700,
                    'fontSize': '42px',
                    'letterSpacing': '-0.02em',
                    'marginBottom': '10px'
                }),
        html.P('',
               style={
                   'textAlign': 'center',
                   'color': '#4a5568',
                   'fontFamily': 'Inter',
                   'fontWeight': 400,
                   'fontSize': '18px'
               })
    ], style={'padding': '40px 0 20px 0'}),

    html.Div([
        html.Div([
            html.Div('🕸️ Impact Network Map', style=SECTION_TITLE_STYLE),
            dcc.Graph(
                id='spider-web',
                figure=create_spider_web(),
                style={'height': '820px', 'width': '100%'},
                config={'displayModeBar': False}
            )
        ], style=CARD_STYLE)
    ], style={
        'width': '68%',
        'display': 'inline-block',
        'verticalAlign': 'top'
    }),

        html.Div([
            html.Div([
                html.Div('📊 Impact Summary', style=SECTION_TITLE_STYLE),
                html.Div(id='impact-panel', style={'fontFamily': 'Inter'})
            ], style={**CARD_STYLE, 'marginBottom': '20px'}),

            html.Div([
                html.Div('💬 AI Assistant', style=SECTION_TITLE_STYLE),

                dcc.Textarea(
                    id='chat-input',
                    placeholder="Ask: 'What if we change R1?' 'Risks?' 'Sustainability impact of R5?'",
                    style={
                        'width': '100%',
                        'height': 110,
                        'padding': 16,
                        'borderRadius': 12,
                        'border': '1.5px solid #cbd5e0',
                        'fontFamily': 'Inter',
                        'fontSize': 14,
                        'resize': 'none',
                        'background': '#f8fafc',
                        'boxSizing': 'border-box'
                    }
                ),

                html.Button(
                    '🤖 Analyze with AI',
                    id='chat-btn',
                    n_clicks=0,
                    style={
                        'width': '100%',
                        'padding': 14,
                        'marginTop': '12px',
                        'background': 'linear-gradient(135deg, #2563eb, #1d4ed8)',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': 12,
                        'fontSize': 15,
                        'fontWeight': 700,
                        'fontFamily': 'Inter',
                        'cursor': 'pointer',
                        'boxShadow': '0 6px 18px rgba(37,99,235,0.35)'
                    }
                ),

                html.Div(
                    id='chat-response',
                    style={
                        'marginTop': 18,
                        'padding': 20,
                        'background': 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                        'borderRadius': 16,
                        'color': 'white',
                        'minHeight': 110,
                        'fontFamily': 'Inter',
                        'fontSize': 14,
                        'lineHeight': 1.6,
                        'boxShadow': '0 10px 25px rgba(79,70,229,0.28)'
                    }
                ),

                html.Div(id='decision-output')
            ], style=CARD_STYLE)
        ], style={
            'width': '30%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'paddingLeft': 18,
            'fontFamily': 'Inter'
        })
])
@callback(
    [Output('spider-web', 'figure'), Output('impact-panel', 'children')],
    Input('spider-web', 'clickData')
)
def update_spider(clickData):
    selected = None
    if clickData and clickData['points']:
        selected = clickData['points'][0]['text']

    fig = create_spider_web(selected)

    if not selected:
        return fig, html.Div([
            html.H2('👆 Click Any Node',
                   style={'color': '#a0aec0', 'textAlign': 'center', 'fontFamily': 'Inter', 'fontWeight': 600}),
            html.P('Watch interconnected systems & subsystems light up with impact analysis!',
                   style={'textAlign': 'center', 'fontSize': 16, 'fontFamily': 'Inter'})
        ])

    metrics = IMPACT_METRICS[selected]
    affected_edges = [e for e in EDGES if e[0] == selected or e[1] == selected]

    return fig, html.Div([
        html.H1(f'🚨 {selected} Analysis',
               style={
                   'color': '#e53e3e',
                   'textAlign': 'center',
                   'fontFamily': 'Inter',
                   'fontWeight': 700,
                   'fontSize': '24px',
                   'marginBottom': '6px'
               }),
        html.H2(REQUIREMENTS[selected]['name'],
               style={
                   'textAlign': 'center',
                   'fontFamily': 'Inter',
                   'fontWeight': 500,
                   'fontSize': '18px',
                   'marginTop': '0',
                   'marginBottom': '10px'
               }),
        html.Hr(style={'borderColor': '#e2e8f0'}),

        html.Div([
            html.Div([
                html.H4('💰 Cost Overrun', style={'color': '#c53030', 'fontFamily': 'Inter', 'marginBottom': '6px'}),
                html.H2(metrics['cost'], style={'fontSize': '28px', 'fontFamily': 'Inter', 'margin': '0'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px 12px', 'verticalAlign': 'top'}),

            html.Div([
                html.H4('⏱️ Schedule', style={'color': '#dd6b20', 'fontFamily': 'Inter', 'marginBottom': '6px'}),
                html.H2(metrics['time'], style={'fontSize': '28px', 'fontFamily': 'Inter', 'margin': '0'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px 12px', 'verticalAlign': 'top'}),
        ], style={
            'background': 'rgba(255,255,255,0.7)',
            'borderRadius': 12,
            'margin': '12px 0',
            'padding': '6px 4px'
        }),

        html.Div([
            html.Div([
                html.H4('🤖 AI Confidence', style={'color': '#38a169', 'fontFamily': 'Inter', 'marginBottom': '6px'}),
                html.H2(metrics['confidence'], style={'fontSize': '28px', 'fontFamily': 'Inter', 'margin': '0'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px 12px', 'verticalAlign': 'top'}),

            html.Div([
                html.H4('⚠️ Risk Level', style={'color': '#c53030', 'fontFamily': 'Inter', 'marginBottom': '6px'}),
                html.H2(metrics['risk'], style={'fontSize': '24px', 'color': '#e53e3e', 'fontFamily': 'Inter', 'margin': '0'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px 12px', 'verticalAlign': 'top'}),
        ], style={
            'background': 'rgba(255,255,255,0.7)',
            'borderRadius': 12,
            'margin': '12px 0',
            'padding': '6px 4px'
        }),

        html.Hr(style={'borderColor': '#e2e8f0'}),
        html.H3(f'🔗 {len(affected_edges)} Impact Links:', style={'fontFamily': 'Inter', 'fontWeight': 600, 'marginBottom': '10px'}),
        html.Div([
            html.Div(
                f'➤ {e[2]} ({e[0]}-{e[1]})',
                style={
                    'background': 'rgba(229,62,62,0.1)',
                    'padding': 12,
                    'margin': '6px 0',
                    'borderRadius': 10,
                    'borderLeft': '4px solid #e53e3e',
                    'fontFamily': 'Inter'
                }
            )
            for e in affected_edges
        ])
    ])

@callback(
    Output('chat-response', 'children'),
    [Input('chat-btn', 'n_clicks')],
    [State('chat-input', 'value')],
    prevent_initial_call=True
)
def ai_chat(n_clicks, question):
    response = build_chat_response(question)

    return html.Div([
        html.P('🤖 AI Response:', style={'fontWeight': 600, 'marginBottom': 10}),
        html.P(response, style={'lineHeight': 1.6, 'whiteSpace': 'pre-line'}),
        html.Hr(style={'borderColor': 'rgba(255,255,255,0.3)'}),
        html.P('👤 Human Decision Required', style={'fontWeight': 500}),
        html.Div([
            html.Button(
                '✅ Proceed with Change',
                id='proceed-btn',
                n_clicks=0,
                style={
                    'backgroundColor': '#16a34a',
                    'color': 'white',
                    'border': 'none',
                    'padding': '12px 18px',
                    'borderRadius': '10px',
                    'marginRight': '12px',
                    'fontWeight': 600,
                    'cursor': 'pointer'
                }
            ),
            html.Button(
                '❌ Do Not Proceed',
                id='reject-btn',
                n_clicks=0,
                style={
                    'backgroundColor': '#dc2626',
                    'color': 'white',
                    'border': 'none',
                    'padding': '12px 18px',
                    'borderRadius': '10px',
                    'fontWeight': 600,
                    'cursor': 'pointer'
                }
            )
        ], style={'marginTop': 10, 'marginBottom': 12}),
        html.Div(id='decision-output')
    ])

@callback(
    Output('decision-output', 'children'),
    [Input('proceed-btn', 'n_clicks'),
     Input('reject-btn', 'n_clicks')],
    [State('chat-input', 'value')],
    prevent_initial_call=True
)
def handle_human_decision(proceed_clicks, reject_clicks, question):
    triggered = ctx.triggered_id
    if not triggered:
        return no_update

    if triggered == 'proceed-btn':
        return build_decision_output(question, 'proceed')
    if triggered == 'reject-btn':
        return build_decision_output(question, 'reject')

    return no_update

if __name__ == '__main__':
    print('🕷️ MODERN SPIDER WEB IMPACT ANALYZER')
    print('✅ Inter font + Premium gradients + Professional design!')
    app.run(debug=False, port=8050)