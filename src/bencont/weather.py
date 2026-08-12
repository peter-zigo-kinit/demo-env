"""Bratislava Weather Forecast Tool — Open-Meteo, location fixed."""

from __future__ import annotations

import httpx

# Bratislava city centre
LATITUDE = 48.1486
LONGITUDE = 17.1077
TIMEZONE = "Europe/Bratislava"


def fetch_bratislava_forecast() -> str:
    """Fetch today / next-24h conditions for Bratislava via Open-Meteo."""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "temperature_2m,precipitation_probability,wind_speed_10m",
        "forecast_hours": 24,
        "timezone": TIMEZONE,
    }
    with httpx.Client(timeout=30.0) as client:
        response = client.get("https://api.open-meteo.com/v1/forecast", params=params)
        response.raise_for_status()
        data = response.json()

    hourly = data["hourly"]
    times = hourly["time"]
    temps = hourly["temperature_2m"]
    precip = hourly["precipitation_probability"]
    wind = hourly["wind_speed_10m"]

    min_t = min(temps)
    max_t = max(temps)
    avg_precip = sum(precip) / len(precip) if precip else 0
    avg_wind = sum(wind) / len(wind) if wind else 0

    return (
        f"Bratislava forecast for the next 24 hours "
        f"(from {times[0]} to {times[-1]}, {TIMEZONE}): "
        f"temperature {min_t:.0f}–{max_t:.0f}°C, "
        f"avg precipitation probability ~{avg_precip:.0f}%, "
        f"avg wind ~{avg_wind:.0f} km/h."
    )
