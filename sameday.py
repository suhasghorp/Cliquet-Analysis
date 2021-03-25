import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc




'''dbc.Row([dbc.Col(id='card1', children=[card_spx], md=3),
                     dbc.Col(id='card2', children=[card_rut], md=3),
                     dbc.Col(id='card3', children=[card_efa], md=3)]),'''

content = html.Div([
            dbc.Row(dbc.Col(html.H1("Cliquet Analysis"),style={'text-align': 'center'}
                                #width={'size': 6, 'offset': 3},
                                ),
                        ),
            dbc.Row(dbc.Col(html.H3("Same Day"),
                                width={'size': 2},
                                ),
                        ),


            html.Br(),

            dcc.Dropdown(id="sd_select_asset",
                         options=[
                             {"label": "RUT", "value": ".RUT"},
                             {"label": "SPX", "value": ".SPX"},
                             {"label": "EFA", "value": "EFA.P"}],
                         multi=False,
                         value=".RUT",
                        className="dash-bootstrap",
                         style={'width': "40%" }
                         ),

            #html.Div(id='sd_output_container', children=[]),
            html.Br(),

            dcc.Graph(id='sd_graph', figure={})
        ])


