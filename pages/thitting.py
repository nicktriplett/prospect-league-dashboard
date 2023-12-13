# Team Hitting Page

import os
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pathlib
from pathlib import Path
from dash_table import DataTable

# Loading Data for Visualizations
main_file_path = pathlib.Path(__file__)
parent_folder = main_file_path.parent

data_file2 = parent_folder / 'pl_team_hitting_stats.csv'
data_file2.is_file()
team_hitting_stats = pd.read_csv(data_file2)
team_hitting_stats

# Dropping TOTALS Observations for Bar Chart
team_hitting_stats.drop(17,inplace=True)

# Changing columns from object to numeric
team_hitting_stats['TTO%'] = team_hitting_stats['TTO%'].str.rstrip('%').astype(float)
team_hitting_stats['BB%'] = team_hitting_stats['BB%'].str.rstrip('%').astype(float)
team_hitting_stats['K%'] = team_hitting_stats['K%'].str.rstrip('%').astype(float)
team_hitting_stats['SB%'] = team_hitting_stats['SB%'].str.rstrip('%').astype(float)
columns_to_convert = ['PA','AB','R','H','1B','2B','RBI','BB','K','TTO','SB','HBP','TB','XBH','GO','FO','RC']
for column in columns_to_convert:
    team_hitting_stats[column] = pd.to_numeric(team_hitting_stats[column], errors='coerce')

# Creating and Setting an Index
team_hitting_stats1=team_hitting_stats.copy()
team_hitting_stats.loc[:,('Name')]
team_hitting_stats.set_index('Name',inplace=True)

# Sorting Lists for Dashboard Components
stat_list=[x for x in team_hitting_stats.columns]
team_list = [x for x in team_hitting_stats.index]

# Rank Function

# Registering the Team Batting Page
dash.register_page(__name__)

