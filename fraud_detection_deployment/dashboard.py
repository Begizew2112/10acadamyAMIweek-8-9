# Import necessary modules
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load the fraud data CSV file
fraud_data = pd.read_csv(r'C:\Users\Yibabe\Desktop\10acadamyAMIweek-8-9\data\cleaned_fraud_Data.csv')  # Adjust the path to your CSV file

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
        'fraud_cases': int(fraud_cases),  # Convert to int for JSON compatibility
        'fraud_percentage': fraud_percentage
    })

# Time trend data endpoint
@app.route('/api/trends', methods=['GET'])
def trends():
    # Aggregate fraud cases over time (by day in this case)
    fraud_trend = fraud_data.resample('D', on='purchase_time')['class'].sum().reset_index()
    fraud_trend = fraud_trend.rename(columns={'purchase_time': 'date', 'class': 'fraud_cases'}).to_dict(orient='records')
    
    return jsonify({'fraud_trend': fraud_trend})

if __name__ == '__main__':
    app.run(debug=True)
