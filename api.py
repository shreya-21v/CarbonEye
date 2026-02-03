from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
from src.prediction_engine import process_vehicle_data, process_industry_data

app = FastAPI(title="CarbonEye API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VEHICLE_RESULTS = "data/vehicle_results.csv"
INDUSTRY_RESULTS = "data/industry_results.csv"


def _load_csv(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Run analysis to generate results.") from exc


@app.post("/run-analysis")
def run_analysis() -> dict:
    process_vehicle_data()
    process_industry_data()
    return {"status": "ok"}


@app.get("/vehicles")
def vehicles() -> list[dict]:
    data = _load_csv(VEHICLE_RESULTS)
    return data.to_dict(orient="records")


@app.get("/industries")
def industries() -> list[dict]:
    data = _load_csv(INDUSTRY_RESULTS)
    return data.to_dict(orient="records")


@app.get("/vehicles/top")
def top_vehicles(limit: int = 5) -> list[dict]:
    data = _load_csv(VEHICLE_RESULTS)
    top = data.sort_values(by="Predicted_CO2", ascending=False).head(limit)
    return top.to_dict(orient="records")


@app.get("/industries/top")
def top_industries(limit: int = 5) -> list[dict]:
    data = _load_csv(INDUSTRY_RESULTS)
    top = data.sort_values(by="Predicted_CO2", ascending=False).head(limit)
    return top.to_dict(orient="records")


@app.get("/vehicles/trend")
def vehicle_trend() -> list[dict]:
    data = _load_csv(VEHICLE_RESULTS)
    trend = data[["vehicle_no", "Predicted_CO2"]].copy()
    trend["Index"] = range(1, len(trend) + 1)
    return trend.to_dict(orient="records")


@app.get("/download/vehicles")
def download_vehicle_report() -> FileResponse:
    return FileResponse(VEHICLE_RESULTS, filename="vehicle_emission_report.csv")


@app.get("/download/industries")
def download_industry_report() -> FileResponse:
    return FileResponse(INDUSTRY_RESULTS, filename="industry_emission_report.csv")