# The Batting Chart Page
layout=dbc.Container(
    children=[
    # Title and Dashboard Explanation
    html.H1('2023 Prospect League Team Hitting Statistics Visualizations',className='text-center text-dark mt-3 mb-2 fs-1'),
    html.H3('Bar Chart', className='text-info text-center fs-2 mt-3 mb-0'),
    # The Graph
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Graph(
                    id='bar_chart',
                    className='m-4',
                    config=dict(displayModeBar=False),
                ),
            ],
            width=10,
            className='offset-md-1'
        )
    ]),
    # User Commands
    dbc.Row([
        dbc.Col(
            children=[
                html.P('Please select a statistical measure to compare teams with.',className='text-center text-dark fs-5 mt-3')
            ],
            width=6
        ),
        dbc.Col(
            children=[
                html.P("Please select a team(s) you'd like to review above.",className='text-center text-dark fs-5 mt-3')
            ]
        )
    ]),
    # Dropdown Boxes
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='stat_choice',
                    options=[
                        dict(label=x,value=x) for x in stat_list
                    ],
                    className='mt-1 mb-3',
                    value='OPS',
                    multi=False,
                    optionHeight=25,
                    clearable=False
                )
            ],
            width=4,
            className='offset-md-1'
        ),
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='team_dropdown',
                    options=[
                        dict(label=x,value=x) for x in team_list
                    ],
                    multi=True,
                    placeholder='Please select a team to review.',
                    optionHeight=25,
                    className='mt-1 mb-3',
                    value=['Chillicothe Paints'],
                    clearable=False
                )
            ],
            width=4,
            className='offset-md-2'
        )
    ]),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    # Title and Dashboard Explanation
    html.H3('Scatter Plot', className='text-info text-center fs-2 mt-3 mb-0'),
    # The Graph
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Graph(
                    id='scatter_plot1',
                    className='m-4',
                    config=dict(displayModeBar=False),
                ),
            ],
            width=10,
            className='offset-md-1'
        )
    ]),
    # User Commands
    dbc.Row([
        dbc.Col(
            children=[
                html.P('Please select a statistical measure for the X-axis to compare teams with.',className='text-center text-dark fs-5 mt-3')
            ],
            width=6
        ),
        dbc.Col(
            children=[
                html.P("Please select a statistical measure for the Y-axis to compare teams with.",className='text-center text-dark fs-5 mt-3')
            ],
            width=6
        )
    ]),
    # Dropdown Boxes
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='stat_dropdown3',
                    options=[
                        dict(label=x,value=x) for x in stat_list
                    ],
                    optionHeight=25,
                    className='mt-1 mb-3',
                    value='wRC+',
                    clearable=False
                )
            ],
            width=4,
            className='offset-md-1'
        ),
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='stat_dropdown4',
                    options=[
                        dict(label=x,value=x) for x in stat_list
                    ],
                    optionHeight=25,
                    className='mt-1 mb-3',
                    value='Win %',
                    clearable=False
                )
            ],
            width=4,
            className='offset-md-2'
        )
    ]),

    # Interactive Table
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.H3('Interactive Table', className='text-info text-center fs-2 mt-3 mb-4'),

    dbc.Row([
        dbc.Col(
            children=[
                DataTable(
                    id='datatable-interactivity',
                    columns=[{"name": i, "id": i,"deletable": False} for i in team_hitting_stats1.columns], 
                    data=team_hitting_stats1.to_dict('records'),
                    sort_action="native",
                    sort_mode="multi",
                    page_action="native",
                    page_current=0,
                    page_size=len(team_hitting_stats1),
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'center'},
                ),
            ],
            width=10,
            className='offset-md-1'
        )
    ]),
    
    dbc.Row([
        dbc.Col(
            children=[
                html.P("Please select what statistics or measures you'd like to be included in this table.",className='text-center text-dark fs-5 mt-3')
            ],
        )
    ]),

    # Dropdown Box for Column Selection
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='column_dropdown',
                    options=[
                        {'label': col, 'value': col} for col in team_hitting_stats1.columns
                    ],
                    multi=True,
                    placeholder='Please select a statistic(s) to review.',
                    className='mt-1 mb-3',
                ),
            ],
            width=4,
            className='offset-md-4'
        ),
    ]),

    # Data Sources and Information
    html.Div(
        children=[
            'Data Source: ',
            html.A(
                'Prospect League',
                href='https://prospectleague.com/landing/index',className='text-info fs-5'
            ),
        ],
        className='text-dark text-center fs-5 mt-5'
    ),
    html.Div(
        children=[
            'Baseball Data Abbreviations and Definitions: ',
            html.A(
                'MLB Glossary',
                href='https://www.mlb.com/glossary',className='text-info fs-5'
            )
        ],
        className='text-dark text-center fs-5 mb-2'
    )
    ],
    fluid=True
)

