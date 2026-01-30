import pandas as pd
import random

vehicle_types = ["Car", "Bike", "SUV", "Truck", "Bus"]
fuel_types = ["Petrol", "Diesel", "CNG"]

data = []

for i in range(200):  # Generates 200 vehicle records
    vehicle_no = f"TN{random.randint(10,99)}AB{random.randint(1000,9999)}"
    vehicle_type = random.choice(vehicle_types)
    fuel_type = random.choice(fuel_types)

    vehicle_age = random.randint(1, 12)
    engine_cc = random.choice([125, 150, 1000, 1200, 1500, 2000, 5000, 6000])
    mileage = random.uniform(5, 50)
    monthly_distance = random.randint(400, 3000)
    last_service_months = random.randint(1, 12)
    engine_condition = random.randint(4, 10)
    fuel_monthly = monthly_distance / mileage

    # Simple realistic CO2 formula (just for dataset generation)
    co2_emission = (
        engine_cc * 0.02 +
        vehicle_age * 2 +
        (50 - mileage) * 1.5 +
        fuel_monthly * 0.5
    )

    data.append([
        vehicle_no, vehicle_type, fuel_type, vehicle_age,
        engine_cc, round(mileage,2), monthly_distance,
        last_service_months, engine_condition,
        round(fuel_monthly,2), round(co2_emission,2)
    ])

columns = [
    "vehicle_no", "vehicle_type", "fuel_type", "vehicle_age",
    "engine_cc", "mileage", "monthly_distance",
    "last_service_months", "engine_condition",
    "fuel_monthly", "co2_emission"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("vehicle_data.csv", index=False)
print("✅ Vehicle dataset with 200 records created!")
