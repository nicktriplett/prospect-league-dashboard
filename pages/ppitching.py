# Player Pitching Page

import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Loading Data for Visualizations
player_pitching_stats = pd.read_csv(r"C:\Users\Nick Triplett\OneDrive\Documents\Thrillville Thrillbillies\pl_player_pitching_stats.csv")

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

# Creating Dataframe for Visualization
player_pitching_stats1 = player_pitching_stats.drop(columns=['Name','#','Year','Pos'])
player_pitching_stats1['Name (Team)'] = player_pitching_stats['Name'] + ' (' + player_pitching_stats['Team'] + ')'
player_pitching_stats1.loc[:,('Name (Team)')]
player_pitching_stats1.set_index('Name (Team)',inplace=True)
player_pitching_stats2=player_pitching_stats1.drop(columns=['Team'])

# Sorting Lists for Dashboard Components
batting_stat_list=[x for x in player_pitching_stats2.columns]
batting_player_list = [x for x in player_pitching_stats2.index]

# Registring the Page
dash.register_page(__name__)

# The Pitching Chart Page
layout=dbc.Container(
    children=[
    # Title and Dashboard Explanation
    html.H1('2023 Player Scatter Plot',className='text-center text-info mt-3 mb-2 fs-1'),
    html.H3('Player Pitching Data Scatter Plot', className='text-dark text-center fs-2 mt-3 mb-0'),
    # The Graph
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Graph(
                    id='scatter_plot5',
                    className='m-4',
                    config=dict(displayModeBar=False),
                ),
            ],
            width=10,
            className='offset-md-1'
        )
    ]),

    dcc.RadioItems(
        id='filter-radio1',
        options=[
            {'label':'All Prospect League Pitchers','value':'all'},
            {'label':'Qualified Prospect League Pitchers','value':'greater_than_0.8'}
        ],
        value='all',
    ),
    # User Commands
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
                    id='stat_dropdown5',
                    options=[
                        dict(label=x,value=x) for x in batting_stat_list
                    ],
                    optionHeight=25,
                    className='mt-1 mb-3',
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
                    className='mt-1 mb-3',
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
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    # Title and Dashboard Explanation
    html.H1('2023 Player Bar Chart',className='text-center text-dark mt-3 mb-2 fs-1'),
    html.H3('Player Pitching Data Bar Chart', className='text-info text-center fs-2 mt-3 mb-0'),
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
                    value=['Ryan Daly (THR)'],
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
    Output('scatter_plot5','figure'),
    Output('bar_chart7','figure'),
    Input('filter-radio1','value'),
    Input('stat_dropdown5','value'),
    Input('stat_dropdown6','value'),
    Input('stat_choice9','value'),
    Input('player_dropdown0','value')
)

def charts(filter_value1,stat_selection1,stat_selection2,stat_selection3,player_selection):
    if filter_value1 == 'all':
        filtered_data = player_pitching_stats1
    else:
        filtered_data = player_pitching_stats1[player_pitching_stats1['IP/G'] >= 0.8]
    
    
    
    if len(stat_selection3)==0:
        stat_selection3 = ['ERA']

    if len(player_selection)==0:
        player_selection = ['Ryan Daly (THR)']

    # Making Batting Data Subset
    player_data_subset=player_pitching_stats1.loc[player_selection,stat_selection3].copy().reset_index() 
    
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
        color='Name (Team)',
        color_discrete_map={
            'A.J. Pabst (ALT)':'#279989',
            'Adam Stilts (ALT)':'#279989',
            'Aiden Joaquin (ALT)':'#279989',
            'Alex Renfrow (ALT)':'#279989',
            'Alex Rodriguez (ALT)':'#279989',
            'Bryce Zupan (ALT)':'#279989',
            'Bryer Arview (ALT)':'#279989',
            'Carson Richardson (ALT)':'#279989',
            'Charlie Hodges (ALT)':'#279989',
            'Colin Hawkins (ALT)':'#279989',
            'Dimitri Ivetic (ALT)':'#279989',
            'Dominic Decker (ALT)':'#279989',
            'Eli Hoerner (ALT)':'#279989',
            'Erik Broekemeier (ALT)':'#279989',
            'Evan Gray (ALT)':'#279989',
            'J.T. Miller (ALT)':'#279989',
            'Jackson Parrill (ALT)':'#279989',
            'Jak Sinclair (ALT)':'#279989',
            'Jake Bockenstedt (ALT)':'#279989',
            'Kalen Reardon (ALT)':'#279989',
            'Kyle Athmer (ALT)':'#279989',
            'Kyle Dixon (ALT)':'#279989',
            'Lucas Johns (ALT)':'#279989',
            'Luigi Albano-Dito (ALT)':'#279989',
            'Luke Gasser (ALT)':'#279989',
            'Nolan Wilson (ALT)':'#279989',
            'RJ LaRocco (ALT)':'#279989',
            'Scott Detweiler (ALT)':'#279989',
            'Tyson Greene (ALT)':'#279989',
            'Victor Heredia (ALT)':'#279989',
            'Zach Olson (ALT)':'#279989',
            'Adrian Nery (BRL)':'#FFB81C',
            'Aiden McGee (BRL)':'#FFB81C',
            'Boyd Skelley (BRL)':'#FFB81C',
            'Cauy Massner (BRL)':'#FFB81C',
            'Chase Golden (BRL)':'#FFB81C',
            'Colton Clarahan (BRL)':'#FFB81C',
            'Connor Lyons (BRL)':'#FFB81C',
            'David Theriot (BRL)':'#FFB81C',
            'Drew Martin (BRL)':'#FFB81C',
            'Jacob Zahner (BRL)':'#FFB81C',
            'Jaden Siemer (BRL)':'#FFB81C',
            'Jake Jakubowski (BRL)':'#FFB81C',
            'Jared Townsend (BRL)':'#FFB81C',
            'Jeremy Fox (BRL)':'#FFB81C',
            'Jordan Martinez (BRL)':'#FFB81C',
            'Kyle Looper (BRL)':'#FFB81C',
            'Matthew Dinae (BRL)':'#FFB81C',
            'Nick Tampa (BRL)':'#FFB81C',
            'Preston Kaufman (BRL)':'#FFB81C',
            'Reece Wissinger (BRL)':'#FFB81C',
            'Rem Maxwell (BRL)':'#FFB81C',
            'Ryan Donley (BRL)':'#FFB81C',
            'Zach Leuschen (BRL)':'#FFB81C',
            'Zane Frese (BRL)':'#FFB81C',
            'Andrew DeWitt (CCY)':'#044283',
            'Ben Zink (CCY)':'#044283',
            'Cam Gilkerson (CCY)':'#044283',
            'Carson Womer (CCY)':'#044283',
            'Charlie Schafer (CCY)':'#044283',
            'Cole Agemy (CCY)':'#044283',
            'Colin Ames (CCY)':'#044283',
            'Connor Huzicka (CCY)':'#044283',
            'Daewin Spence (CCY)':'#044283',
            'Ethan Conley (CCY)':'#044283',
            'Evan Lorey (CCY)':'#044283',
            'Gabe Phipps (CCY)':'#044283',
            'Garrett Peters (CCY)':'#044283',
            'Gercal Reyes (CCY)':'#044283',
            'Hilario DeLaPaz III (CCY)':'#044283',
            'Jake Woolf (CCY)':'#044283',
            'Johnathon Ray (CCY)':'#044283',
            'Kyle Kesel (CCY)':'#044283',
            'Lucas Day (CCY)':'#044283',
            'Luke Myers (CCY)':'#044283',
            'Luke Swanger (CCY)':'#044283',
            'Michael Moore (CCY)':'#044283',
            'Nate Manley (CCY)':'#044283',
            'Noah Curi (CCY)':'#044283',
            'Zach Cabell (CCY)':'#044283',
            'Alex Esker (CGR)':'#78BE21',
            'Breven Yarbro (CGR)':'#78BE21',
            'Bryce Morgan (CGR)':'#78BE21',
            'Caden Bogenpohl (CGR)':'#78BE21',
            'Cameron Marchi (CGR)':'#78BE21',
            'Camron Lewis (CGR)':'#78BE21',
            'Curry Sutherland (CGR)':'#78BE21',
            'Dante Zamudio (CGR)':'#78BE21',
            'Devyn Terbrak (CGR)':'#78BE21',
            'Dylan Peck (CGR)':'#78BE21',
            'Eddie White (CGR)':'#78BE21',
            'Jeff Clarke (CGR)':'#78BE21',
            'Jordan Riley (CGR)':'#78BE21',
            'Jorge Romero (CGR)':'#78BE21',
            'Kaden Jeffries (CGR)':'#78BE21',
            'Kam Dohogne (CGR)':'#78BE21',
            'Kole Turner (CGR)':'#78BE21',
            'Kolten Poorman (CGR)':'#78BE21',
            'Marshall Brown (CGR)':'#78BE21',
            'Noah Gadberry (CGR)':'#78BE21',
            'Raymond Ochoa (CGR)':'#78BE21',
            'AJ Clegg (CHI)':'#BA0C2F',
            'Bryson Brown (CHI)':'#BA0C2F',
            'Caden Kline (CHI)':'#BA0C2F',
            'Cameron Macon (CHI)':'#BA0C2F',
            'Chad Rogers (CHI)':'#BA0C2F',
            'Cole Pauley (CHI)':'#BA0C2F',
            'Colin Bryant (CHI)':'#BA0C2F',
            'Dylan Dudones (CHI)':'#BA0C2F',
            'Jackson Bergman (CHI)':'#BA0C2F',
            'Jared Adams (CHI)':'#BA0C2F',
            'Landen Vance (CHI)':'#BA0C2F',
            'Luke Walter (CHI)':'#BA0C2F',
            'Max Whitesell (CHI)':'#BA0C2F',
            'Mikey Olivieri (CHI)':'#BA0C2F',
            'Nate Ginsburg (CHI)':'#BA0C2F',
            'Nate Ryhlick (CHI)':'#BA0C2F',
            'Nick Falter (CHI)':'#BA0C2F',
            'Sammy Stoner (CHI)':'#BA0C2F',
            'Scotty Adelman (CHI)':'#BA0C2F',
            'Todd Bangtson (CHI)':'#BA0C2F',
            'Tyler Mendez (CHI)':'#BA0C2F',
            'Victor Figueroa (CHI)':'#BA0C2F',
            'Will Rettig (CHI)':'#BA0C2F',
            'Alex Windey (CLN)':'#00843D',
            'Ben DeTaeye (CLN)':'#00843D',
            'Brady Schiesl (CLN)':'#00843D',
            'Brock Reade (CLN)':'#00843D',
            'Cade Turner (CLN)':'#00843D',
            'Carson Lydon (CLN)':'#00843D',
            'Coby Greiner (CLN)':'#00843D',
            'Drew Duckhorn (CLN)':'#00843D',
            'Drew Dykstra (CLN)':'#00843D',
            'Drew Proskovec (CLN)':'#00843D',
            'Evan Bender (CLN)':'#00843D',
            'Evan Chung (CLN)':'#00843D',
            'Graysen Drezek (CLN)':'#00843D',
            'Jack Turgasen (CLN)':'#00843D',
            'Jack Young (CLN)':'#00843D',
            'Jackson Bruno (CLN)':'#00843D',
            'Jai Jensen (CLN)':'#00843D',
            'Jared Simpson (CLN)':'#00843D',
            'Jimmy Burke (CLN)':'#00843D',
            'Johnny Czeslawski (CLN)':'#00843D',
            'Josh Fleming (CLN)':'#00843D',
            'Kieran Baliey (CLN)':'#00843D',
            'Logan Mullholand (CLN)':'#00843D',
            'Logan Romasanta (CLN)':'#00843D',
            'Logan Schmitt (CLN)':'#00843D',
            'Lorenz Elion (CLN)':'#00843D',
            'Lucas Foley (CLN)':'#00843D',
            'Mason Behn (CLN)':'#00843D',
            'Matt Irvine (CLN)':'#00843D',
            'Nick Scanlon (CLN)':'#00843D',
            'Nile Foss (CLN)':'#00843D',
            'Owen Brauch (CLN)':'#00843D',
            'Sam Lavin (CLN)':'#00843D',
            'Sebastian Parchomenko (CLN)':'#00843D',
            'Turner Doran (CLN)':'#00843D',
            'Tyler Stern (CLN)':'#00843D',
            'Zach Sabers (CLN)':'#00843D',
            'Blake Binderup (DAN)':'#D22730',
            'Caleb Pittman (DAN)':'#D22730',
            'Carter Heninger (DAN)':'#D22730',
            'Carter Krawchuk (DAN)':'#D22730',
            'Carter Sabol (DAN)':'#D22730',
            'Cole Tremain (DAN)':'#D22730',
            'Connor Nation (DAN)':'#D22730',
            'Decker Mac Neil (DAN)':'#D22730',
            'Enas Hayden (DAN)':'#D22730',
            'Gabriel Pancratz (DAN)':'#D22730',
            'Hunter Hoopes (DAN)':'#D22730',
            'Jack Potteiger (DAN)':'#D22730',
            'Jake Inman (DAN)':'#D22730',
            'Jared Casebier (DAN)':'#D22730',
            'John Balok, Jr. (DAN)':'#D22730',
            'Johnny Colombo (DAN)':'#D22730',
            'Luke Nichols (DAN)':'#D22730',
            'Mason Robinson (DAN)':'#D22730',
            'Nick Burns (DAN)':'#D22730',
            'Rance Bryant (DAN)':'#D22730',
            'Robert Castillo (DAN)':'#D22730',
            'Tyler Fay (DAN)':'#D22730',
            'Will Jacobson (DAN)':'#D22730',
            'Andrew Zemaitis (IVY)':'#FF8200',
            'Brendan Comerford (IVY)':'#FF8200',
            'Bret Baldus (IVY)':'#FF8200',
            'Christian Graves (IVY)':'#FF8200',
            'Cody Kashimoto (IVY)':'#FF8200',
            'Cristian Padilla (IVY)':'#FF8200',
            'Daniel Strohm (IVY)':'#FF8200',
            'Daniel Vogt (IVY)':'#FF8200',
            'David Andolina (IVY)':'#FF8200',
            'Evan Clark (IVY)':'#FF8200',
            "Finn O'Meara (IVY)":'#FF8200',
            'Gage Burdick (IVY)':'#FF8200',
            'Griffin Sleyko (IVY)':'#FF8200',
            'Jake Ferguson (IVY)':'#FF8200',
            'Jared Herzog (IVY)':'#FF8200',
            'Jason Shanner (IVY)':'#FF8200',
            'Joey Cecola (IVY)':'#FF8200',
            'Juju Thompson (IVY)':'#FF8200',
            'Justin Lane (IVY)':'#FF8200',
            'Justin Rios (IVY)':'#FF8200',
            'Kedren Kinzie (IVY)':'#FF8200',
            'Kyle Wisch (IVY)':'#FF8200',
            'Louis Perona (IVY)':'#FF8200',
            'Nico Azpilcueta (IVY)':'#FF8200',
            'Noah Malone (IVY)':'#FF8200',
            'River Scott (IVY)':'#FF8200',
            'Ryan Keeley (IVY)':'#FF8200',
            'Sam Corbett (IVY)':'#FF8200',
            'Sebastian Gonzalez (IVY)':'#FF8200',
            'Tobey Jackson (IVY)':'#FF8200',
            'Tyler Conklin (IVY)':'#FF8200',
            'Tyler Dorsch (IVY)':'#FF8200',
            'Will Worthington (IVY)':'#FF8200',
            'Zach Lane (IVY)':'#FF8200',
            'Aden Johnson (JAX)':'#84329B',
            'Avery Hastings (JAX)':'#84329B',
            'Balfour Roe (JAX)':'#84329B',
            'Braden Becker (JAX)':'#84329B',
            'Bryce Dreher (JAX)':'#84329B',
            'Cade Davis (JAX)':'#84329B',
            'Chance Arender (JAX)':'#84329B',
            'Cole McCallum (JAX)':'#84329B',
            'Colton Brumley (JAX)':'#84329B',
            'Dalton Rudd (JAX)':'#84329B',
            'Danton Rinehart (JAX)':'#84329B',
            'Ethan Orwig (JAX)':'#84329B',
            'Harrison Freeman (JAX)':'#84329B',
            'Hayden Collins (JAX)':'#84329B',
            'Jack Hearn (JAX)':'#84329B',
            'Jake McCutcheon (JAX)':'#84329B',
            'Jamal Allen (JAX)':'#84329B',
            'James Denten (JAX)':'#84329B',
            'JD Klug (JAX)':'#84329B',
            'JJ Gray (JAX)':'#84329B',
            'Josh Furtado (JAX)':'#84329B',
            'Juwan Fitch (JAX)':'#84329B',
            'Kyle Lambert (JAX)':'#84329B',
            'Mason Krznarich (JAX)':'#84329B',
            'Noah Pridmore (JAX)':'#84329B',
            'Parker Davis (JAX)':'#84329B',
            'Peyton Charles (JAX)':'#84329B',
            'Riley Mertl (JAX)':'#84329B',
            'Roman Smith (JAX)':'#84329B',
            'Sam Poindexter (JAX)':'#84329B',
            'Tyler Lawrence (JAX)':'#84329B',
            'Tyler Macon (JAX)':'#84329B',
            'Tyler Smith (JAX)':'#84329B',
            'Wesley Mann (JAX)':'#84329B',
            'Will Ripoll (JAX)':'#84329B',
            'Will Schnepf (JAX)':'#84329B',
            'Addison Clymer (JNT)':'#3E342F',
            'Alex Mykut (JNT)':'#3E342F',
            'Austin Baal (JNT)':'#3E342F',
            'Brennan Murphy (JNT)':'#3E342F',
            'Bump Burgreen (JNT)':'#3E342F',
            'Caden Goodwin (JNT)':'#3E342F',
            'Cameron Goble (JNT)':'#3E342F',
            'Chris Hasse (JNT)':'#3E342F',
            'Cole Yeager (JNT)':'#3E342F',
            'Dan Merkel (JNT)':'#3E342F',
            'Daniel Morgano (JNT)':'#3E342F',
            'Dante DiMatteo (JNT)':'#3E342F',
            'Drake Dobson (JNT)':'#3E342F',
            'Forrest Havanis (JNT)':'#3E342F',
            'Gage Gillott (JNT)':'#3E342F',
            'Gannon Wentz (JNT)':'#3E342F',
            'Gio Calamia (JNT)':'#3E342F',
            'Jacob Kocuba (JNT)':'#3E342F',
            'Jake Roshau (JNT)':'#3E342F',
            'Kaden Kumzi (JNT)':'#3E342F',
            'Kayden Faulcon (JNT)':'#3E342F',
            'Koa Dabuet (JNT)':'#3E342F',
            'Manny Nager (JNT)':'#3E342F',
            'Mark Edeburn (JNT)':'#3E342F',
            'Matthew Benton (JNT)':'#3E342F',
            'Max Beaulieu (JNT)':'#3E342F',
            'Michael Klingensmith (JNT)':'#3E342F',
            'Miguel Vega (JNT)':'#3E342F',
            'Morgan Wyatt (JNT)':'#3E342F',
            'Nate Nolan (JNT)':'#3E342F',
            'Nick Guidas (JNT)':'#3E342F',
            'Nick Merriman (JNT)':'#3E342F',
            'Noah Czajkowski (JNT)':'#3E342F',
            'Phil Fox (JNT)':'#3E342F',
            'Scotty McManamon (JNT)':'#3E342F',
            'Tyler Horvat (JNT)':'#3E342F',
            'Tyler Quade (JNT)':'#3E342F',
            'Tyson Bryant-Dawson (JNT)':'#3E342F',
            'Aiden Hinds (LAF)':'#FFC82F',
            'Alek Elges (LAF)':'#FFC82F',
            'Alex Alberico (LAF)':'#FFC82F',
            'Brody Fine (LAF)':'#FFC82F',
            'Brooks Sailors (LAF)':'#FFC82F',
            'Caden Leonard (LAF)':'#FFC82F',
            'Caden Tarango (LAF)':'#FFC82F',
            'Caiden Bennett (LAF)':'#FFC82F',
            'Caleb Everson (LAF)':'#FFC82F',
            'Calvin Shepherd (LAF)':'#FFC82F',
            'Cayden Gothrup (LAF)':'#FFC82F',
            'Charles Lefebvre (LAF)':'#FFC82F',
            'Coley Stevens (LAF)':'#FFC82F',
            'Damien Wallace (LAF)':'#FFC82F',
            'Elliott Rossell (LAF)':'#FFC82F',
            'Foster McDonald (LAF)':'#FFC82F',
            'Graham Kollen (LAF)':'#FFC82F',
            'Jackson Burk (LAF)':'#FFC82F',
            'Jake Gothrup (LAF)':'#FFC82F',
            'Joe Olsavsky (LAF)':'#FFC82F',
            'Joey Humphrey (LAF)':'#FFC82F',
            'Joey Wilmoth (LAF)':'#FFC82F',
            'Kendall Anthes (LAF)':'#FFC82F',
            'Lawson Cole (LAF)':'#FFC82F',
            'Matt Lelito (LAF)':'#FFC82F',
            'Tyler Papenbrock (LAF)':'#FFC82F',
            'Wyatt Geesaman (LAF)':'#FFC82F',
            'Zach Zaborowski (LAF)':'#FFC82F',
            'AJ Rinebold (NOR)':'#2C5234',
            'Blake Roundtree Jr. (NOR)':'#2C5234',
            'Bode Gebbink (NOR)':'#2C5234',
            'Caleb Jacobs (NOR)':'#2C5234',
            'Case Sanderson (NOR)':'#2C5234',
            'Christian Badorek (NOR)':'#2C5234',
            'Drake Downing (NOR)':'#2C5234',
            'Drew Conn (NOR)':'#2C5234',
            'Easton Harris (NOR)':'#2C5234',
            'Gabe Helder (NOR)':'#2C5234',
            'Graham Kasey (NOR)':'#2C5234',
            'Hunter Pudio (NOR)':'#2C5234',
            'Jack Bach (NOR)':'#2C5234',
            'Jack Duncan (NOR)':'#2C5234',
            'Jake Perrino (NOR)':'#2C5234',
            'Joey Hagen (NOR)':'#2C5234',
            'Kayden Althoff (NOR)':'#2C5234',
            'Kyle Moore (NOR)':'#2C5234',
            'Max Jones (NOR)':'#2C5234',
            'Nash Mose (NOR)':'#2C5234',
            'Noah Leingang (NOR)':'#2C5234',
            'Parker Stoneking (NOR)':'#2C5234',
            'Payton Mansfield (NOR)':'#2C5234',
            'PJ Rogan (NOR)':'#2C5234',
            'Porter Conn (NOR)':'#2C5234',
            'Ryne Willard (NOR)':'#2C5234',
            'Scott Newman (NOR)':'#2C5234',
            'Trey Bryant (NOR)':'#2C5234',
            'Tyler Hensch (NOR)':'#2C5234',
            'Tyler Woltman (NOR)':'#2C5234',
            'Zach Courson (NOR)':'#2C5234',
            'Barrett Lohman (OFL)':'#010101',
            'Blake Bax (OFL)':'#010101',
            'Braden Barnard (OFL)':'#010101',
            'Caiden Otte (OFL)':'#010101',
            'Chase Becker (OFL)':'#010101',
            'Christian Harvey (OFL)':'#010101',
            'Coby Rogers (OFL)':'#010101',
            'Drew Politte (OFL)':'#010101',
            'Dylan Bates (OFL)':'#010101',
            'Eric Loomis (OFL)':'#010101',
            'Eric Steward (OFL)':'#010101',
            'Gavin Kinworthy (OFL)':'#010101',
            'Griffin King (OFL)':'#010101',
            'Hayden Wilson (OFL)':'#010101',
            'Ian Benner (OFL)':'#010101',
            'Jack DuMont (OFL)':'#010101',
            'Jack Jones (OFL)':'#010101',
            'Jake Vitale (OFL)':'#010101',
            'Kaden Joggerst (OFL)':'#010101',
            'Matt Haley (OFL)':'#010101',
            'Nathan Beaton (OFL)':'#010101',
            'Nick Harms (OFL)':'#010101',
            'Noah Arras (OFL)':'#010101',
            'Owen Schexnaydre (OFL)':'#010101',
            'Pierce Hartmann (OFL)':'#010101',
            'Samuel Feltz (OFL)':'#010101',
            'Stetson Marion (OFL)':'#010101',
            'Tanner Mueller (OFL)':'#010101',
            'Tucker Platt (OFL)':'#010101',
            'Victor Fujiu (OFL)':'#010101',
            'Zach Beatty (OFL)':'#010101',
            'Andrew Fay (QUI)':'#E4002B',
            'Anthony Ribes (QUI)':'#E4002B',
            'Braden Smith (QUI)':'#E4002B',
            'Brian Henke (QUI)':'#E4002B',
            'Carter Poole (QUI)':'#E4002B',
            'Cole Parkhill (QUI)':'#E4002B',
            'Connor Schwindeler (QUI)':'#E4002B',
            'Davin Meier (QUI)':'#E4002B',
            'Dawson Flowers (QUI)':'#E4002B',
            'Drew Evans (QUI)':'#E4002B',
            'Easton Mains (QUI)':'#E4002B',
            'Jake Schisler (QUI)':'#E4002B',
            'Jake Syverson (QUI)':'#E4002B',
            'Josh Hempelman (QUI)':'#E4002B',
            'Juan C Wu (QUI)':'#E4002B',
            'Luke Jessen (QUI)':'#E4002B',
            'Max Babich (QUI)':'#E4002B',
            'Noah Harbin (QUI)':'#E4002B',
            'Otto Jones (QUI)':'#E4002B',
            'Parker Mangelsen (QUI)':'#E4002B',
            'Peyton Clampitt (QUI)':'#E4002B',
            'Philip Reinhardt (QUI)':'#E4002B',
            'PJ Schmidt (QUI)':'#E4002B',
            'Rich Snider (QUI)':'#E4002B',
            'Riley Black (QUI)':'#E4002B',
            'Ryan Foley (QUI)':'#E4002B',
            'Samuel Skirvin (QUI)':'#E4002B',
            'Stefan Stockwell (QUI)':'#E4002B',
            'Stephen Eskridge (QUI)':'#E4002B',
            'Tanner Gerdes (QUI)':'#E4002B',
            'Tim Gooden (QUI)':'#E4002B',
            'Tyler Barker (QUI)':'#E4002B',
            'Tyler Dance (QUI)':'#E4002B',
            'AJ Golembiewski (SPR)':'#072B31',
            'Blake Donnan (SPR)':'#072B31',
            'Brant Smith (SPR)':'#072B31',
            'Brendan Strenke (SPR)':'#072B31',
            'Brody Logsdon (SPR)':'#072B31',
            'Bryan Jubelt (SPR)':'#072B31',
            'Bryce Stenzel (SPR)':'#072B31',
            'Chris Kustigian (SPR)':'#072B31',
            'Cody Ellis (SPR)':'#072B31',
            'Cole Smith (SPR)':'#072B31',
            'Connor McCaleb (SPR)':'#072B31',
            'Gavin Craggs (SPR)':'#072B31',
            'Grant Marshall (SPR)':'#072B31',
            'Hunter Moser (SPR)':'#072B31',
            'Isaiah Naylor (SPR)':'#072B31',
            'Jacob Hager (SPR)':'#072B31',
            'Jaden Mathon (SPR)':'#072B31',
            'Jase Daley (SPR)':'#072B31',
            'Jaylen Morgan (SPR)':'#072B31',
            'KJ Baker (SPR)':'#072B31',
            'Laine Axtetter (SPR)':'#072B31',
            'Logan Tabeling (SPR)':'#072B31',
            'Lucas Kresin (SPR)':'#072B31',
            'Matt Miscik (SPR)':'#072B31',
            'Matthew Cruise (SPR)':'#072B31',
            'Matthew Ulrici (SPR)':'#072B31',
            'Mike Sullivan (SPR)':'#072B31',
            'Mitch Dye (SPR)':'#072B31',
            'Nick Terrell (SPR)':'#072B31',
            'Nolan Self (SPR)':'#072B31',
            'Patrick Graham (SPR)':'#072B31',
            'Payton Matthews (SPR)':'#072B31',
            'Trent Koehler (SPR)':'#072B31',
            'Trey Carter (SPR)':'#072B31',
            'Ty Rhoades (SPR)':'#072B31',
            'Will Davidsmeier (SPR)':'#072B31',
            'Zane Danielson (SPR)':'#072B31',
            'Alex Marx (TER)':'#0057B7',
            'Blake Mincey (TER)':'#0057B7',
            'Blake Nigg (TER)':'#0057B7',
            'Brayden Lybarger (TER)':'#0057B7',
            'Bryce Martens (TER)':'#0057B7',
            'Cade Rusch (TER)':'#0057B7',
            'Caleb Hohman (TER)':'#0057B7',
            'Camden Karczewski (TER)':'#0057B7',
            'Carter Murphy (TER)':'#0057B7',
            'Casey Henry (TER)':'#0057B7',
            "CJ O'Dell (TER)":'#0057B7',
            'Clay Hendry (TER)':'#0057B7',
            'Clayton Weisheit (TER)':'#0057B7',
            'Connor Brady (TER)':'#0057B7',
            'Cory Wolter (TER)':'#0057B7',
            'Damon Cox (TER)':'#0057B7',
            'Dawson Smith (TER)':'#0057B7',
            'Derek Lebron (TER)':'#0057B7',
            'Diego Cardenas (TER)':'#0057B7',
            'Dominic Gill (TER)':'#0057B7',
            'Donnie Dycus (TER)':'#0057B7',
            'Eric Cunning (TER)':'#0057B7',
            'Evan Price (TER)':'#0057B7',
            'Greg Wiley (TER)':'#0057B7',
            'Jayson Cottrell (TER)':'#0057B7',
            'Jean Gonzalez (TER)':'#0057B7',
            'Jeremy Piatkiewicz (TER)':'#0057B7',
            'Jonathon Hanscom (TER)':'#0057B7',
            'Justin Bogard (TER)':'#0057B7',
            'Kaleb Marrs (TER)':'#0057B7',
            'Landon Carr (TER)':'#0057B7',
            'Morgan Colopy (TER)':'#0057B7',
            'Nathan Frady (TER)':'#0057B7',
            'Nazhir Bergen (TER)':'#0057B7',
            'Nolan Miller (TER)':'#0057B7',
            'Oscar Welsh (TER)':'#0057B7',
            'Payton Adkisson (TER)':'#0057B7',
            'Sam Pesa (TER)':'#0057B7',
            'Tanner Perry (TER)':'#0057B7',
            'Tripper Capps (TER)':'#0057B7',
            'Tyce Ochs (TER)':'#0057B7',
            'Warren Bailey (TER)':'#0057B7',
            'Xavier Croxton (TER)':'#0057B7',
            'Zacheus Carr (TER)':'#0057B7',
            'Austin Gast (THR)':'#FF8F1C',
            'Ben Eisenhauer (THR)':'#FF8F1C',
            'Ben Vaughn (THR)':'#FF8F1C',
            'Chase Austin (THR)':'#FF8F1C',
            'Eli Pillsbury (THR)':'#FF8F1C',
            'Ethan Ames (THR)':'#FF8F1C',
            'Hunter Ralls (THR)':'#FF8F1C',
            'Jackson Kranawetter (THR)':'#FF8F1C',
            'James Cravens (THR)':'#FF8F1C',
            'Kale Cameron (THR)':'#FF8F1C',
            'Kaleb Herbert (THR)':'#FF8F1C',
            'Karsten Stotlar (THR)':'#FF8F1C',
            'Levin East (THR)':'#FF8F1C',
            'Logan Mueller (THR)':'#FF8F1C',
            'Matthew Derrick (THR)':'#FF8F1C',
            'Michael Pfeiffer (THR)':'#FF8F1C',
            'Nathan Ball (THR)':'#FF8F1C',
            'Nick Oyster (THR)':'#FF8F1C',
            'Noah Willingham (THR)':'#FF8F1C',
            'Preston Drebes (THR)':'#FF8F1C',
            'Roman Harrison (THR)':'#FF8F1C',
            'Ryan Daly (THR)':'#FF8F1C',
            'Scott Wood (THR)':'#FF8F1C',
            'Shane Wilhelm (THR)':'#FF8F1C',
            'Tyler Yotkewich (THR)':'#FF8F1C',
            'Zach Haygood (THR)':'#FF8F1C',
        }
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

    return pitching_scatter_plot, pitching_figure1
