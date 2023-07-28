# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 20:41:16 2023

@author: berar

Graph the AL West Race by day
Data Source
https://www.baseball-reference.com/teams
Schedule/results

"""

import pandas as pd
import numpy as np
import dash
import requests
import io
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from plotly.offline import plot
from dash.dependencies import Input, Output, State
import plotly.express as px

# a = pd.read_html('https://www.baseball-reference.com/teams/CLE/2023-schedule-scores.shtml')
# a = pd.concat(a)
# a= a[a['Unnamed: 2']!='preview']
# b = a[a['Gm#']!='Gm#']

def get_standings():
    filename = r'C:\Users\berar\Documents\Projects\visualization_demo\baseball\data\mlb_standings.csv'
    df = pd.read_csv(filename)
    df['Division'] = df['League'] + ' ' + df['Division']
    return df

def get_data_results():
    filename = r'C:\Users\berar\Documents\Projects\visualization_demo\baseball\data\schedule_results.csv'
    df = pd.read_csv(filename)
    # Need to accumulate wins and losses
    df['W'] = np.where(df['W/L']=='W',1,0)
    df['L'] = np.where(df['W']==0,1,0)
    df['cum_W'] = df.groupby(['Tm'])['W'].cumsum()
    df['cum_L'] = df.groupby(['Tm'])['L'].cumsum()
    df['WL_perc'] = (df['cum_W']/(df['cum_W']+ df['cum_L']))*100
    df['Dd'] = df['Date'].str.split(',')
    df['DDD'] = df['Dd'].str[1]
    df['DDD'] = df['DDD'].str.strip()
    df['DDD'] = df['DDD'].str.split('(')
    # df['DDD'] = df['DDD'].str.replace('(1)', '')
    # df['DDD'] = df['DDD'].str.replace('(2)', '')
    df['DDD'] = df['DDD'].str[0]
    df['DDD'] = df['DDD'].str.strip() + ' 2023'
    df['Date'] = pd.to_datetime(df['DDD'], format='%b %d %Y')
    df = df.drop_duplicates(['Tm', 'Date'], keep='last')
    df['cum_R'] = df.groupby(['Tm'])['R'].cumsum()
    df['cum_RA'] = df.groupby(['Tm'])['RA'].cumsum()
    df['run_diff'] = df['cum_R'] - df['cum_RA']
    return df

def day_of_season():
    df = get_data_results()
    dmin = df.Date.min()
    dmax = df.Date.max()
    daterange = pd.DataFrame(pd.date_range(dmin, dmax))
    daterange['idx'] = daterange.index
    return daterange

def plot_wins():
    df = get_data_results()
    df = df[['WL_perc', 'cum_W', 'run_diff', 'Tm', 'Date', 'Division']]
    df = pd.pivot_table(df, values=['WL_perc', 'cum_W', 'run_diff'], index=['Tm', 'Date', 'Division'],
                        aggfunc={'WL_perc': np.sum, 
                                 'cum_W': np.sum, 
                                 'run_diff': np.sum}).reset_index()
    df = df.ffill()
    return df

def get_attendance():
    filename = r'C:\Users\berar\Documents\Projects\visualization_demo\baseball\data\mlb_att.csv'
    df = pd.read_csv(filename)
    return df

def get_population():
    filename = r'C:\Users\berar\Documents\Projects\visualization_demo\baseball\data\tm_pop.csv'
    df = pd.read_csv(filename)
    df = df[df['Radius']==25]
    return df

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

df = get_data_results()
dates = day_of_season()
date_max = dates['idx'].max()
wins = plot_wins()
pop = get_population()
standings = get_standings()
att = get_attendance()
att = att.drop('Tm', axis=1)
att = pd.merge(standings, att, how='inner', left_on=['Tm'], right_on=['Tm Abbv'])
att = pd.merge(att, pop, how='inner', on=['Tm Abbv'])

fig = px.line(
    wins,
    y="WL_perc",
    x="Date",
    title='Win-Loss Percentage',
    color='Tm',
    color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
    hover_name='Tm',
    )

fig2 = px.line(
    wins,
    y="cum_W",
    x="Date",
    title='Cumulative Wins',
    color='Tm',
    color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
    hover_name='Tm',
    )

fig3 = px.line(
    wins,
    y="run_diff",
    x="Date",
    title='Run Differential',
    color = 'Tm',
    color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
    hover_name='Tm',
    )

fig4 = px.scatter(
    att,
    y='perc_full',
    x="Est. Payroll",
    size='perc_full',
    text = att['Tm'],
    opacity=0.2,
    # color = 'Tm',     
    # color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
    hover_data=['Tm'],
    )

fig5 = px.scatter(
    att,
    y="perc_full",
    x="GB",
    size='Attendance',
    text = att['Tm'],
    opacity=0.2,
    # color = 'Tm',     
    # color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
    hover_data=['Tm'],
    )

fig6 = px.scatter(
    att,
    y="perc_full",
    x="W",
    size='Attendance',
    text = att['Tm'],
    opacity=0.2,
    # color = 'Tm',     
    # color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
    hover_data=['Tm'],
    )

fig7 = px.scatter(
    att,
    y="perc_full",
    x="CAPACITY",
    size='Attendance',
    text = att['Tm'],
    opacity=0.2,
    # color = 'Tm',     
    # color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
    hover_data=['Tm'],
    )

fig8 = px.scatter(
    att,
    y="perc_full",
    x=" Population ",
    size='Attendance',
    text = att['Tm'],
    opacity=0.2,
    # color = 'Tm',     
    # color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
    hover_data=['Tm'],
    )

fig9 = px.scatter(
    att,
    y="W",
    x="Est. Payroll",
    size='Attendance',
    text = att['Tm'],
    opacity=0.2,
    # color = 'red',
    # color = 'Tm',     
    # color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
    hover_data=['Tm'],
    )

app  = dash.Dash()

app.layout = html.Div([
    html.H1(
        children='Baseline', style={'textAlign':'center'}
        ),
    
    dcc.Slider(
        id='day-slider',
        value = date_max,
        min = 0,
        max = date_max,
        step=1,
        # marks={idx: str(0) for idx in range(0, 115)},
        # value=df.Date.min()
        ),
    
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='status-dropdown',
                    options=[
                        {'label': s, 'value': s} for s in df.Division.unique()
                        ],
                    value = 'AL West',
                    ),
                html.Div(children=[
                    dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in standings.columns],
                    data=standings.to_dict('records'),
                    export_format="csv",
                    page_size=40,
                    style_data={
                        'width': '100px',
                        'maxWidth': '100px',
                        'minWidth': '100px',
                        'font-size': '10px',
                        'font': 'Calibri',
                        'height': '10%',
                        'width': '90%'
                    },
                    style_table={'height': '400px', 'width': '800px', 'overflowY': 'auto'},
                    style_cell={'minWidth': 95, 'width': '90%', 'maxWidth': 95, "height": "10%"},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(220, 220, 220)',
                        }
                        ],
                    )
                    ], style={'padding': 10, 'flex': 2, 'flex-width': '90%'}
                    ),
            ], style={'display': 'flex', 'flex-direction': 'column'}
            ),
            html.Div(
                [dcc.Graph(id='Win-Loss Percentage', figure=fig,
                           config={'displayModeBar': False})
                 ],
                className='chart'),
            html.Div(
                [dcc.Graph(id='Cumulative Wins', figure=fig2,
                           config={'displayModeBar': False})
                 ],
                className='chart2'),
            html.Div(
                [dcc.Graph(id='Run Differential', figure=fig3,
                           config={'displayModeBar': False})
                 ],
                className='chart3'),
            ], style={'display': 'flex', 'flex-direction': 'row'}
        ),
        
        ], style={'display': 'flex', 'flex-direction': 'row'}
        ),
    html.Div([
        html.Div(
            [dcc.Graph(id='Attendance Per Payroll', figure=fig4,
                       config={'displayModeBar': False})
             ],
            className='chart4'),
        html.Div(
            [dcc.Graph(id='Attendance Per GamesBack', figure=fig5,
                       config={'displayModeBar': False})
             ],
            className='chart5'),
        html.Div(
            [dcc.Graph(id='Attendance Per Win', figure=fig6,
                       config={'displayModeBar': False})
             ],
            className='chart6'),
        ], style={'display': 'flex', 'flex-direction': 'row'}
        ),
    html.Div([    
        html.Div(
            [dcc.Graph(id='Perc Full by Capacity', figure=fig7,
                       config={'displayModeBar': False})
             ],
            className='chart7'),
        html.Div(
            [dcc.Graph(id='Perc Full by Population', figure=fig8,
                       config={'displayModeBar': False})
             ],
            className='chart8'),
        html.Div(
            [dcc.Graph(id='W per Payroll', figure=fig9,
                       config={'displayModeBar': False})
             ],
            className='chart9'),
        ], style={'display': 'flex', 'flex-direction': 'row'}
        ),
    ]
    )


@app.callback(
    Output(component_id='Win-Loss Percentage', component_property='figure'),
    Input(component_id='status-dropdown', component_property='value'),
    Input(component_id='day-slider', component_property='value')
    )
def update_chart(input_value, date_input):
    dates = day_of_season()
    print(date_input)
    dates = dates[dates['idx']<date_input]
    df = plot_wins()
    df = pd.merge(dates, df, how='inner', left_on=[0], right_on=['Date'])
    df = df[df['Division']==input_value]
    fig = px.line(
        df,
        y="WL_perc",
        x="Date",
        title='Win-Loss Percentage',
        color='Tm',
        color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
        hover_name='Tm',
        )
    fig.update_yaxes(title='Percent')
    fig.update_xaxes(title=None)
    fig.update_layout(
    plot_bgcolor='white'
    )
    return fig

@app.callback(
    Output(component_id='Cumulative Wins', component_property='figure'),
    Input(component_id='status-dropdown', component_property='value'),
    Input(component_id='day-slider', component_property='value')
    )
def update_chart2(input_value, date_input):
    dates = day_of_season()
    print(date_input)
    dates = dates[dates['idx']<date_input]
    df = plot_wins()
    df = pd.merge(dates, df, how='inner', left_on=[0], right_on=['Date'])
    df = df[df['Division']==input_value]
    fig = px.line(
        df,
        y="cum_W",
        x="Date",
        title='Cumulative Wins',
        color='Tm',
        color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
        hover_name='Tm',
        )
    fig.update_yaxes(title='Wins')
    fig.update_xaxes(title=None)
    fig.update_layout(
    plot_bgcolor='white'
    )
    return fig

@app.callback(
    Output(component_id='Run Differential', component_property='figure'),
    Input(component_id='status-dropdown', component_property='value'),
    Input(component_id='day-slider', component_property='value')
    )
def update_chart3(input_value, date_input):
    dates = day_of_season()
    print(date_input)
    dates = dates[dates['idx']<date_input]
    df = plot_wins()
    df = pd.merge(dates, df, how='inner', left_on=[0], right_on=['Date'])
    df = df[df['Division']==input_value]
    # animations = {
    #     px.line(
    #         df, x='Date', y='run_diff',
    #         animation_frame='Date',
    #         animation_group='Tm', color='Tm',
    #         hover_name='Tm'
    #         )
    #     }
    # return animations
    fig = px.line(
        df,
        y="run_diff",
        x="Date",
        title='Run Differential',
        color='Tm',
        color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
        hover_name='Tm',
        )
    fig.update_yaxes(title='Runs', visible=True, showticklabels=True)
    fig.update_xaxes(title=None)
    fig.update_layout(
    plot_bgcolor='white'
    )
    return fig

# @app.callback(
#     Output(component_id='Run Differential', component_property='figure'),
#     Input(component_id='status-dropdown', component_property='value'),
#     Input(component_id='day-slider', component_property='value')
#     )
# def update_chart4(input_value, date_input):
#     dates = day_of_season()
#     print(date_input)
#     dates = dates[dates['idx']<date_input]
#     df = plot_wins()
#     df = pd.merge(dates, df, how='inner', left_on=[0], right_on=['Date'])
#     df = df[df['Division']==input_value]
#     # animations = {
#     #     px.line(
#     #         df, x='Date', y='run_diff',
#     #         animation_frame='Date',
#     #         animation_group='Tm', color='Tm',
#     #         hover_name='Tm'
#     #         )
#     #     }
#     # return animations
#     fig = px.line(
#         df,
#         y="run_diff",
#         x="Date",
#         title='Run Differential',
#         color='Tm',
#         color_discrete_sequence=["orange", "red", "green", "teal", 'blue'],
#         hover_name='Tm',
#         )
#     fig.update_yaxes(title='Runs', visible=True, showticklabels=True)
#     fig.update_xaxes(title=None)
#     fig.update_layout(
#     plot_bgcolor='white'
#     )
#     return fig

@app.callback(
    Output("table", "data"), 
    Input("status-dropdown", component_property='value')
)
def display_table(input_value):
    dff = standings[standings['Division'].str.contains(input_value)]
    return dff.to_dict("records")


if __name__ == '__main__':
    app.run_server(debug=True)
                                 

