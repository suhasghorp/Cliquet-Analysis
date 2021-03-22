import pandas as pd
import plotly.express as px  # (version 4.7.0)
from azure.storage.blob import BlobServiceClient

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from io import StringIO


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#STORAGEACCOUNTNAME= "sgderivops"
#STORAGEACCOUNTKEY= "juXnmJdznmjBb3LuNZMKIcv3hC7ap5ub6ROnPOEA3pXK4tYbRkt7eUxb86pSuIoorJUOPqyeCxVAko081nGGVg=="
#LOCALFILENAME= "sameday.csv"
CONTAINERNAME= "cliquet-analysis-container"
BLOBNAME= "Cliquet_sameday_2021-03-15.csv"
CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=sgderivops;AccountKey=juXnmJdznmjBb3LuNZMKIcv3hC7ap5ub6ROnPOEA3pXK4tYbRkt7eUxb86pSuIoorJUOPqyeCxVAko081nGGVg==;EndpointSuffix=core.windows.net"

blob_service_client = BlobServiceClient.from_connection_string(conn_str=CONNECTION_STRING)
blob_client = blob_service_client.get_blob_client(container=CONTAINERNAME, blob=BLOBNAME)
blobstring = blob_client.download_blob()
df = pd.read_csv(StringIO(blobstring.content_as_text()))
df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1("Cliquet Analysis"),style={'text-align': 'center'}
                        #width={'size': 6, 'offset': 3},
                        ),
                ),
    dbc.Row(dbc.Col(html.H3("Same Day"),
                        width={'size': 2},
                        ),
                ),
    #html.H1("Same Day Analysis", style={'text-align': 'center'}),

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
