import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)

df = pd.read_csv("Cliquet_sameday_2021-03-15.csv")
df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Same Day Analysis", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_asset",
                 options=[
                     {"label": "RUT", "value": ".RUT"},
                     {"label": "SPX", "value": ".SPX"},
                     {"label": "EFA.P", "value": "EFA.P"}],
                 multi=False,
                 value=".RUT",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_map', figure={})
])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_map', component_property='figure')],
    [Input(component_id='select_asset', component_property='value')]
)
def update_graph(asset_selected):
    print(asset_selected)
    print(type(asset_selected))

    container = "The Asset chosen by user was: {}".format(asset_selected)

    dff = df.copy()
    dff = dff[dff["assetId"] == asset_selected]

    fig = px.scatter(
        data_frame=dff,
        x="deltaT1",
        y="gammaT1",
        color="Book",
        hover_data=["deltaT1", "gammaT1"]
    )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
