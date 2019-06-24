import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('df_for_dash.csv')

available_indicators = ['sales', 'covers', 'ppa', 'temperature', 'apparent_temperature', 'humdiity', 'precip_prob']

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='sales'
            )
        ],
        style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='covers'
            )
        ],style={'width': '30%', 'float': 'left', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value')])
     
def update_graph(xaxis_column_name, yaxis_column_name,
        ):
    
    dff = df

    return {
        'data': [go.Scatter(
            x=dff[dff['variable'] == xaxis_column_name]['value'],
            y=dff[dff['variable'] == yaxis_column_name]['value'],
            text=dff[dff['variable'] == yaxis_column_name]['date'],

            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)