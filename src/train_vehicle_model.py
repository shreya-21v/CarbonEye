import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score

# Loading dataset
df = pd.read_csv('../data/vehicle_data.csv')

# Encoding categorical features
le_fuel = LabelEncoder()
le_type = LabelEncoder()

df['fuel_type'] = le_fuel.fit_transform(df['fuel_type'])
df['vehicle_type'] = le_type.fit_transform(df['vehicle_type'])

# Define features and target
X = df.drop(columns=['vehicle_no', 'co2_emission'])
y = df['co2_emission']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Testing the accuracy
preds = model.predict(X_test)
score = r2_score(y_test, preds)
print(f"Model R2 Score: {score:.2f}")

# Saving the model
joblib.dump(model, '../models/vehicle_model.pkl')
print("✅ Vehicle emission model saved as vehicle_model.pkl")
