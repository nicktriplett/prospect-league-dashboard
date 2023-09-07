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

# Convert columns to numeric
player_hitting_stats['G'] = pd.to_numeric(player_hitting_stats['G'], errors='coerce')
player_hitting_stats['PA'] = pd.to_numeric(player_hitting_stats['PA'], errors='coerce')
player_hitting_stats['PA/G'] = pd.to_numeric(player_hitting_stats['PA/G'], errors='coerce')
player_hitting_stats['BB%'] = pd.to_numeric(player_hitting_stats['BB%'], errors='coerce')
player_hitting_stats['K%'] = pd.to_numeric(player_hitting_stats['K%'], errors='coerce')
player_hitting_stats['SB%'] = pd.to_numeric(player_hitting_stats['SB%'], errors='coerce')
player_hitting_stats['BABIP'] = pd.to_numeric(player_hitting_stats['BABIP'], errors='coerce')
player_hitting_stats['RC'] = pd.to_numeric(player_hitting_stats['RC'], errors='coerce')

# Creating Dataframe for Visualization
player_hitting_stats1 = player_hitting_stats.drop(columns=['Name','#','Year','Pos'])
player_hitting_stats1['Name (Team)'] = player_hitting_stats['Name'] + ' (' + player_hitting_stats['Team'] + ')'
player_hitting_stats1.loc[:,('Name (Team)')]
player_hitting_stats1.set_index('Name (Team)',inplace=True)
player_hitting_stats2=player_hitting_stats1.drop(columns=['Team'])

# Sorting Lists for Dashboard Components
batting_stat_list=[x for x in player_hitting_stats2.columns]
batting_player_list = [x for x in player_hitting_stats2.index]

# Registring the Page
dash.register_page(__name__)

