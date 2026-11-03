# Car Price Prediction - Beginner ML Project

## Files

- `car_data.csv` - sample training dataset
- `train_model.py` - trains the machine learning model
- `model.pkl` - saved model (created after training)
- `app.py` - simple desktop GUI for prediction
- `requirements.txt` - Python libraries
- `car_price_prediction.ipynb` - optional notebook showing the basic workflow

## How to run on Windows PC

### 1. Install Python
Install Python 3.10+ from the official Python website:
https://www.python.org/downloads/

During installation, tick **Add Python to PATH**.

### 2. Open the project folder
Open the `Car_Price_Prediction` folder.

Click the address bar in File Explorer, type:
`cmd`
and press Enter.

### 3. Install libraries

Run:

`pip install -r requirements.txt`

If `pip` does not work, try:

`python -m pip install -r requirements.txt`

### 4. Train the model

Run:

`python train_model.py`

You should see:
- Model trained successfully
- R² Score
- Mean Absolute Error
- model.pkl created successfully

### 5. Run the application

Run:

`python app.py`

A Car Price Prediction window will open.

Enter the car details and click **Predict Price**.

## Important
This project includes a small demonstration dataset created for learning. The predicted prices are examples for a college/project demonstration, not real market valuations.

## Optional Jupyter Notebook

Install Jupyter:

`pip install notebook`

Then run:

`jupyter notebook`

Open `car_price_prediction.ipynb`.
