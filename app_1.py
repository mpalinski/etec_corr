import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_dangerously_set_inner_html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df=pd.read_csv('./corr_countries.csv')
df_schools=pd.read_csv('./corr_schools.csv')
df_stud=pd.read_csv('./corr_students.csv')


available_indicators = df['Indicator Name'].unique()
available_countries = df['Country Name'].unique()

# external JavaScript files
external_scripts = [
    'https://cdn.jsdelivr.net/gh/mpalinski/etec_corr@main/assets/resizing.js'
]


app1 = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
external_scripts=external_scripts,
url_base_pathname='/dash/')

# server = app.server

app1.title = 'TIMSS 2019 | Correlations'

app1.layout = html.Div([
    # html.Title('TIMSS 2019 | Correlations'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
html.H1('TIMSS 2019 | Correlations', style={'marginTop': '31rem'}),
html.H3('Analysis level'),
    dcc.Link(html.Button('Country level'), href='/country-lvl'),

    dcc.Link(html.Button('School level'), href='/school-lvl'),

    dcc.Link(html.Button('Student level'), href='/student-lvl'),

],  style={
  # 'className': 'cover',
  'textAlign': 'center', 'position':'fixed',
  'width':'100%',
  'height':'100%',
  'top':'0px',
  'left':'0px',
  # 'zIndex':'1000',
  'backgroundImage':'url(/assets/background7.gif)',
  'backgroundRepeat': 'no-repeat',
  'backgroundPosition': 'center',
  'backgroundSize': 'auto',
  'opacity': '0.8'
}
),


country_layout = html.Div([
    html.Div([
    html.H1('TIMSS 2019 | Correlations | Countries'),

     html.Div([

html.Div(
    dbc.Button('Analysis level', className="tutorial", href='/dash'),
    style={'width': '10%', 'display': 'inline-block'}
),
html.Div(
    [
        dbc.Button("Tutorial", id="open", className="tutorial"),
        dbc.Modal(
            [
                dbc.ModalHeader("Tutorial"),
                dbc.ModalBody(
                html.Iframe(src="https://www.dailymotion.com/embed/video/k7DKKxILyWYWplwXaUQ?autoplay=1&queue-enable=false", width="100%", height="500px")
    ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto tutorial")
                ),
            ],
            id="modal",
            size="lg",
        ),
    ]
,style={'width': '10%', 'display': 'inline-block'}),
]),
        html.Div(
        [html.H4('x axis'),
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Home Resources for Learning'
            ),
            # dcc.RadioItems(
            #     id='crossfilter-xaxis-type',
            #     options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            #     value='Linear',
            #     labelStyle={'display': 'inline-block'}
            # )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([

        html.H4('y axis'),
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Math'
            ),
            # dcc.RadioItems(
            #     id='crossfilter-yaxis-type',
            #     options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            #     value='Linear',
            #     labelStyle={'display': 'inline-block'}
            # )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '60%', 'display': 'block', 'padding': '0 0 0', "marginLeft": "auto",
            "marginRight": "auto",}),
            html.Br(),

    html.Hr(),

    html.Div([html.P(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(''))],id='stats', style={'margin-left': 'auto','margin-right':'auto'})

],  style={
            'textAlign': 'center'})
@app1.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app1.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    [Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     # Input('crossfilter-xaxis-type', 'value'),
     # Input('crossfilter-yaxis-type', 'value'),
     ])

def update_graph(xaxis_column_name, yaxis_column_name,
                 # xaxis_type, yaxis_type,

                 ):
    dff=df

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'], color=dff[dff['Indicator Name'] == xaxis_column_name]['continent'], marginal_x='histogram',marginal_y='histogram',
            trendline='ols', template="plotly_white"
)
    fig.update_traces(marker=dict(
                              line=dict(width=1,
                                        color='DarkSlateGrey'),
                                        ),
                  selector=dict(mode='markers'))

    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    # fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    # fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.add_annotation(x=dff[(dff['Indicator Name'] == xaxis_column_name) & (dff['Country Name']=='Saudi Arabia')]['Value'].values[0], y=dff[(dff['Indicator Name'] == yaxis_column_name) & (dff['Country Name']=='Saudi Arabia')]['Value'].values[0],
            text="Saudi Arabia",
            showarrow=False,
            )

    return fig

@app1.callback(
    Output('stats', 'children'),
    [Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     # Input('crossfilter-xaxis-type', 'value'),
     # Input('crossfilter-yaxis-type', 'value'),

     ])

def stats(xaxis_column_name, yaxis_column_name,
                 # xaxis_type, yaxis_type,
                 ):
    dff=df
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

    # fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    # fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.add_annotation(x=dff[(dff['Indicator Name'] == xaxis_column_name) & (dff['Country Name']=='Saudi Arabia')]['Value'].values[0], y=dff[(dff['Indicator Name'] == yaxis_column_name) & (dff['Country Name']=='Saudi Arabia')]['Value'].values[0],
            text="Saudi Arabia",
            showarrow=False,
            )
    results = px.get_trendline_results(fig)
    model = results.px_fit_results.iloc[0].summary()

    a=model.as_html()
    return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(a)


school_layout = html.Div([
    html.Div([
    html.H1('TIMSS 2019 | Correlations | Schools'),
     html.Div([

html.Div(
    dbc.Button('Analysis level', className="tutorial", href='/dash'),
    style={'width': '10%', 'display': 'inline-block'}
),
html.Div(
    [
        dbc.Button("Tutorial", id="open", className="tutorial"),
        dbc.Modal(
            [
                dbc.ModalHeader("Tutorial"),
                dbc.ModalBody(
                html.Iframe(src="https://www.dailymotion.com/embed/video/k7DKKxILyWYWplwXaUQ?autoplay=1&queue-enable=false", width="100%", height="500px")
    ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto tutorial")
                ),
            ],
            id="modal",
            size="lg",
        ),
    ]
,style={'width': '10%', 'display': 'inline-block'}),
]),
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
            labelStyle={'display': 'inline-block', 'visibility':'hidden'}
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
    }),
    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter-schools',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '60%', 'display': 'block', 'padding': '0 0 0', "margin-left": "auto",
            "margin-right": "auto",}),
            html.Br(),
    html.Hr(),

    html.Div([html.P(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(''))],id='stats_schools', style={'margin-left': 'auto', 'margin-right':'auto'})


],  style={
            'textAlign': 'center'})

@app1.callback(
    Output('crossfilter-indicator-scatter-schools', 'figure'),
    [Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-country-column', 'value'),
     Input('crossfilter-xaxis-type', 'value'),
     Input('crossfilter-yaxis-type', 'value'),
     ])


def update_graph(xaxis_column_name, yaxis_column_name, country_column_name,
                 xaxis_type, yaxis_type):

    dff=df_schools[df_schools['Country Name']==country_column_name]
    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['idschool'], marginal_x='histogram',marginal_y='histogram',
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

@app1.callback(
    Output('stats_schools', 'children'),
    [Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-country-column', 'value'),
     Input('crossfilter-xaxis-type', 'value'),
     Input('crossfilter-yaxis-type', 'value'),
     ])

def stats_schools(xaxis_column_name, yaxis_column_name, country_column_name,
                 xaxis_type, yaxis_type
                 ):
    dff=df_schools[df_schools['Country Name']==country_column_name]

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

    fig.update_traces(customdata=dff[df_schools['Indicator Name'] == yaxis_column_name]['Country Name'])

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')


    results = px.get_trendline_results(fig)
    model = results.px_fit_results.iloc[0].summary()
    a=model.as_html()

    return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(a)


student_layout = html.Div([
    html.Div([
    html.H1('TIMSS 2019 | Correlations | Students'),

     html.Div([

html.Div(
    dbc.Button('Analysis level', className="tutorial", href='/dash'),
    style={'width': '10%', 'display': 'inline-block'}
),
html.Div(
    [
        dbc.Button("Tutorial", id="open", className="tutorial"),
        dbc.Modal(
            [
                dbc.ModalHeader("Tutorial"),
                dbc.ModalBody(
                html.Iframe(src="https://www.dailymotion.com/embed/video/k7DKKxILyWYWplwXaUQ?autoplay=1&queue-enable=false", width="100%", height="500px")
    ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto tutorial")
                ),
            ],
            id="modal",
            size="lg",
        ),
    ]
,style={'width': '10%', 'display': 'inline-block'}),
]),
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
            labelStyle={'display': 'inline-block', 'visibility':'hidden'}
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

    html.Hr(),

    html.Div([html.P(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(''))],id='stats_stud', style={'margin-left': 'auto', 'margin-right': 'auto'})


], style={
            'textAlign': 'center'})

@app1.callback(
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

@app1.callback(
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



# Update the index
@app1.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/country-lvl':
        return country_layout
    elif pathname == '/school-lvl':
        return school_layout
    elif pathname == '/student-lvl':
        return student_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app1.run_server(debug=True)
