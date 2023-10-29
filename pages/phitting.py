# Player Hitting Page

import os
import pathlib
from pathlib import Path
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc

# Loading Data for Visualizations
main_file_path = pathlib.Path(__file__)
parent_folder = main_file_path.parent

data_file1 = parent_folder / 'pl_player_hitting_stats.csv'
data_file1.is_file()
player_hitting_stats = pd.read_csv(data_file1)
player_hitting_stats

# Cleaning Data for Visualizations
player_hitting_stats['Name'].replace('\n', '', regex=True, inplace=True)

# Dropping Column(s) for Visualizations
player_hitting_stats.drop(columns=['Name_With_Blanks'],inplace=True)

player_hitting_stats.drop(485,inplace=True)

# Convert columns to float/numeric
player_hitting_stats['K%'] = player_hitting_stats['K%'].str.rstrip('%').astype(float)
player_hitting_stats['BB%'] = player_hitting_stats['BB%'].str.rstrip('%').astype(float)
player_hitting_stats['SB%'] = player_hitting_stats['SB%'].str.rstrip('%').astype(float)
player_hitting_stats['TTO%'] = player_hitting_stats['TTO%'].str.rstrip('%').astype(float)
player_hitting_stats['G'] = pd.to_numeric(player_hitting_stats['G'], errors='coerce')
player_hitting_stats['PA'] = pd.to_numeric(player_hitting_stats['PA'], errors='coerce')
player_hitting_stats['PA/G'] = pd.to_numeric(player_hitting_stats['PA/G'], errors='coerce')
player_hitting_stats['BB%'] = pd.to_numeric(player_hitting_stats['BB%'], errors='coerce')
player_hitting_stats['K%'] = pd.to_numeric(player_hitting_stats['K%'], errors='coerce')
player_hitting_stats['SB%'] = pd.to_numeric(player_hitting_stats['SB%'], errors='coerce')
player_hitting_stats['BABIP'] = pd.to_numeric(player_hitting_stats['BABIP'], errors='coerce')
player_hitting_stats['RC'] = pd.to_numeric(player_hitting_stats['RC'], errors='coerce')
player_hitting_stats['wOBA'] = pd.to_numeric(player_hitting_stats['wOBA'], errors='coerce')
player_hitting_stats['wRAA'] = pd.to_numeric(player_hitting_stats['wRAA'], errors='coerce')
player_hitting_stats['wRAA/PA'] = pd.to_numeric(player_hitting_stats['wRAA/PA'], errors='coerce')
player_hitting_stats['wRC'] = pd.to_numeric(player_hitting_stats['wRC'], errors='coerce')
player_hitting_stats['wRC+'] = pd.to_numeric(player_hitting_stats['wRC+'], errors='coerce')

# Creating Dataframe for Visualization
player_hitting_stats1 = player_hitting_stats.drop(columns=['Name','#','Year','Pos'])
player_hitting_stats1['Name (Team)'] = player_hitting_stats['Name'] + ' (' + player_hitting_stats['Team'] + ')'
player_hitting_stats1.loc[:,('Name (Team)')]
player_hitting_stats1.set_index('Name (Team)',inplace=True)
player_hitting_stats2=player_hitting_stats1.drop(columns=['Team'])

# Sorting Lists for Dashboard Components
batting_stat_list=[x for x in player_hitting_stats2.columns if x not in ['Conference', 'Division', 'Qualified']]
batting_player_list = [x for x in player_hitting_stats2.index]
unique_teams = player_hitting_stats1['Team'].unique()


# Registring the Page
dash.register_page(__name__)