# The Pitching Chart Page
layout=dbc.Container(
    children=[
    # Title and Dashboard Explanation
    html.H1('2023 Player Scatter Plot',className='text-center text-dark mt-3 mb-2 fs-1'),
    html.H3('Player Hitting Data Scatter Plot', className='text-info text-center fs-2 mt-3 mb-0'),
    # The Graph
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Graph(
                    id='scatter_plot',
                    className='m-4',
                    config=dict(displayModeBar=False),
                ),
            ],
            width=10,
            className='offset-md-1'
        )
    ]),
    # User Commands
        dcc.RadioItems(
            id='filter-radio',
            options=[
                {'label':'All Prospect League Hitters','value':'all'},
                {'label':'Qualified Prospect League Hitters','value':'greater_than_2.7'}
            ],
            value='all',
    ),

    dbc.Row([
        dbc.Col(
            children=[
                html.P('Please select a statistical measure for the X-axis to compare players with.',className='text-center text-dark fs-5 mt-3')
            ],
            width=6
        ),
        dbc.Col(
            children=[
                html.P("Please select a statistical measure for the Y-axis to compare players with.",className='text-center text-dark fs-5 mt-3')
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
                    className='mt-1 mb-3',
                    value='OBP',
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
                    className='mt-1 mb-3',
                    value='SLG',
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
    html.H1('2023 Player Bar Chart',className='text-center text-dark mt-3 mb-2 fs-1'),
    html.H3('Player Batting Data Bar Chart', className='text-info text-center fs-2 mt-3 mb-0'),
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
    Input('stat_dropdown1','value'),
    Input('stat_dropdown2','value'),
    Input('stat_choice1','value'),
    Input('player_dropdown1','value'),
)

def charts(filter_value,stat_selection1,stat_selection2,stat_selection3,player_selection):
    # if active_cell:
    #     cell_data = player_hitting_stats1.iloc[active_cell['row']][active_cell['column_id']]
    #     return f"Data: \"{cell_data}\" from table cell: {active_cell}"
    
    if filter_value == 'all':
        filtered_data = player_hitting_stats1
    else:
        filtered_data = player_hitting_stats1[player_hitting_stats1['PA/G'] >= 2.7]
    
    if len(stat_selection3)==0:
        stat_selection3 = ['OPS']

    if len(player_selection)==0:
        player_selection = ['Tim Orr (CHI)']

    # Making Batting Data Subset
    player_data_subset=player_hitting_stats1.loc[player_selection,stat_selection3].copy().reset_index() 

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
        color='Name (Team)',
        color_discrete_map={
            'A.J. Pabst (ALT)':'#279989',
            'Aiden Joaquin (ALT)':'#279989',
            'Alex Hagen (ALT)':'#279989',
            'Blake Burris (ALT)':'#279989',
            'Brayden Caskey (ALT)':'#279989',
            'Bryce Zupan (ALT)':'#279989',
            'Bryer Arview (ALT)':'#279989',
            'Chase Bloomer (ALT)':'#279989',
            'Cole Yearsley (ALT)':'#279989',
            'Diego Murillo (ALT)':'#279989',
            'Dominic Decker (ALT)':'#279989',
            'Drake Westcott (ALT)':'#279989',
            'Dylan Mass (ALT)':'#279989',
            'Eli Hoerner (ALT)':'#279989',
            'Eli Young (ALT)':'#279989',
            'Erik Broekemeier (ALT)':'#279989',
            'Evan Evola (ALT)':'#279989',
            'Evan Evola (ALT)':'#279989',
            'Jak Sinclair (ALT)':'#279989',
            "Jake O'Steen (ALT)":'#279989',
            'Kaden Byrne (ALT)':'#279989',
            'Kaden Coutts (ALT)':'#279989',
            'Luigi Albano-Dito (ALT)':'#279989',
            'Mattias Sessing (ALT)':'#279989',
            'RJ LaRocco (ALT)':'#279989',
            'Robby Taul (ALT)':'#279989',
            'Tyler Imbach (ALT)':'#279989',
            'Tyler Martin (ALT)':'#279989',
            'Tyson Greene (ALT)':'#279989',
            'Victor Heredia (ALT)':'#279989',
            'Zach Olson (ALT)':'#279989',
            'Brandon Bickford (BRL)':'#FFB81C',
            'Caleb Wulf (BRL)':'#FFB81C',
            'Cedric Dunnwald (BRL)':'#FFB81C',
            'Chase Honeycutt (BRL)':'#FFB81C',
            'Connor Laeng (BRL)':'#FFB81C',
            'Corey Boyette (BRL)':'#FFB81C',
            'Coy Sarsfield (BRL)':'#FFB81C',
            'Drew Gaskins (BRL)':'#FFB81C',
            'Ian Wolski (BRL)':'#FFB81C',
            'Jackson Fisher (BRL)':'#FFB81C',
            'Jaden Hackbarth (BRL)':'#FFB81C',
            'Keanu Spenser (BRL)':'#FFB81C',
            'Keegan Schmitt (BRL)':'#FFB81C',
            'Kooper Schulte (BRL)':'#FFB81C',
            'Lincoln Riley (BRL)':'#FFB81C',
            'Mason Schwalbach (BRL)':'#FFB81C',
            'Mitch Wood (BRL)':'#FFB81C',
            'Nick Tampa (BRL)':'#FFB81C',
            'Tanner Holland (BRL)':'#FFB81C',
            'Trent Rice (BRL)':'#FFB81C',
            'Zach Barden (BRL)':'#FFB81C',
            'Ben Bach (CCY)':'#044283',
            'Ben Zink (CCY)':'#044283',
            'Blake Buzzeo (CCY)':'#044283',
            'Brayden Carter (CCY)':'#044283',
            'Brayden Quincel (CCY)':'#044283',
            'Broc Parmer (CCY)':'#044283',
            'Calin Smith (CCY)':'#044283',
            'Cam Gilkerson (CCY)':'#044283',
            'Carson Womer (CCY)':'#044283',
            'CJ Richmond (CCY)':'#044283',
            'Connor Huzicka (CCY)':'#044283',
            'David Novak (CCY)':'#044283',
            'Eric Fouraker (CCY)':'#044283',
            'Evan Lorey (CCY)':'#044283',
            'Gabe Phipps (CCY)':'#044283',
            'Hilario DeLaPaz III (CCY)':'#044283',
            'Jake Sherman (CCY)':'#044283',
            'Lucas Day (CCY)':'#044283',
            'Nate Manley (CCY)':'#044283',
            'Nikolas Pereira (CCY)':'#044283',
            'Ryan Robinson (CCY)':'#044283',
            'Sam Seeker (CCY)':'#044283',
            'Skylar Mays (CCY)':'#044283',
            'Tyler Cox (CCY)':'#044283',
            'Zach Cabell (CCY)':'#044283',
            'Brody Chrisman (CGR)':'#78BE21',
            'Caden Bogenpohl (CGR)':'#78BE21',
            'Cal Kilgore (CGR)':'#78BE21',
            'Chris Hall (CGR)':'#78BE21',
            'Creek Robertson (CGR)':'#78BE21',
            'Curry Sutherland (CGR)':'#78BE21',
            'Dante Zamudio (CGR)':'#78BE21',
            'Dee Triplett (CGR)':'#78BE21',
            'Hayden Nazarenus (CGR)':'#78BE21',
            'Jack Dunn (CGR)':'#78BE21',
            'Jacob Baller (CGR)':'#78BE21',
            'Jacob Danneman (CGR)':'#78BE21',
            'Jeff Clarke (CGR)':'#78BE21',
            'Jude Putz (CGR)':'#78BE21',
            'Justin Carinci (CGR)':'#78BE21',
            'Kaden Jeffries (CGR)':'#78BE21',
            'Kevin Balfe (CGR)':'#78BE21',
            'Kevin McCarthy (CGR)':'#78BE21',
            'Kolten Poorman (CGR)':'#78BE21',
            'Landon Godsey (CGR)':'#78BE21',
            'Lane Crowden (CGR)':'#78BE21',
            'Quinton Borders (CGR)':'#78BE21',
            'Scott Shuler (CGR)':'#78BE21',
            'Tucker Stockman (CGR)':'#78BE21',
            'Arturo Disla (CHI)':'#BA0C2F',
            'Brayden White (CHI)':'#BA0C2F',
            'Brayton Bowen (CHI)':'#BA0C2F',
            'Caleb Vaughn (CHI)':'#BA0C2F',
            'Cameron Bowen (CHI)':'#BA0C2F',
            'Cameron Macon (CHI)':'#BA0C2F',
            'CJ Carmichael (CHI)':'#BA0C2F',
            'CJ Dean (CHI)':'#BA0C2F',
            'Cole Kwiatkowski (CHI)':'#BA0C2F',
            'Drew Donaldson (CHI)':'#BA0C2F',
            'Gavin Ganun (CHI)':'#BA0C2F',
            'Jack Gidcumb (CHI)':'#BA0C2F',
            'Jimmy Nugent (CHI)':'#BA0C2F',
            'Mason Eckelman (CHI)':'#BA0C2F',
            'Max Whitesell (CHI)':'#BA0C2F',
            'Nate Dorinsky (CHI)':'#BA0C2F',
            'Owen Wilson (CHI)':'#BA0C2F',
            'Sammy Stoner (CHI)':'#BA0C2F',
            'Sean Kolenich (CHI)':'#BA0C2F',
            'Tim Orr (CHI)':'#BA0C2F',
            'Tyler Mendez (CHI)':'#BA0C2F',
            'Tyler Shaneyfelt (CHI)':'#BA0C2F',
            'Victor Figueroa (CHI)':'#BA0C2F',
            'Alex Diaz (CLN)':'#00843D',
            'Andy Nelson (CLN)':'#00843D',
            'Brandon Vicko (CLN)':'#00843D',
            'Brock Wollin (CLN)':'#00843D',
            'Carson Lydon (CLN)':'#00843D',
            'Casen Neumann (CLN)':'#00843D',
            'Casey Hintz (CLN)':'#00843D',
            'Connor Giusti (CLN)':'#00843D',
            'Darrell Michael Jean (CLN)':'#00843D',
            'Dylan DeButy (CLN)':'#00843D',
            'Gavin Brzozowski (CLN)':'#00843D',
            'Jai Jensen (CLN)':'#00843D',
            'Jeremy Conforti (CLN)':'#00843D',
            'Jeremy Figueroa (CLN)':'#00843D',
            'Kyle Lehmann (CLN)':'#00843D',
            'Logan Romasanta (CLN)':'#00843D',
            'Matt Scherrman (CLN)':'#00843D',
            'Max Holy (CLN)':'#00843D',
            'Nick Meyer (CLN)':'#00843D',
            'Parker Shupe (CLN)':'#00843D',
            'Patrick McGinn (CLN)':'#00843D',
            'Paul Schuyler III (CLN)':'#00843D',
            'Paul Vossen (CLN)':'#00843D',
            'Sam Lavin (CLN)':'#00843D',
            'Sebastian Parchomenko (CLN)':'#00843D',
            'Tate Gillen (CLN)':'#00843D',
            'Trevor Burkhart (CLN)':'#00843D',
            'Turner Doran (CLN)':'#00843D',
            'Will MacLean (CLN)':'#00843D',
            'Will Stark (CLN)':'#00843D',
            'Zachary Mazoch (CLN)':'#00843D',
            'Adam Ebling (DAN)':'#D22730',
            'Blake Binderup (DAN)':'#D22730',
            'Brandon Bishop (DAN)':'#D22730',
            'Caleb Pittman (DAN)':'#D22730',
            'Carlos Vasquez (DAN)':'#D22730',
            'Chase Vinson (DAN)':'#D22730',
            'Cole Tremain (DAN)':'#D22730',
            'DJ Akiyama (DAN)':'#D22730',
            'Drake Digiorno (DAN)':'#D22730',
            'Enas Hayden (DAN)':'#D22730',
            'Haiden Walters (DAN)':'#D22730',
            'Hank Bard (DAN)':'#D22730',
            'Jackson Micheels (DAN)':'#D22730',
            'Jake Stadler (DAN)':'#D22730',
            'Joe Siciliano (DAN)':'#D22730',
            'Johnny Colombo (DAN)':'#D22730',
            'JT Crabbe (DAN)':'#D22730',
            'JT Waldon (DAN)':'#D22730',
            'Julio Cajigas (DAN)':'#D22730',
            'Justin Vossos (DAN)':'#D22730',
            'Lance Gardiner (DAN)':'#D22730',
            'Nate Chester (DAN)':'#D22730',
            'Nate Vargas (DAN)':'#D22730',
            'Rance Bryant (DAN)':'#D22730',
            'Robert Castillo (DAN)':'#D22730',
            'Ryan Jackson (DAN)':'#D22730',
            'Sammy Leis (DAN)':'#D22730',
            'Trenton Pallas (DAN)':'#D22730',
            'Trey Higgins (DAN)':'#D22730',
            'Wyatt King (DAN)':'#D22730',
            'Alton Gyselman (IVY)':'#FF8200',
            'Anthony Fornero (IVY)':'#FF8200',
            'Brayden Bakes (IVY)':'#FF8200',
            'Brendan Comerford (IVY)':'#FF8200',
            'Chance Resetich (IVY)':'#FF8200',
            'Christian Graves (IVY)':'#FF8200',
            'Cody Kashimoto (IVY)':'#FF8200',
            'Daniel Strohm (IVY)':'#FF8200',
            'David Andolina (IVY)':'#FF8200',
            'Emanuel Andujar (IVY)':'#FF8200',
            'Evan Evola (IVY)':'#FF8200',
            'Evan Evola (IVY)':'#FF8200',
            'Isaiah Hart (IVY)':'#FF8200',
            'Jake Ferguson (IVY)':'#FF8200',
            'Jake Zitella (IVY)':'#FF8200',
            'Jason Shanner (IVY)':'#FF8200',
            'Joseph Stagowski (IVY)':'#FF8200',
            'Justin Rios (IVY)':'#FF8200',
            'Kedren Kinzie (IVY)':'#FF8200',
            'Kyle Beach (IVY)':'#FF8200',
            'Logan Delgado (IVY)':'#FF8200',
            'Logan Gregorio (IVY)':'#FF8200',
            'Louis Perona (IVY)':'#FF8200',
            'Max Handron (IVY)':'#FF8200',
            'Nick Chavez (IVY)':'#FF8200',
            'Nico Azpilcueta (IVY)':'#FF8200',
            'Noah Malone (IVY)':'#FF8200',
            'River Scott (IVY)':'#FF8200',
            'Robert Marinec (IVY)':'#FF8200',
            'Ryan Bakes (IVY)':'#FF8200',
            'Sam Corbett (IVY)':'#FF8200',
            'Sebastian Gonzalez (IVY)':'#FF8200',
            'Tobey Jackson (IVY)':'#FF8200',
            'Tristan Kerr (IVY)':'#FF8200',
            'Tyler Dorsch (IVY)':'#FF8200',
            'Tyler Patton (IVY)':'#FF8200',
            'Will Worthington (IVY)':'#FF8200',
            'Xander Sielken (IVY)':'#FF8200',
            'Zach Lane (IVY)':'#FF8200',
            'Aden Johnson (JAX)':'#84329B',
            'Aydan Hamilton (JAX)':'#84329B',
            'Ben Smith (JAX)':'#84329B',
            'Braden Becker (JAX)':'#84329B',
            'Braden Vinyard (JAX)':'#84329B',
            'Brady Wilson (JAX)':'#84329B',
            'Brandon Valdez (JAX)':'#84329B',
            'Brett Blankenship (JAX)':'#84329B',
            'Bryce Dreher (JAX)':'#84329B',
            'Carter Vrabel (JAX)':'#84329B',
            'Chris Godwin (JAX)':'#84329B',
            'Cole McCallum (JAX)':'#84329B',
            'Cruz Valencia (JAX)':'#84329B',
            'Dalton Rudd (JAX)':'#84329B',
            'Duncan Mathews (JAX)':'#84329B',
            'Dylan LaRue (JAX)':'#84329B',
            'Garrett Lance (JAX)':'#84329B',
            'Griffin Cameron (JAX)':'#84329B',
            'Harrison Freeman (JAX)':'#84329B',
            'Hayden Collins (JAX)':'#84329B',
            'Hudson Cepparulo (JAX)':'#84329B',
            'Jake Keyl (JAX)':'#84329B',
            'Jake McCutcheon (JAX)':'#84329B',
            'James Denten (JAX)':'#84329B',
            'Jaxin Settlemires (JAX)':'#84329B',
            'Joseph Hufstedler (JAX)':'#84329B',
            'Kevin Okins (JAX)':'#84329B',
            'Luke Lowery (JAX)':'#84329B',
            'Mason Krznarich (JAX)':'#84329B',
            'Matthew Beuka (JAX)':'#84329B',
            'Michael Bell (JAX)':'#84329B',
            'Nicho Jordan (JAX)':'#84329B',
            'Nick Stamper (JAX)':'#84329B',
            'Preston Ford (JAX)':'#84329B',
            'Traeshon Hall (JAX)':'#84329B',
            'Tyler Heckert (JAX)':'#84329B',
            'Tyler Macon (JAX)':'#84329B',
            'Walton Thompson (JAX)':'#84329B',
            'Wesley Mann (JAX)':'#84329B',
            'Austin Baal (JNT)':'#3E342F',
            'Bobby Lane (JNT)':'#3E342F',
            'Brad Vargas (JNT)':'#3E342F',
            'Brennan Murphy (JNT)':'#3E342F',
            'Bump Burgreen (JNT)':'#3E342F',
            'Clay Wiesen (JNT)':'#3E342F',
            'Cole Yeager (JNT)':'#3E342F',
            'Dan Merkel (JNT)':'#3E342F',
            'Dylan Gray (JNT)':'#3E342F',
            'Eli Sutton (JNT)':'#3E342F',
            'Forrest Havanis (JNT)':'#3E342F',
            'Gage Gillott (JNT)':'#3E342F',
            'Gio Calamia (JNT)':'#3E342F',
            'Jack Rogers (JNT)':'#3E342F',
            'Jake Baumgartner (JNT)':'#3E342F',
            'Jake Kendro (JNT)':'#3E342F',
            'Jalen Freeman (JNT)':'#3E342F',
            'Jeremy Delamota (JNT)':'#3E342F',
            'Joe Alcorn (JNT)':'#3E342F',
            'Justin Mauer (JNT)':'#3E342F',
            'Lance MacDonald (JNT)':'#3E342F',
            'Matt Santarelli (JNT)':'#3E342F',
            'Matthew Benton (JNT)':'#3E342F',
            'Matthew Kenney, Jr. (JNT)':'#3E342F',
            'Max Beaulieu (JNT)':'#3E342F',
            'Michael Klingensmith (JNT)':'#3E342F',
            'Miguel Vega (JNT)':'#3E342F',
            'Morgan Wyatt (JNT)':'#3E342F',
            'Phil Fox (JNT)':'#3E342F',
            'Randy Carlo IV (JNT)':'#3E342F',
            'Ryan Sylvester (JNT)':'#3E342F',
            'Scotty McManamon (JNT)':'#3E342F',
            'Tyler Horvat (JNT)':'#3E342F',
            'Tyler Quade (JNT)':'#3E342F',
            'Tyson Bryant-Dawson (JNT)':'#3E342F',
            'Xavier Baker (JNT)':'#3E342F',
            'Aiden Hinds (LAF)':'#FFC82F',
            'Brandon Daniels (LAF)':'#FFC82F',
            'Brody Williams (LAF)':'#FFC82F',
            'Brooks Sailors (LAF)':'#FFC82F',
            'Camden Gasser (LAF)':'#FFC82F',
            'Cameron Nagel (LAF)':'#FFC82F',
            'Clay Shelton (LAF)':'#FFC82F',
            'Evan Liddie (LAF)':'#FFC82F',
            'Jack Taulman (LAF)':'#FFC82F',
            'Jacob Walker (LAF)':'#FFC82F',
            'James Jett (LAF)':'#FFC82F',
            'Jared Evans (LAF)':'#FFC82F',
            'Joe Olsavsky (LAF)':'#FFC82F',
            'Joey Humphrey (LAF)':'#FFC82F',
            'John Hoskyn (LAF)':'#FFC82F',
            'Josiah Miller (LAF)':'#FFC82F',
            'Mack Whitcomb (LAF)':'#FFC82F',
            'Mason Kelley (LAF)':'#FFC82F',
            'Max Mandler (LAF)':'#FFC82F',
            'Mikey Scott (LAF)':'#FFC82F',
            'Parker Harrison (LAF)':'#FFC82F',
            'Sebastian Kuhns (LAF)':'#FFC82F',
            'Tripp Davis (LAF)':'#FFC82F',
            'Aaron Bock (NOR)':'#2C5234',
            'Ben Higgins (NOR)':'#2C5234',
            'Ben Karpowicz (NOR)':'#2C5234',
            'Camden Ruby (NOR)':'#2C5234',
            'Carson Wadel (NOR)':'#2C5234',
            'Case Sanderson (NOR)':'#2C5234',
            'Chase Mason (NOR)':'#2C5234',
            'Clay Conn (NOR)':'#2C5234',
            'Colin Kalinowski (NOR)':'#2C5234',
            'Daniel Young (NOR)':'#2C5234',
            'Easton Harris (NOR)':'#2C5234',
            'Ethan Willoughby (NOR)':'#2C5234',
            'J.D. Bogart (NOR)':'#2C5234',
            'Jackson Blemler (NOR)':'#2C5234',
            'Jackson Chatterton (NOR)':'#2C5234',
            'James Harris (NOR)':'#2C5234',
            'Joey Hagen (NOR)':'#2C5234',
            'Kannon Kleine (NOR)':'#2C5234',
            'Max Jones (NOR)':'#2C5234',
            'Payton Mansfield (NOR)':'#2C5234',
            'Peter Johnson (NOR)':'#2C5234',
            'Peyton Dillingham (NOR)':'#2C5234',
            'PJ Rogan (NOR)':'#2C5234',
            'Scott Newman (NOR)':'#2C5234',
            'Sean McGurk (NOR)':'#2C5234',
            "Timmy O'Brien (NOR)":'#2C5234',
            'Tyler Bickers (NOR)':'#2C5234',
            'Tyler Castro (NOR)':'#2C5234',
            'Tyler Woltman (NOR)':'#2C5234',
            'Angelo Luna (OFL)':'#010101',
            'Brady Kindhart (OFL)':'#010101',
            'Braedon Stoakes (OFL)':'#010101',
            'Cameron Hailstone (OFL)':'#010101',
            'Chase Beattie (OFL)':'#010101',
            'Chase Becker (OFL)':'#010101',
            'Drew Mize (OFL)':'#010101',
            'Drew Politte (OFL)':'#010101',
            'Ethan Rossow (OFL)':'#010101',
            'Gavin Baldwin (OFL)':'#010101',
            'Ivan Dahlberg (OFL)':'#010101',
            'Jack Meyer (OFL)':'#010101',
            'Jacob Rowold (OFL)':'#010101',
            'Jake Vitale (OFL)':'#010101',
            'John Stallcup (OFL)':'#010101',
            'Maloy Heaghney (OFL)':'#010101',
            'Matthew Arnold (OFL)':'#010101',
            'Michael Long (OFL)':'#010101',
            'Mike Maloney (OFL)':'#010101',
            "Mike O'Conor (OFL)":'#010101',
            'Nick Harms (OFL)':'#010101',
            'Rhett Hendricks (OFL)':'#010101',
            'Tucker Platt (OFL)':'#010101',
            'Tyler Ferguson (OFL)':'#010101',
            'Tyson Ludwig (OFL)':'#010101',
            'Zach Beatty (OFL)':'#010101',
            'Andrew Fay (QUI)':'#E4002B',
            'Cam Suto (QUI)':'#E4002B',
            'Charles Schebler (QUI)':'#E4002B',
            'Chase Chappell (QUI)':'#E4002B',
            'Cross Jumper (QUI)':'#E4002B',
            'Easton Mains (QUI)':'#E4002B',
            'Harrison Blueweiss (QUI)':'#E4002B',
            'Harry Fandre (QUI)':'#E4002B',
            'Harry Oden (QUI)':'#E4002B',
            'Jack Zebig (QUI)':'#E4002B',
            'Jaison Andujar (QUI)':'#E4002B',
            'Jimmy Koza (QUI)':'#E4002B',
            'Joe Huffman (QUI)':'#E4002B',
            'Joe Siervo (QUI)':'#E4002B',
            'Jordan Scott (QUI)':'#E4002B',
            'Kyle Hvidsten (QUI)':'#E4002B',
            'Logan Voth (QUI)':'#E4002B',
            'Lucas Loos (QUI)':'#E4002B',
            'Luke Jessen (QUI)':'#E4002B',
            'Nathan VerMaas (QUI)':'#E4002B',
            'Otto Jones (QUI)':'#E4002B',
            'Riley Black (QUI)':'#E4002B',
            'Tristan Meny (QUI)':'#E4002B',
            'Aidan McNamee (SPR)':'#072B31',
            'Anthony Stellato (SPR)':'#072B31',
            'Brady Small (SPR)':'#072B31',
            'Brandon Hager (SPR)':'#072B31',
            'Brayden Smith (SPR)':'#072B31',
            'Cade Duffin (SPR)':'#072B31',
            'Charles McCaleb (SPR)':'#072B31',
            'Chris Kustigian (SPR)':'#072B31',
            'Connor Milton (SPR)':'#072B31',
            'Daedrick Cail (SPR)':'#072B31',
            'Dawson Johns (SPR)':'#072B31',
            'Eli Marvin (SPR)':'#072B31',
            'Hunter Moser (SPR)':'#072B31',
            'Jacob Hager (SPR)':'#072B31',
            'Jaylen Morgan (SPR)':'#072B31',
            'Kaden Griffitts (SPR)':'#072B31',
            'Kristian Sprawling (SPR)':'#072B31',
            'Laine Axtetter (SPR)':'#072B31',
            'Mark Kattula (SPR)':'#072B31',
            'Nick Terrell (SPR)':'#072B31',
            'Nolan Self (SPR)':'#072B31',
            'Patrick Graham (SPR)':'#072B31',
            'Payton Matthews (SPR)':'#072B31',
            'Trent Koehler (SPR)':'#072B31',
            'Ty Rhoades (SPR)':'#072B31',
            'William Zareh (SPR)':'#072B31',
            'Zane Danielson (SPR)':'#072B31',
            'Alex Marx (TER)':'#0057B7',
            'Brady Yeryar (TER)':'#0057B7',
            'Brett Sherrard (TER)':'#0057B7',
            'Bryan Kohlmeyer (TER)':'#0057B7',
            'Bryce Miller (TER)':'#0057B7',
            'Caleb Hohman (TER)':'#0057B7',
            'Camden Karczewski (TER)':'#0057B7',
            'Carter Murphy (TER)':'#0057B7',
            "CJ O'Dell (TER)":'#0057B7',
            'Clay Hendry (TER)':'#0057B7',
            'Derek Lebron (TER)':'#0057B7',
            'Dominic Krupinski (TER)':'#0057B7',
            'Ethan Burdette (TER)':'#0057B7',
            'Gabe Wright (TER)':'#0057B7',
            'Jayden Lepper (TER)':'#0057B7',
            'Jayson Cottrell (TER)':'#0057B7',
            'Jean Gonzalez (TER)':'#0057B7',
            'Jeremy Piatkiewicz (TER)':'#0057B7',
            'Joe Hamilton (TER)':'#0057B7',
            'Justin Bogard (TER)':'#0057B7',
            'Kaleb Marrs (TER)':'#0057B7',
            'Keegan Garis (TER)':'#0057B7',
            'Matthew Albritton (TER)':'#0057B7',
            'Morgan Colopy (TER)':'#0057B7',
            'Nathan Frady (TER)':'#0057B7',
            'Nazhir Bergen (TER)':'#0057B7',
            'Nolan Miller (TER)':'#0057B7',
            'Payton Howard (TER)':'#0057B7',
            'Sam Pesa (TER)':'#0057B7',
            'Slater Schield (TER)':'#0057B7',
            'Steven Walsh (TER)':'#0057B7',
            'Tripper Capps (TER)':'#0057B7',
            'Warren Bailey (TER)':'#0057B7',
            'Xavier Croxton (TER)':'#0057B7',
            'Zacheus Carr (TER)':'#0057B7',
            'Alex Wilson (THR)':'#FF8F1C',
            'Alex Zimmerman (THR)':'#FF8F1C',
            'Andrew Schroeder (THR)':'#FF8F1C',
            'Bryce Toci (THR)':'#FF8F1C',
            'Bryson Arnette (THR)':'#FF8F1C',
            'Cameron Hill (THR)':'#FF8F1C',
            'Charlie Corum (THR)':'#FF8F1C',
            'Chase Austin (THR)':'#FF8F1C',
            'Cole Smith (THR)':'#FF8F1C',
            'Dylan Drumke (THR)':'#FF8F1C',
            'Evan McCarthy (THR)':'#FF8F1C',
            'Grant Palmer (THR)':'#FF8F1C',
            'Hayden Ralls (THR)':'#FF8F1C',
            'Jackson Cooke (THR)':'#FF8F1C',
            'Jackson Lindsey (THR)':'#FF8F1C',
            'Jackson McCoy (THR)':'#FF8F1C',
            'Jaden Correa (THR)':'#FF8F1C',
            'Jake Munroe (THR)':'#FF8F1C',
            'Josh Griffin (THR)':'#FF8F1C',
            'Kaleb Herbert (THR)':'#FF8F1C',
            'Michael Mylott (THR)':'#FF8F1C',
            'Nick Oyster (THR)':'#FF8F1C',
            'Virgil Smith (THR)':'#FF8F1C',
            'TOTALS (-)':'c0c0c0',
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
