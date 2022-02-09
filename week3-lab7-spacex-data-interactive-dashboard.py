# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        dcc.Dropdown(
            id="site_dropdown",
            options=[{"label": "All Sites", "value": "ALL"}]
            + [{"label": i, "value": i} for i in spacex_df["Launch Site"].unique()],
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success_pie_chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        # dcc.RangeSlider(id='payload-slider',...)
        dcc.RangeSlider(
            id="payload_slider",
            min=0,
            max=10000,
            step=1000,
            marks={
                0: "0",
                2000: "2000",
                4000: "4000",
                6000: "6000",
                8000: "8000",
                10000: "10000",
            },
            value=[min_payload, max_payload],
        ),
        html.Br(),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success_payload_scatter_chart")),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id="success_pie_chart", component_property="figure"),
    Input(component_id="site_dropdown", component_property="value"),
)
def get_pie_chart(site_dropdown):
    filtered_df = spacex_df
    if site_dropdown == "ALL":
        fig = px.pie(
            filtered_df,
            values="class",
            names="Launch Site",
            title="Total Success Launches by Site!",
        )
        return fig
    else:
        fig = px.pie(
            filtered_df[filtered_df["Launch Site"] == site_dropdown]
            .groupby("class")
            .size()
            .reset_index(name="counts"),
            values="counts",
            names="class",
            title="Total Success Launches for site " + site_dropdown,
        )
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success_payload_scatter_chart", component_property="figure"),
    [
        Input(component_id="site_dropdown", component_property="value"),
        Input(component_id="payload_slider", component_property="value"),
    ],
)
def get_scatter_chart(site_dropdown, payload_slider):
    filtered_df = spacex_df  # [spacex_df['Payload Mass (kg)'] >= payload_slider[0] & spacex_df['Payload Mass (kg)'] <= max_payload]
    low, high = payload_slider
    mask = (filtered_df["Payload Mass (kg)"] >= low) & (
        filtered_df["Payload Mass (kg)"] <= high
    )
    if site_dropdown == "ALL":
        fig = px.scatter(
            filtered_df[mask],
            y="class",
            x="Payload Mass (kg)",
            color="Booster Version Category",
            title="Correlation between Payload and Success for All Site",
        )
        return fig
    else:
        fig = px.scatter(
            filtered_df[(filtered_df["Launch Site"] == site_dropdown) & mask],
            y="class",
            x="Payload Mass (kg)",
            color="Booster Version Category",
            title="Correlation between Payload and Success for site " + site_dropdown,
        )
        return fig


# Run the app
if __name__ == "__main__":
    app.run_server()
