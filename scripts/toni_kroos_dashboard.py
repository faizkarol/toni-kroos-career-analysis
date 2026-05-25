import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Data from the page
data = {
    "Season": ["2023/2024", "2022/2023", "2021/2022", "2020/2021", "2019/2020", "2018/2019", "2017/2018", "2016/2017", "2015/2016", "2014/2015"],
    "Apps": [33, 30, 28, 28, 35, 28, 27, 29, 32, 36],
    "Min": [2152, 2181, 2119, 2116, 2661, 2235, 2275, 2503, 2746, 3066],
    "G": [1, 2, 1, 3, 4, 0, 5, 3, 1, 2],
    "A": [8, 4, 3, 9, 5, 4, 7, 12, 10, 7],
    "Sh90": [1.46, 1.28, 1.95, 1.45, 1.93, 1.21, 1.62, 1.19, 0.66, 1.00],
    "KP90": [2.59, 2.23, 2.17, 2.81, 2.06, 2.54, 2.49, 2.88, 1.87, 2.08],
    "xG": [1.73, 1.20, 2.18, 2.31, 3.34, 1.41, 2.98, 1.74, 0.68, 2.06],
    "xA": [6.07, 4.94, 4.18, 7.47, 5.65, 4.18, 6.38, 8.08, 4.79, 4.55],
    "Completed Passes": [2000, 1900, 1850, 1800, 2100, 1950, 2000, 2050, 2200, 2300],
    "Attempted Passes": [2200, 2100, 2000, 1950, 2300, 2150, 2200, 2250, 2400, 2500]
}

df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Toni Kroos Performance Dashboard"),
    dcc.Dropdown(
        id='season-dropdown',
        options=[{'label': season, 'value': season} for season in df['Season']],
        value='2023/2024'
    ),
    dcc.Checklist(
        id='passes-toggle',
        options=[
            {'label': 'Show Passes', 'value': 'show_passes'}
        ],
        value=[]
    ),
    dcc.Graph(id='performance-chart'),
    html.Div(id='pass-percent-comment'),
    dcc.Graph(id='all-seasons-chart')
])

# Callback to update the chart based on the selected season and toggle
@app.callback(
    [Output('performance-chart', 'figure'), Output('pass-percent-comment', 'children'), Output('all-seasons-chart', 'figure')],
    [Input('season-dropdown', 'value'), Input('passes-toggle', 'value')]
)
def update_chart(selected_season, passes_toggle):
    filtered_df = df[df['Season'] == selected_season]
    y_columns = ['G', 'A', 'Sh90', 'KP90', 'xG', 'xA']
    pass_comment = ""
    if 'show_passes' in passes_toggle:
        y_columns.extend(['Completed Passes', 'Attempted Passes'])
        completed_passes = filtered_df['Completed Passes'].values[0]
        attempted_passes = filtered_df['Attempted Passes'].values[0]
        pass_percent = (completed_passes / attempted_passes) * 100
        pass_comment = f"Pass Completion Rate: {pass_percent:.2f}%"
    fig = px.bar(filtered_df, x='Season', y=y_columns, barmode='group')
    
    # Plot for all seasons
    all_seasons_y_columns = ['G', 'A', 'Sh90', 'KP90', 'xG', 'xA']
    if 'show_passes' in passes_toggle:
        all_seasons_y_columns.extend(['Completed Passes', 'Attempted Passes'])
        df['Pass Percentage'] = (df['Completed Passes'] / df['Attempted Passes']) * 100
        all_seasons_fig = px.line(df, x='Season', y=all_seasons_y_columns, markers=True)
        for i in range(len(df)):
            all_seasons_fig.add_annotation(x=df['Season'][i], y=df['Pass Percentage'][i], text=f"{df['Pass Percentage'][i]:.2f}%", showarrow=True, arrowhead=1)
    else:
        all_seasons_fig = px.line(df, x='Season', y=all_seasons_y_columns, markers=True)
    
    return fig, pass_comment, all_seasons_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
