import pandas as pd
import plotly.express as px  # (version 4.7.0)
from azure.storage.blob import BlobServiceClient

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from io import StringIO
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

'''
Steps for deploying to Azure web app service with KeyVault
First create a web app service in portal with name cliquet-analysis
Next steps are run in powershell

az ad sp create-for-rbac --name https://cliquet-analysis.azurewebsites.net --skip-assignment

this outputs following important IDs
"appId": "xxx",
"displayName": "cliquet-analysis.azurewebsites.net",
"name": "https://cliquet-analysis.azurewebsites.net",
"password": "xxx",
"tenant": "xxx"

For running locally in pycharm, set following 3 env variables in debug/run configuration
AZURE_CLIENT_ID=appId w/o quotes
AZURE_CLIENT_SECRET=password w/o quotes
AZURE_TENANT_ID=tenant w/o quotes
VAULT_URL=vault_url_you_know

Before deploying to azure, 

go into cliquet-analysis webapp Identity, make sure System Assigned is turned on
In KeyVault access policies, add access policy, select get kv permissions and select principal

then execute following in PS
az keyvault set-policy --name kvderivops --spn appId_from_above --secret-permissions get

'''

vault_url = os.environ['VAULT_URL']

dash_app = dash.Dash(__name__)
app = dash_app.server
dash_app.config.suppress_callback_exceptions = True

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=vault_url, credential=credential)
connection_string = secret_client.get_secret("CONNECTION-STRING").value

CONTAINERNAME= "cliquet-analysis-container"
BLOBNAME= "Cliquet_sameday_2021-03-15.csv"

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
blob_client = blob_service_client.get_blob_client(container=CONTAINERNAME, blob=BLOBNAME)
blobstring = blob_client.download_blob()
sd_df = pd.read_csv(StringIO(blobstring.content_as_text()))
sd_df.reset_index(inplace=True)

BLOBNAME= "Cliquet_nextday_2021-03-15.csv"
blob_client = blob_service_client.get_blob_client(container=CONTAINERNAME, blob=BLOBNAME )
blobstring = blob_client.download_blob()
nd_df = pd.read_csv(StringIO(blobstring.content_as_text()))
nd_df.reset_index(inplace=True)

def create_card(title, content):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H4(title),
                html.Br(),
                html.H4(content),
                html.Br()
            ]
        ),
        color="info", inverse=True
    )
    return card

card_spx = create_card("SPX", len(sd_df[sd_df["assetId"] == ".SPX"].index))
card_rut = create_card("RUT", len(sd_df[sd_df["assetId"] == ".RUT"].index))
card_efa = create_card("EFA.P", len(sd_df[sd_df["assetId"] == "EFA.P"].index))


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    }

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar"),
        html.Hr(),
        html.P(
            "Lets do some cliquets"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Same Day Analysis", href="/sameday", active="exact"),
                dbc.NavLink("Next Day Analysis", href="/nextday", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

dash_app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@dash_app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            dbc.Row(dbc.Col(html.H1("This is the content for home page"),style={'text-align': 'center'})),
            html.Br(),
            dbc.Row([dbc.Col(id='card1', children=[card_spx], md=3),
                     dbc.Col(id='card2', children=[card_rut], md=3),
                     dbc.Col(id='card3', children=[card_efa], md=3)])
        ])
    elif pathname == "/sameday":
        import sameday
        return [sameday.content]
    elif pathname == "/nextday":
        import nextday
        return [nextday.content]


# ------------------------------------------------------------------------------
# App layout
@dash_app.callback(
    Output(component_id='sd_graph', component_property='figure'),
    [Input(component_id='sd_select_asset', component_property='value')]
)
def update_sd_graph(asset_selected):
    print(asset_selected)
    print(type(asset_selected))

    #container = "The Asset chosen by user was: {}".format(asset_selected)

    dff = sd_df.copy()
    dff = dff[dff["assetId"] == asset_selected]

    fig = px.scatter(
        data_frame=dff,
        x="deltaT1",
        y="gammaT1",
        color="Book",
        template="plotly_dark",
        hover_data=["deltaT1", "gammaT1"]
    )

    return fig




# ------------------------------------------------------------------------------
if __name__ == '__main__':
    dash_app.run_server(debug=True)
