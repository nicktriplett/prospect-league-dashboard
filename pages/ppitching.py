# Player Pitching Page

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

data_file3 = parent_folder / 'pl_player_pitching_stats.csv'
data_file3.is_file()
player_pitching_stats = pd.read_csv(data_file3)
player_pitching_stats

# Cleaning Data for Visualizations
player_pitching_stats['Name'].replace('\n', '', regex=True, inplace=True)

# Dropping TOTALS Observations for Bar Chart
player_pitching_stats.drop(522,inplace=True)

# Dropping Column(s) for Visualizations
player_pitching_stats.drop(columns=['Name_With_Blank'],inplace=True)

player_pitching_stats['App'] = pd.to_numeric(player_pitching_stats['App'], errors='coerce')
player_pitching_stats['IP'] = pd.to_numeric(player_pitching_stats['IP'], errors='coerce')
player_pitching_stats['H'] = pd.to_numeric(player_pitching_stats['H'], errors='coerce')
player_pitching_stats['H/9'] = pd.to_numeric(player_pitching_stats['H/9'], errors='coerce')
player_pitching_stats['R'] = pd.to_numeric(player_pitching_stats['R'], errors='coerce')
player_pitching_stats['ER'] = pd.to_numeric(player_pitching_stats['ER'], errors='coerce')
player_pitching_stats['BB'] = pd.to_numeric(player_pitching_stats['BB'], errors='coerce')
player_pitching_stats['BB/9'] = pd.to_numeric(player_pitching_stats['BB/9'], errors='coerce')
player_pitching_stats['K'] = pd.to_numeric(player_pitching_stats['K'], errors='coerce')
player_pitching_stats['K/BB'] = pd.to_numeric(player_pitching_stats['K/BB'], errors='coerce')
player_pitching_stats['WHIP'] = pd.to_numeric(player_pitching_stats['WHIP'], errors='coerce')
player_pitching_stats['FIP'] = pd.to_numeric(player_pitching_stats['FIP'], errors='coerce')

# Creating Dataframe for Visualization
player_pitching_stats1 = player_pitching_stats.drop(columns=['Name','#','Year','Pos'])
player_pitching_stats1['Name (Team)'] = player_pitching_stats['Name'] + ' (' + player_pitching_stats['Team'] + ')'
player_pitching_stats1.loc[:,('Name (Team)')]
player_pitching_stats1.set_index('Name (Team)',inplace=True)
player_pitching_stats2=player_pitching_stats1.drop(columns=['Team'])

player_pitching_stats3 = player_pitching_stats[player_pitching_stats['IP/G'] >= 0.76]


# Sorting Lists for Dashboard Components
batting_stat_list=[x for x in player_pitching_stats2.columns]
batting_player_list = [x for x in player_pitching_stats2.index]
unique_teams1 = player_pitching_stats1['Team'].unique()

# Registring the Page
dash.register_page(__name__)