# Callbacks
@callback(
    Output('datatable-interactivity', 'columns'),
    Output('datatable-interactivity', 'data'),
    Output('bar_chart', 'figure'),
    Output('scatter_plot1', 'figure'),
    Input('stat_choice', 'value'),
    Input('team_dropdown', 'value'),
    Input('stat_dropdown3', 'value'),
    Input('stat_dropdown4', 'value'),
    Input('datatable-interactivity', 'selected_columns'),
    Input('column_dropdown', 'value'),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"),
)
def update_data_and_table(
        stat_selection, list_of_teams, stat_selection2, stat_selection3,
        selected_columns, column_selection, rows, derived_virtual_selected_rows
):
    if len(stat_selection) == 0:
        stat_selection = ['OPS']

    if len(list_of_teams) == 0:
        list_of_teams = ['Chillicothe Paints']

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    if column_selection is None:
        column_selection = team_hitting_stats1.columns

    if 'Name' not in column_selection:
        column_selection.insert(0, 'Name')

    # Update the DataTable based on selected columns
    columns = [{"name": i, "id": i, "deletable": True, "selectable": True} for i in column_selection]
    data = team_hitting_stats1[column_selection].to_dict('records')

    # Making Batting Data Subset
    batting_data_subset = team_hitting_stats.loc[list_of_teams, stat_selection].copy().reset_index()

    # Batting Chart
    batting_figure=px.bar(
        batting_data_subset,
        x=stat_selection,
        y='Name',
        orientation='h',
        text_auto=True,
        title=' ',
        color='Name',
        color_discrete_map={
            "Champion City Kings":'#044283',
            "Chillicothe Paints":'#BA0C2F',
            "Johnstown Mill Rats":'#3E342F',
            "Lafayette Aviators":'#FFC82F',
            "Danville Dans":'#D22730',
            "Normal CornBelters":'#2C5234',
            "REX Baseball":'#0057B7',
            "Springfield Lucky Horseshoes":'#072B31',
            "Burlington Bees":'#FFB81C',
            "Clinton LumberKings":'#00843D',
            "Illinois Valley Pistol Shrimp":'#FF8200',
            "Quincy Gems":'#E4002B',
            "Alton River Dragons":'#279989',
            "Cape Catfish":'#78BE21',
            "Jackson Rockabillys":'#84329B',
            "O'Fallon Hoots":'#010101',
            "Thrillville Thrillbillies":'#FF8F1C',
        }
    )

    batting_figure.update_xaxes(
        title_font={
        'size': 18,
        'color': 'black'
        },
        tickfont=dict(
            size=14,
            color='black'
        ),
        showgrid=True,
        gridwidth=1,
        gridcolor='black',
        showline=True,
        linewidth=1,
        linecolor='black'
    )

    batting_figure.update_yaxes(
        title_text='Team(s)',
        title_font={
        'size': 18,
        'color': 'black'
        },
        tickfont=dict(
            size=14,
            color='black'
        ),
        showline=True,
        linewidth=1,
        linecolor='black',
        categoryorder='total ascending'
    )

    batting_figure.update_layout(
        title_font={
        'size': 24,
        'color': 'black'
        },
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0,r=0,t=0,b=0),
        showlegend=False,
    )

    batting_figure.update_traces(
        marker_line_color='black',
        marker_line_width=0.5,
        textfont_size=14,
)
    
    # Pitching Chart
    hitting_scatter_plot1=px.scatter(
        team_hitting_stats,
        x=stat_selection2,
        y=stat_selection3,
        title=' ',
        hover_name=team_hitting_stats.index,
        color=team_hitting_stats.index,
        color_discrete_map={
            "Champion City Kings":'#044283',
            "Chillicothe Paints":'#BA0C2F',
            "Johnstown Mill Rats":'#3E342F',
            "Lafayette Aviators":'#FFC82F',
            "Danville Dans":'#D22730',
            "Normal CornBelters":'#2C5234',
            "REX Baseball":'#0057B7',
            "Springfield Lucky Horseshoes":'#072B31',
            "Burlington Bees":'#FFB81C',
            "Clinton LumberKings":'#00843D',
            "Illinois Valley Pistol Shrimp":'#FF8200',
            "Quincy Gems":'#E4002B',
            "Alton River Dragons":'#279989',
            "Cape Catfish":'#78BE21',
            "Jackson Rockabillys":'#84329B',
            "O'Fallon Hoots":'#010101',
            "Thrillville Thrillbillies":'#FF8F1C',
        }
    )

    hitting_scatter_plot1.update_xaxes(
        title_font={
        'size': 18,
        'color': 'black'
        },
        tickfont=dict(
            size=14,
            color='black'
        ),
        showgrid=True,
        gridwidth=0.5,
        gridcolor='black',
        showline=True,
        linewidth=1,
        linecolor='black'
    )

    hitting_scatter_plot1.update_yaxes(
        title_font={
        'size': 18,
        'color': 'black'
        },
        tickfont=dict(
            size=14,
            color='black'
        ),
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridwidth=1,
        gridcolor='black',
    )

    hitting_scatter_plot1.update_layout(
        title_font={
        'size': 24,
        'color': 'black'
        },
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0,r=0,t=0,b=0),
        showlegend=False,
    )

    hitting_scatter_plot1.update_traces(
        marker_size=11,
        marker_line_color='black',
        marker_line_width=1,
        textfont_size=14
)
    
    return columns, data, batting_figure, hitting_scatter_plot1
