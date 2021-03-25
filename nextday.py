import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import application

content = html.Div([
    dbc.Row(dbc.Col(html.H1("Cliquet Analysis"), style={'text-align': 'center'}
                    # width={'size': 6, 'offset': 3},
                    ),
            ),
    dbc.Row(dbc.Col(html.H3("Next Day"),
                    width={'size': 2},
                    ),
            ),


    html.Div(id='nd_output_container', children=[]),
    html.Br(),

    dcc.Graph(id='bargraph',
             figure=px.box(
            data_frame=application.nd_df,
            x="CP",
            y="Px_diff",
            points="all",
            template="plotly_dark",
            #range_y=[-0.04, 0.04],
            #barmode="group",
            color="Underlying"
        ))
])


