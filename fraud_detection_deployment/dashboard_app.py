from flask import Flask, jsonify
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import requests

# Initialize Flask app
app = Flask(__name__)

# Load the fraud data CSV file
fraud_data = pd.read_csv(r'C:\Users\Yibabe\Desktop\10acadamyAMIweek-8-9\data\cleaned_fraud_Data.csv')

# Ensure 'purchase_time' is in datetime format for trend analysis
fraud_data['purchase_time'] = pd.to_datetime(fraud_data['purchase_time'])

# Summary statistics endpoint
@app.route('/api/summary', methods=['GET'])
def summary_stats():
    total_transactions = len(fraud_data)
    fraud_cases = fraud_data['class'].sum()  # Using 'class' as the fraud indicator column
    fraud_percentage = (fraud_cases / total_transactions) * 100

    return jsonify({
        'total_transactions': total_transactions,
        'fraud_cases': int(fraud_cases),
        'fraud_percentage': fraud_percentage
    })

# Time trend data endpoint
@app.route('/api/trends', methods=['GET'])
def trends():
    # Aggregate fraud cases over time (by day in this case)
    fraud_trend = fraud_data.resample('D', on='purchase_time')['class'].sum().reset_index()
    fraud_trend = fraud_trend.rename(columns={'purchase_time': 'date', 'class': 'fraud_cases'}).to_dict(orient='records')
    
    return jsonify({'fraud_trend': fraud_trend})

# Create Dash app and attach it to the Flask app
dash_app = Dash(__name__, server=app, url_base_pathname='/my_dash/')

# Layout for the Dash app
dash_app.layout = html.Div([
    html.H1("Fraud Detection Dashboard"),
    html.Div(id='summary-box'),
    dcc.Graph(id='fraud-trend-chart'),
])

@dash_app.callback(
    [Output('summary-box', 'children'),
     Output('fraud-trend-chart', 'figure')],
    Input('interval-component', 'n_intervals')  # Replace with appropriate input if needed
)
def update_dashboard(n):
    summary = requests.get("http://127.0.0.1:5000/api/summary").json()
    trend_data = requests.get("http://127.0.0.1:5000/api/trends").json()

    # Create summary display
    summary_box = html.Div([
        html.P(f"Total Transactions: {summary['total_transactions']}"),
        html.P(f"Fraud Cases: {summary['fraud_cases']}"),
        html.P(f"Fraud Percentage: {summary['fraud_percentage']:.2f}%")
    ])

    # Create line chart
    trend_df = pd.DataFrame(trend_data['fraud_trend'])
    fig = px.line(trend_df, x='date', y='fraud_cases', title="Fraud Cases Over Time")

    return summary_box, fig

if __name__ == '__main__':
    app.run(debug=True)
