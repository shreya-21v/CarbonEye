import pandas as pd
import random

industry_types = ["Cement", "Steel", "Textile", "Power", "Chemical", "Food", "Paper"]
fuel_types = ["Coal", "Gas", "Oil", "Biomass", "Electricity"]

data = []

for i in range(200):  # 200 industry records
    industry_name = f"Industry_{i+1}"
    industry_type = random.choice(industry_types)
    fuel_used = random.choice(fuel_types)

    electricity_kwh = random.randint(5000, 200000)
    production_tons = random.randint(200, 6000)
    waste_tons = random.randint(5, 400)
    fuel_consumption = random.randint(50, 1000)
    operating_hours = random.randint(400, 750)
    machinery_age = random.randint(2, 25)
    pollution_control = random.choice(["Yes", "No"])

    # Simple realistic CO2 formula
    co2_emission = (
        electricity_kwh * 0.002 +
        fuel_consumption * 0.8 +
        machinery_age * 3 +
        waste_tons * 0.5
    )

    data.append([
        industry_name, industry_type, fuel_used, electricity_kwh,
        production_tons, waste_tons, fuel_consumption,
        operating_hours, machinery_age, pollution_control,
        round(co2_emission,2)
    ])

columns = [
    "Industry_Name", "Industry_Type", "Fuel_Used", "Electricity_kWh",
    "Production_Tons", "Waste_Tons", "Fuel_Consumption",
    "Operating_Hours", "Machinery_Age", "Pollution_Control",
    "CO2_Emission"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("industry_data.csv", index=False)
print("✅ Industry dataset with 200 records created!")
