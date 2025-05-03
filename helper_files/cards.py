import dash_bootstrap_components as dbc

from dash import Dash, dcc, html
import plotly.express as px
from helper_files.config import variables, heatmap_fig, state_week

info_card = dbc.Card(
    [
        html.Div([
            html.H1("COVID-19 & Mental Health Dashboard", style={'textAlign': 'center'}),
            html.H2("Background & Thesis", style={'marginTop': '1rem'}),
            dcc.Markdown(
                    """
                    **Mission:** To illustrate how mental-health symptoms in the U.S. population  
                    tracked alongside the COVID-19 pandemic from April 2020 through October 2023.

                    ### Pandemic Timeline
                    - **Dec 2019:** First cases reported in Wuhan, China  
                    - **Mar 2020:** U.S. declares national emergency; stay-at-home orders begin  
                    - **Winter 2020–21:** First major wave peaks; vaccines roll out  
                    - **Summer 2021:** Delta variant surge  
                    - **Winter 2021–22:** Omicron variant surge  
                    - **…through Oct 2023** when this data collection ends  

                    ### Why Mental Health?
                    The pandemic created unprecedented stressors—social isolation, economic insecurity,  
                    fear of illness—that have been linked to increases in anxiety and depression.

                    ### Data & Approach
                    We use the Census Household Pulse Survey (“HPS”), which interviews tens of thousands  
                    of Americans each week on topics including anxiety, worry, loss of interest, and  
                    feeling down. In this dashboard you will see:
                    1. **Timeline tab:** week-by-week averages of self-reported symptoms  
                    2. **Map tab:** geographic variation in symptom prevalence  

                    ### Thesis Statement
                    > Mental-health symptoms rose and fell in step with the pandemic waves  
                    across time and differed significantly by state.

                    ### How to Use This App
                    - Switch to the **Timeline** tab to explore trends over time.  
                    - Go to **Geography** to see state-level differences.  
                    - Visit **Correlation** to compare symptom measures against each other.
                    """
            )

        ])

    ], style={'padding': '20px', 'maxWidth': '800px', 'margin': 'auto', 'lineHeight': '1.6rem'}
)

timeline_card = dbc.Card([
                        dbc.CardHeader(html.H5("Weekly Mean Symptom Scores")),
                        dbc.CardBody([
                            dcc.Markdown(
                                """
                                **Household Pulse Survey** respondents reported how often they experienced four key symptoms each week from **April 2020 to October 2023**:

                                - **Anxiety**  
                                - **Feeling down** (Depression)  
                                - **Loss of interest**  
                                - **Excessive worry**

                                This chart shows the **weekly average scores** for each symptom on a **1–4 scale**, where:

                                > - **Not at all** = 1  
                                > - **Several days** = 2  
                                > - **More than half the days** = 3  
                                > - **Nearly every day** = 4  

                                Use the **checkboxes below** to select which symptoms to display.
                                """,
                                style={"lineHeight": "1.6", "marginBottom": "1rem"}
                            ),
                            dcc.Checklist(
                                id="symptom-selector",
                                options=[{"label": s.title(), "value": s} for s in variables],
                                value=variables,          # list of selected items is fine here
                                inline=False,             # or True if you want them on one line
                                inputStyle={"marginRight": "5px", "marginLeft": "10px"}
                            )

                        ])
                    ], className="h-100 mb-4")


# ─── Heatmap Card ─────────────────────────────────────────────────────────────
heatmap_card = dbc.Card([
    dbc.CardHeader(html.H5("Symptom Correlation Heatmap")),
    dbc.CardBody([
        dcc.Graph(figure=heatmap_fig, config={"displayModeBar": False}),
        dcc.Markdown(
            """
            This is a **correlation heatmap** showing the pairwise *Pearson* **r** values between
            the four symptom scores: **ANXIOUS**, **DOWN** (depression), **INTEREST** (loss of interest),
            and **WORRY**.

            - **Diagonal cells** are all 1.00, since each symptom is perfectly correlated with itself.  
            - **Off-diagonal cells** show how closely two different symptoms move together:
              - *Anxious vs. Worry* = 0.99 (very dark orange)  
              - *Anxious vs. Down*  = 0.97 (purple)  
              - *Interest vs. Worry* = 0.95 (dark blue)  
              …and so on for each pair.

            Because most correlations exceed **0.95**, higher anxiety scores tend to coincide
            with higher depression, greater loss of interest, and more excessive worry.
            """,
            style={"lineHeight": "1.5", "marginTop": "1rem"}
        )
    ])
], className="mb-4")


weeks = state_week["WEEK"].unique()
min_w, max_w = weeks.min(), weeks.max()

# build marks at min, max, and every 5 weeks
marks = {int(min_w): str(int(min_w)), int(max_w): str(int(max_w))}
for w in weeks:
    if (w - min_w) % 5 == 0:
        marks[int(w)] = str(int(w))

geography_card = dbc.Card([
        dbc.CardBody([
          dcc.Markdown(
            """
            This map shows the **average anxiety score** (1–4 scale) for each state  
            over the selected weeks. Darker shades indicate higher anxiety.
            """,
            style={"marginBottom":"1rem"}
          ),
          html.Div(style={"display":"flex","alignItems":"center","gap":"1rem"}, children=[
            html.Button("▶ Play", id="play-button", n_clicks=0),
              dbc.Col(
            dcc.RangeSlider(
              id="geo-week-range",
              min=min_w, max=max_w,
              value=[min_w, max_w],
              marks=marks,
              step=1,
              allowCross=False,
              tooltip={"placement":"bottom"}
            ), width= 8
            ),
            dcc.Interval(id="play-interval", interval=200, disabled=True)
          ])
        ])
      ])

