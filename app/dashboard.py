# dashboard.py

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, callback_context
from dash.dependencies import Input, Output, State
import plotly.express as px

from helper_files.cards import info_card, heatmap_card, timeline_card, geography_card, min_w, max_w
from helper_files.config import variables, time_long, time_metrics, event_weeks, state_week, misc_metrics

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
server = app.server

# ─── Dashboard Tab ─────────────────────────────────────────────────────────────
dashboard_tab = dcc.Tab(
    label="Dashboard", value="dashboard-tab", children=[
        dbc.Container(fluid=True, style={"padding":"1rem"}, children=[

            # Row: explanation & controls (left) + main chart (right)
            dbc.Row([
                dbc.Col(
                    timeline_card,
                    width=5
                ),
                dbc.Col(
                    dbc.Card(dbc.CardBody(
                        dcc.Graph(id="time-series-chart")
                    ), className="h-100 mb-4"),
                    width=7
                )
            ]),

            html.Div(style={"height": "2rem"}),

            # Row: heatmap card
            dbc.Row([
                dbc.Col(
                    heatmap_card,
                    width=12
                )
            ])

        ])
    ]
)

geography_tab = dcc.Tab(
    label="Geography", value="geography-tab", children=[
        dbc.Container(fluid=True, style={"padding":"1rem"}, children=[

            # Top: choropleth map card
            dbc.Card([
                dbc.CardHeader(html.H5("State‐by‐State Anxiety Over Time")),
                dbc.CardBody(
                    dcc.Graph(id="choropleth-map")
                )
            ], className="mb-4"),

            # Bottom: explanation + week slider
            geography_card,
            html.Div(style={"height": "4rem"}),

        ])
    ]
)



corr_tab = dcc.Tab(label="Correlation", value="correlation-tab", children=[

    # Existing heatmap card
    html.Div(heatmap_card, style={"marginBottom":"2rem"}),

    # New: multi-line trends card
    dbc.Card([
        dbc.CardHeader(html.H5("Weekly Mean: Current Food Sufficiency")),
        dbc.CardBody([
            dcc.Graph(id="food-sufficiency-chart")
        ])
    ], className="mb-4")
])

# … assemble tabs including corr_tab …


tabs = dcc.Tabs(id="main-tabs", value="introduction", children=[
    dcc.Tab(label="Introduction", value="introduction", children=[info_card]),
    dashboard_tab,
    geography_tab,
])

app.layout = dbc.Container([
    dcc.Store(id="mode_store", data="individual"),
    dbc.Row(dbc.Col(
        [html.H2("The Impacts of COVID-19 on Mental Health Dashboard",
                className="text-center bg-primary text-white p-2"),
        html.H5("Brevin Tating - CS150", className="text-center")]
    )),
    dbc.Row(dbc.Col(tabs, width=12, className="mt-4"))
], fluid=True)

# ─── Callback for Updating Time-Series Chart ────────────────────────────────────
@app.callback(
    Output("time-series-chart", "figure"),
    Input("symptom-selector", "value")
)
def update_time_series(selected_symptoms):
    if not selected_symptoms:
        return px.line().update_layout(
            title="No symptom selected",
            xaxis_title="Week",
            yaxis_title="Mean Score"
        )

    dff = time_long[time_long["Symptom"].isin(selected_symptoms)]
    fig = px.line(
        dff, x="WEEK", y="MeanScore", color="Symptom",
        markers=True, title="Weekly Mean Symptom Scores"
    )
    fig.update_layout(
        xaxis_title="Survey Week",
        yaxis_title="Mean Score",
        yaxis_range=[1, 4],
        margin=dict(l=40, r=20, t=60, b=40)
    )
    for wk, label in event_weeks.items():
        fig.add_vline(x=wk, line_dash="dash", line_color="gray")
        fig.add_annotation(
            x=wk, y=1.0, yref="paper",
            text=label, textangle=90, showarrow=False,
            xanchor="left", font=dict(size=10, color="gray")
        )
    return fig

# ─── 4) Callback to update the choropleth ──────────────────────────────────────
@app.callback(
    Output("choropleth-map", "figure"),
    Input("geo-week-range", "value")
)
def update_map(week_range):
    start, end = week_range
    df_window = (
        state_week
        .loc[state_week["WEEK"].between(start, end)]
        .groupby("state_abbrev")["ANXIOUS"].mean()
        .reset_index()
    )
    fig = px.choropleth(
        df_window,
        locations="state_abbrev", locationmode="USA-states",
        color="ANXIOUS", range_color=[1,4],
        scope="usa",
        labels={"ANXIOUS":"Mean Anxiety"}
    )
    fig.update_layout(
        title_text=f"Avg Anxiety by State — Weeks {start}–{end}",
        margin=dict(l=20,r=20,t=40,b=20)
    )
    return fig

@app.callback(
    Output("geo-week-range", "value"),
    Output("play-interval", "disabled"),
    Input("play-button", "n_clicks"),
    Input("play-interval", "n_intervals"),
    State("geo-week-range", "value")
)
def animate_slider(n_clicks, n_intervals, week_range):
    ctx = callback_context
    if not ctx.triggered:
        # initialization
        return week_range, True

    trigger = ctx.triggered[0]["prop_id"].split(".")[0]

    # On Play button: reset to full range start
    if trigger == "play-button":
        return [min_w, min_w], False

    # On each Interval tick: advance upper bound
    start, end = week_range
    if end >= max_w:
        return [start, end], True
    return [start, end + 1], False




if __name__ == "__main__":
    app.run(debug=True)