# The Pitching Chart Page
layout=dbc.Container(
    children=[
    # Title and Dashboard Explanation
    html.H1('2023 Prospect League Pitching Statistics Visualizations',className='text-center text-dark mt-3 mb-2 fs-1'),
    html.H3('Scatter Plot', className='text-info text-center fs-2 mt-3 mb-0'),
    # The Graph
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Graph(
                    id='scatter_plot5',
                    className='mx-4 my-3',
                    config=dict(displayModeBar=False),
                ),
            ],
            width=10,
            className='offset-md-1'
        )
    ]),
    dbc.Row([
        dbc.Col(
            children=[
                dcc.RadioItems(
                    id='filter-radio1',
                    options=[
                        {'label':'All Prospect League Pitchers','value':'all'},
                        {'label':'Qualified Prospect League Pitchers','value':'greater_than_0.8'}
                    ],
                    value='all',
                    labelStyle={'display': 'inline-block','margin-right': '10px'},
                    inputStyle={'margin-right': '10px'},
                )
            ],
            className='offset-md-4'
        )
    ]),

    dbc.Row([
        dbc.Col(
            children=[
                html.P('Team(s) Selector',className='text-dark, text-center mb-2 fs-5'),
                dcc.Dropdown(
                    id='team-dropdown26',
                    options=[{'label': team, 'value': team} for team in unique_teams1],
                    multi=True,
                    value=unique_teams1
                ),
            ],
            width=10,
            className='mt-4 offset-md-1 mb-3'
        )
    ]),
    # User Commands
    dbc.Row([
        dbc.Col(
            children=[
                html.P('Please select a statistical measure for the X-axis to compare players with.',className='text-center text-dark fs-5 mt-1')
            ],
            width=6
        ),
        dbc.Col(
            children=[
                html.P("Please select a statistical measure for the Y-axis to compare players with.",className='text-center text-dark fs-5 mt-1')
            ],
            width=6
        )
    ]),
    # Dropdown Boxes
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='stat_dropdown5',
                    options=[
                        dict(label=x,value=x) for x in batting_stat_list
                    ],
                    optionHeight=25,
                    className='mt-0 mb-3',
                    value='IP',
                    clearable=False
                )
            ],
            width=4,
            className='offset-md-1'
        ),
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='stat_dropdown6',
                    options=[
                        dict(label=x,value=x) for x in batting_stat_list
                    ],
                    optionHeight=25,
                    className='mt-0 mb-3',
                    value='ERA',
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
    html.H3('Bar Chart', className='text-info text-center fs-2 mt-3 mb-0'),
    # The Graph
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Graph(
                    id='bar_chart7',
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
                html.P('Please select a statistical measure to compare players with.',className='text-center text-dark fs-5 mt-3')
            ],
            width=6
        ),
        dbc.Col(
            children=[
                html.P("Please select a player(s) you'd like to review above.",className='text-center text-dark fs-5 mt-3')
            ]
        )
    ]),
    # Dropdown Boxes
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='stat_choice9',
                    options=[
                        dict(label=x,value=x) for x in batting_stat_list
                    ],
                    className='mt-1 mb-3',
                    value='ERA',
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
                    id='player_dropdown0',
                    options=[
                        dict(label=x,value=x) for x in batting_player_list
                    ],
                    multi=True,
                    placeholder='Please select a team to review.',
                    optionHeight=25,
                    className='mt-1 mb-3',
                    value=['Sebastian Gonzalez (IVY)'],
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

    html.H3('Interactive Table (Qualified Pitchers)', className='text-info text-center fs-2 mt-3 mb-4'),

    dbc.Row([
        dbc.Col(
            children=[
                DataTable(
                    id='datatable-interactivity3',
                    columns=[{"name": i, "id": i,"deletable": False} for i in player_pitching_stats3.columns], 
                    data=player_pitching_stats3.to_dict('records'),
                    sort_action="native",
                    sort_mode="multi",
                    page_action="native",
                    page_current=0,
                    page_size=20,
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
                html.P('Please select a statistical measure(s) for the X-axis to compare teams with.',className='text-center text-dark fs-5 mt-3 mb-0')
            ],
        )
    ]),

    # Dropdown Box for Column Selection
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='column_dropdown3',
                    options=[
                        {'label': col, 'value': col} for col in player_pitching_stats3.columns
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


# Section for the Callback
@callback(
    Output('datatable-interactivity3', 'columns'),
    Output('datatable-interactivity3', 'data'),
    Output('scatter_plot5','figure'),
    Output('bar_chart7','figure'),
    Input('filter-radio1','value'),
    Input('team-dropdown26','value'),
    Input('stat_dropdown5','value'),
    Input('stat_dropdown6','value'),
    Input('stat_choice9','value'),
    Input('player_dropdown0','value'),
    Input('datatable-interactivity3', 'selected_columns'),
    Input('column_dropdown3', 'value'),
    Input('datatable-interactivity3', "derived_virtual_data"),
    Input('datatable-interactivity3', "derived_virtual_selected_rows"),
)

def charts(filter_value1,selected_teams1,stat_selection1,stat_selection2,stat_selection3,player_selection,selected_columns3,column_selection3,rows3,derived_virtual_selected_rows3):
    if filter_value1 == 'all':
        filtered_data = player_pitching_stats1
    else:
        filtered_data = player_pitching_stats1[player_pitching_stats1['IP/G'] >= 0.76]
    
    filtered_data = filtered_data[filtered_data['Team'].isin(selected_teams1)]

    if len(filtered_data) == 0 and filter_value1 == 'greater_than_0.8':
        filtered_data = player_pitching_stats1[player_pitching_stats1['IP/G'] >= 0.76]
    elif len(filtered_data) == 0:
        filtered_data = player_pitching_stats1
    
    if len(filtered_data) == 0:
        filtered_data = player_pitching_stats1
    
    if len(stat_selection3)==0:
        stat_selection3 = ['ERA']

    if len(player_selection)==0:
        player_selection = ['Sebastian Gonzalez (IVY)']

    if derived_virtual_selected_rows3 is None:
        derived_virtual_selected_rows3 = []

    if column_selection3 is None:
        column_selection3 = player_pitching_stats3.columns

    if 'Name (Team)' not in column_selection3:
        column_selection3.insert(0, 'Name (Team)')

    # Update the DataTable based on selected columns
    columns3 = [{"name": i, "id": i, "deletable": True, "selectable": True} for i in column_selection3]
    data3 = player_pitching_stats3.reset_index()[column_selection3].to_dict('records')

    # Making Batting Data Subset
    player_data_subset=player_pitching_stats1.loc[player_selection,stat_selection3].copy().reset_index()

    # Create a new DataFrame with 'Team' as a regular column
    team_column = player_pitching_stats1.loc[player_selection, 'Team'].reset_index()['Team']

    # Add the 'Team' column to the player_data_subset DataFrame
    player_data_subset['Team'] = team_column
    
    # Pitching Chart
    pitching_scatter_plot=px.scatter(
        filtered_data,
        x=stat_selection1,
        y=stat_selection2,
        title=' ',
        hover_name=filtered_data.index,
        color='Team',
        color_discrete_map={
            "CCY":'#044283',
            "CHI":'#BA0C2F',
            "JNT":'#3E342F',
            "LAF":'#FFC82F',
            "DAN":'#D22730',
            "NOR":'#2C5234',
            "TER":'#0057B7',
            "SPR":'#072B31',
            "BRL":'#FFB81C',
            "CLN":'#00843D',
            "IVY":'#FF8200',
            "QUI":'#E4002B',
            "ALT":'#279989',
            "CGR":'#78BE21',
            "JAX":'#84329B',
            "OFL":'#010101',
            "THR":'#FF8F1C',
        }
    )

    pitching_scatter_plot.update_xaxes(
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

    pitching_scatter_plot.update_yaxes(
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

    pitching_scatter_plot.update_layout(
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

    pitching_scatter_plot.update_traces(
        marker_size=11,
        marker_line_color='black',
        marker_line_width=1,
        textfont_size=14
)
    
    # Pitching Bar Chart
    pitching_figure1=px.bar(
        player_data_subset,
        x=stat_selection3,
        y='Name (Team)',
        orientation='h',
        text_auto=True,
        title=' ',
        color='Team',
        color_discrete_map={
            "CCY":'#044283',
            "CHI":'#BA0C2F',
            "JNT":'#3E342F',
            "LAF":'#FFC82F',
            "DAN":'#D22730',
            "NOR":'#2C5234',
            "TER":'#0057B7',
            "SPR":'#072B31',
            "BRL":'#FFB81C',
            "CLN":'#00843D',
            "IVY":'#FF8200',
            "QUI":'#E4002B',
            "ALT":'#279989',
            "CGR":'#78BE21',
            "JAX":'#84329B',
            "OFL":'#010101',
            "THR":'#FF8F1C',
        },
    )

    pitching_figure1.update_xaxes(
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

    pitching_figure1.update_yaxes(
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

    pitching_figure1.update_layout(
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

    pitching_figure1.update_traces(
        marker_line_color='black',
        marker_line_width=0.5,
        textfont_size=14
)

    return columns3, data3, pitching_scatter_plot, pitching_figure1
