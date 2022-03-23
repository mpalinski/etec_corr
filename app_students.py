
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_dangerously_set_inner_html
import dash_bootstrap_components as dbc

# external_stylesheets = [dbc.themes.SUPERHERO]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df_stud=pd.read_csv('./corr_students.csv')

available_indicators = df_stud['Indicator Name'].unique()
available_countries = df_stud['Country Name'].unique()

app.layout = html.Div([
    html.Div([
    html.H1('TIMSS 2019: Correlations'),

    html.Div(

    [html.H4('country'),
        dcc.Dropdown(
            id='crossfilter-country-column',
            options=[{'label': i, 'value': i} for i in available_countries],
            value='Saudi Arabia'
        ),
        dcc.RadioItems(
            id='crossfilter-country-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            labelStyle={'display': 'inline-block'}
        )
    ],
    style={'width': '20%', 'display': 'inline-block'}),

        html.Div(

        [html.H4('x axis'),
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Home Resources for Learning'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '20%', 'display': 'inline-block'}),

        html.Div([

        html.H4('y axis'),
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Math'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '20%','display': 'inline-block'})

    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        # 'padding': '10px 5px'
    }),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter-stud',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '60%', 'display': 'block', 'padding': '0 0 0', "margin-left": "auto",
            "margin-right": "auto",}),
            html.Br(),

    html.Div([html.P(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(''))],id='stats_stud', style={'display': 'block','align':'center' ,'marginLeft': 'auto', 'marginRight': 'auto'})


])

@app.callback(
    Output('crossfilter-indicator-scatter-stud', 'figure'),
    [Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-country-column', 'value'),
     Input('crossfilter-xaxis-type', 'value'),
     Input('crossfilter-yaxis-type', 'value'),
     ])


def update_graph(xaxis_column_name, yaxis_column_name, country_column_name,
                 xaxis_type, yaxis_type):

    dff=df_stud[df_stud['Country Name']==country_column_name]
    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['idstud'], marginal_x='histogram',marginal_y='histogram',
            trendline='ols', template="plotly_white"
)
    fig.update_traces(marker=dict(
                              line=dict(width=1,
                                        color='DarkSlateGrey'),

                                        ),
                  selector=dict(mode='markers'))

    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig

def create_time_series(dff, axis_type, title):

    fig = px.scatter(dff, x='Year', y='Value')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig

@app.callback(
    Output('stats_stud', 'children'),
    [Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-country-column', 'value'),
     Input('crossfilter-xaxis-type', 'value'),
     Input('crossfilter-yaxis-type', 'value'),
     ])

def stats_stud(xaxis_column_name, yaxis_column_name, country_column_name,
                 xaxis_type, yaxis_type
                 ):
    dff=df_stud[df_stud['Country Name']==country_column_name]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'], marginal_x='histogram',marginal_y='histogram',
            trendline='ols', template="plotly_white"
)
    fig.update_traces(marker=dict(
                              line=dict(width=1,
                                        color='DarkSlateGrey'),

                                        ),
                  selector=dict(mode='markers'))

    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')


    results = px.get_trendline_results(fig)
    model = results.px_fit_results.iloc[0].summary()
    a=model.as_html()

    return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(a)




if __name__ == '__main__':
    app.run_server(debug=True)
