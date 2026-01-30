import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score

# Loading dataset
df = pd.read_csv('../data/industry_data.csv')

# Encoding categorical columns
le_type = LabelEncoder()
le_fuel = LabelEncoder()

df['Industry_Type'] = le_type.fit_transform(df['Industry_Type'])
df['Fuel_Used'] = le_fuel.fit_transform(df['Fuel_Used'])
df['Pollution_Control'] = df['Pollution_Control'].map({'Yes':1, 'No':0})

# Features and target
X = df.drop(columns=['Industry_Name', 'CO2_Emission'])
y = df['CO2_Emission']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Testing the accuracy
preds = model.predict(X_test)
score = r2_score(y_test, preds)
print(f"Model R2 Score: {score:.2f}")

# Saving the model
joblib.dump(model, '../models/industry_model.pkl')
print("✅ Industry emission model saved as industry_model.pkl")
