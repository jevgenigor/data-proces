# Ethereum Price Prediction Tool

This project analyzes real-time market data to predict the price direction of Ethereum over the next hour or day.

## Project Structure

- `data_collection/`: Contains scripts to fetch data from different APIs.
- `indicators/`: Contains scripts to calculate various financial indicators.
- `model/`: Contains scripts for training and predicting using machine learning models.
- `visualization/`: Contains scripts for visualizing the predictions and indicators.
- `main.py`: The main entry point to run the application.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd eth_price_prediction
   ```

2. Create a virtual environment (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script: