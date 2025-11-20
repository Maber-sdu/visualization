import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# --------------------------------------
# Load data
# --------------------------------------
df = pd.read_csv("global_leader_ideologies.csv")

# Keep only relevant columns
df = df[["year", "hog_ideology"]]

# Normalize ideology names
df["hog_ideology"] = df["hog_ideology"].str.lower()

# Map ideology to a simpler coded version
valid_ideologies = ["leftist", "centrist", "rightist"]

# --------------------------------------
# Prepare Dash App
# --------------------------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Political Ideology Trends Over Time", style={"textAlign": "center"}),

    # Dropdown to pick ideology
    html.Label("Select Ideology:", style={"fontSize": 18}),
    dcc.Dropdown(
        id="ideology_selector",
        options=[{"label": ide.capitalize(), "value": ide} for ide in valid_ideologies],
        value="leftist",
        clearable=False,
        style={"width": "40%"}
    ),

    dcc.Graph(id="trend_chart")
])

# --------------------------------------
# Callbacks
# --------------------------------------
@app.callback(
    Output("trend_chart", "figure"),
    Input("ideology_selector", "value")
)
def update_chart(selected_ideology):

    # Filter and count for each year
    filtered = df[df["hog_ideology"] == selected_ideology]
    yearly_counts = filtered.groupby("year").size().reset_index(name="count")

    # Bar chart
    fig = px.bar(
        yearly_counts,
        x="year",
        y="count",
        title=f"Number of {selected_ideology.capitalize()} Governments Over Time",
        labels={"count": "Number of Countries"},
        opacity=0.7
    )

    # Trend line overlay
    fig.add_traces(px.line(
        yearly_counts,
        x="year",
        y="count"
    ).data)

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Count",
        template="plotly_white"
    )

    return fig


# --------------------------------------
# Run the app
# --------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