# The Pitching Chart Page
layout=dbc.Container(
    children=[
    # Title and Dashboard Explanation
    html.H1('2023 Prospect League Player Hitting Statistics Plots',className='text-center text-dark mt-3 mb-2 fs-1'),
    html.H3('Scatter Plot', className='text-info text-center fs-2 mt-3 mb-0'),
    # The Graph
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Graph(
                    id='scatter_plot',
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
                    id='filter-radio',
                    options=[
                        {'label':'All Prospect League Hitters','value':'all'},
                        {'label':'Qualified Prospect League Hitters','value':'greater_than_2.7'}
                    ],
                    value='all',
                    labelStyle={'display': 'inline-block','margin-right': '10px'},
                    inputStyle={'margin-right': '10px'}
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
                    id='team-dropdown25',
                    options=[{'label': team, 'value': team} for team in unique_teams],
                    multi=True,
                    value=unique_teams
                ),
            ],
            width=10,
            className='mt-4 offset-md-1 mb-3'
        )
    ]),

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
                    id='stat_dropdown1',
                    options=[
                        dict(label=x,value=x) for x in batting_stat_list
                    ],
                    optionHeight=25,
                    className='mt-0 mb-3',
                    value='PA',
                    clearable=False
                )
            ],
            width=4,
            className='offset-md-1'
        ),
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='stat_dropdown2',
                    options=[
                        dict(label=x,value=x) for x in batting_stat_list
                    ],
                    optionHeight=25,
                    className='mt-0 mb-3',
                    value='wRC+',
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
                    id='bar_chart1',
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
                    id='stat_choice1',
                    options=[
                        dict(label=x,value=x) for x in batting_stat_list
                    ],
                    className='mt-1 mb-3',
                    value='wRC+',
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
                    id='player_dropdown1',
                    options=[
                        dict(label=x,value=x) for x in batting_player_list
                    ],
                    multi=True,
                    placeholder='Please select a team to review.',
                    optionHeight=25,
                    className='mt-1 mb-3',
                    value=['Tim Orr (CHI)'],
                    clearable=False
                )
            ],
            width=4,
            className='offset-md-2'
        )
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
    Output('scatter_plot','figure'),
    Output('bar_chart1','figure'),
    Input('filter-radio','value'),
    Input('team-dropdown25','value'),
    Input('stat_dropdown1','value'),
    Input('stat_dropdown2','value'),
    Input('stat_choice1','value'),
    Input('player_dropdown1','value'),
)

def charts(filter_value,selected_teams,stat_selection1,stat_selection2,stat_selection3,player_selection):    
    if filter_value == 'all':
        filtered_data = player_hitting_stats1
    else:
        filtered_data = player_hitting_stats1[player_hitting_stats1['PA/G'] >= 2.7]

    filtered_data = filtered_data[filtered_data['Team'].isin(selected_teams)]

    if len(filtered_data) == 0 and filter_value == 'greater_than_2.7':
        filtered_data = player_hitting_stats1[player_hitting_stats1['PA/G'] >= 2.7]
    elif len(filtered_data) == 0:
        filtered_data = player_hitting_stats1
    
    if len(filtered_data) == 0:
        filtered_data = player_hitting_stats1

    if len(stat_selection3)==0:
        stat_selection3 = ['wRC+']

    if len(player_selection)==0:
        player_selection = ['Tim Orr (CHI)']

    # Making Batting Data Subset
    player_data_subset=player_hitting_stats1.loc[player_selection,stat_selection3].copy().reset_index()

    # Create a new DataFrame with 'Team' as a regular column
    team_column = player_hitting_stats1.loc[player_selection, 'Team'].reset_index()['Team']

    # Add the 'Team' column to the player_data_subset DataFrame
    player_data_subset['Team'] = team_column

        # Pitching Chart
    hitting_scatter_plot=px.scatter(
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

    hitting_scatter_plot.update_xaxes(
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

    hitting_scatter_plot.update_yaxes(
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

    hitting_scatter_plot.update_layout(
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

    hitting_scatter_plot.update_traces(
        marker_size=11,
        marker_line_color='black',
        marker_line_width=1,
        textfont_size=14
)
    
    # Batting Chart
    batting_figure1=px.bar(
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
        }
    )

    batting_figure1.update_xaxes(
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

    batting_figure1.update_yaxes(
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

    batting_figure1.update_layout(
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

    batting_figure1.update_traces(
        marker_line_color='black',
        marker_line_width=0.5,
        textfont_size=14
)

    return hitting_scatter_plot, batting_figure1
