import joblib
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the trained model (update the path to your model)
model = joblib.load('C:/Users/Yibabe/Desktop/10acadamyAMIweek-8-9/notebook/decision_tree_fraud_model.pkl')

@app.route('/')
def home():
    return "Welcome to the Fraud Detection API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json  # Get data from the request
        required_fields = ["purchase_value", "age", "ip_int", "transaction_count_per_day", "time_diff", "hour_of_day", "day_of_week", "source_Direct", "source_SEO", "browser_FireFox", "browser_IE", "browser_Opera", "browser_Safari", "sex_M"]
        
        # Validate input data
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields in the input data.'}), 400
        
        # Format the input correctly as a list
        input_data = [
            data["purchase_value"],
            data["age"],
            data["ip_int"],
            data["transaction_count_per_day"],
            data["time_diff"],
            data["hour_of_day"],
            data["day_of_week"],
            data["source_Direct"],
            data["source_SEO"],
            data["browser_FireFox"],
            data["browser_IE"],
            data["browser_Opera"],
            data["browser_Safari"],
            data["sex_M"]
        ]
        
        # Make a prediction using the model
        prediction = model.predict([input_data])
        
        # Log the received data and the prediction
        logging.info(f"Received data: {data}")
        logging.info(f"Prediction: {prediction.tolist()}")
        
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
