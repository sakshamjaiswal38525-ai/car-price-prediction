import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load dataset
data = pd.read_csv("car_data.csv")

# Features and target
X = data.drop("Selling_Price_Lakh", axis=1)
y = data["Selling_Price_Lakh"]

categorical = ["Brand", "Fuel_Type", "Transmission"]
numeric = ["Year", "Kilometers_Driven", "Owners", "Engine_CC", "Mileage_Kmpl"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ("num", "passthrough", numeric)
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Model trained successfully!")
print(f"R² Score: {r2:.2f}")
print(f"Mean Absolute Error: ₹{mae:.2f} lakh")

joblib.dump(model, "model.pkl")
print("model.pkl created successfully.")
