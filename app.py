from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

DATA_PATH = Path(__file__).resolve().parent / 'data' / 'spacex_launch_dash.csv'
df = pd.read_csv(DATA_PATH)
SITE = 'Launch Site'
PAYLOAD = 'Payload Mass (kg)'
BOOSTER = 'Booster Version Category'


def filtered(site, payload_range):
    rows = df[df[PAYLOAD].between(*payload_range)]
    return rows if site == 'ALL' else rows[rows[SITE] == site]


def figures(site, payload_range):
    rows = filtered(site, payload_range)
    if site == 'ALL':
        counts = rows.groupby(SITE, as_index=False)['class'].sum()
        pie = px.pie(counts, names=SITE, values='class', title='Successful landings by site')
    else:
        counts = rows.groupby('class').size().rename('Launches').reset_index()
        counts['Outcome'] = counts['class'].map({0: 'Unsuccessful', 1: 'Successful'})
        pie = px.pie(counts, names='Outcome', values='Launches', title=f'Landing outcomes: {site}')
    scatter = px.scatter(rows, x=PAYLOAD, y='class', color=BOOSTER,
                         title='Payload and landing outcome', hover_data=[SITE])
    scatter.update_yaxes(tickvals=[0, 1], ticktext=['Unsuccessful', 'Successful'])
    return pie, scatter


app = Dash(__name__)
app.layout = html.Div([
    html.H1('SpaceX Falcon 9 Landing Analysis'),
    html.P('Historical IBM course data. Filters apply to both charts. No operational forecasts.'),
    dcc.Dropdown(id='site', options=[{'label': 'All sites', 'value': 'ALL'}] +
                 [{'label': s, 'value': s} for s in sorted(df[SITE].unique())], value='ALL', clearable=False),
    html.Label('Payload mass (kg)'),
    dcc.RangeSlider(id='payload', min=0, max=10000, step=100, value=[0, 10000],
                    marks={i: str(i) for i in range(0, 10001, 2000)}),
    dcc.Graph(id='pie'), dcc.Graph(id='scatter'),
], style={'maxWidth': '1100px', 'margin': 'auto', 'fontFamily': 'Arial'})


@app.callback(Output('pie', 'figure'), Output('scatter', 'figure'),
              Input('site', 'value'), Input('payload', 'value'))
def update(site, payload_range):
    return figures(site, payload_range)


if __name__ == '__main__':
    app.run(debug=False)
