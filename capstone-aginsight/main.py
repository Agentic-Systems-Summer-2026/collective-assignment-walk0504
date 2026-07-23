import json
import os
from datetime import datetime
from pathlib import Path

import requests


# ---------------------------------------------------------
# 1. LIVE WEATHER DATA WITH FALLBACK
# ---------------------------------------------------------

def get_live_weather():
    """
    Retrieves current weather for Weatherford, Oklahoma.

    If the weather API is unavailable, the workflow continues
    using clearly defined fallback data.
    """

    latitude = 35.5262
    longitude = -98.7076

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,wind_speed_10m"
        "&daily=precipitation_probability_max"
        "&temperature_unit=fahrenheit"
        "&wind_speed_unit=mph"
        "&timezone=auto"
        "&forecast_days=1"
    )

    fallback_weather = {
        "temperature_f": 96,
        "rain_chance_percent": 15,
        "wind_speed_mph": 13,
        "data_source": "fallback"
    }

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        current = data["current"]
        daily = data["daily"]

        return {
            "temperature_f": round(current["temperature_2m"]),
            "rain_chance_percent": round(
                daily["precipitation_probability_max"][0]
            ),
            "wind_speed_mph": round(current["wind_speed_10m"]),
            "data_source": "Open-Meteo API"
        }

    except requests.RequestException as error:
        print(f"Weather API unavailable: {error}")
        print("Using fallback weather data so the workflow can continue.")

        return fallback_weather

def get_live_commodity_prices():
    """
    Retrieves the latest available global wheat and corn observations
    from Alpha Vantage.

    If the API is unavailable or the key is missing, the workflow
    continues using clearly labeled fallback values.
    """

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    fallback_commodities = {
        "wheat_price": 5.72,
        "corn_price": 4.18,
        "wheat_date": "fallback",
        "corn_date": "fallback",
        "data_source": "fallback sample data"
    }

    if not api_key:
        print("Alpha Vantage API key is missing.")
        print("Using fallback commodity data so the workflow can continue.")
        return fallback_commodities

    def fetch_latest(function_name):
        url = "https://www.alphavantage.co/query"

        params = {
            "function": function_name,
            "interval": "monthly",
            "apikey": api_key
        }

        response = requests.get(
            url,
            params=params,
            timeout=30
        )
        response.raise_for_status()

        payload = response.json()

        if "Note" in payload:
            raise RuntimeError(payload["Note"])

        if "Information" in payload:
            raise RuntimeError(payload["Information"])

        if "Error Message" in payload:
            raise RuntimeError(payload["Error Message"])

        observations = payload.get("data", [])

        for observation in observations:
            value = observation.get("value")

            if value not in (None, "."):
                return {
                    "value": float(value),
                    "date": observation.get("date", "unknown")
                }

        raise ValueError(
            f"No usable observations returned for {function_name}."
        )

    try:
        wheat = fetch_latest("WHEAT")
        corn = fetch_latest("CORN")

        return {
            "wheat_price": wheat["value"],
            "corn_price": corn["value"],
            "wheat_date": wheat["date"],
            "corn_date": corn["date"],
            "data_source": "Alpha Vantage global commodity data"
        }

    except (
        requests.RequestException,
        RuntimeError,
        ValueError,
        KeyError,
        TypeError
    ) as error:
        print(f"Commodity API unavailable: {error}")
        print("Using fallback commodity data so the workflow can continue.")
        return fallback_commodities

weather_data = get_live_weather()
commodity_data = get_live_commodity_prices()

# ---------------------------------------------------------
# 2. GENERATE AN INITIAL ALERT
# ---------------------------------------------------------

def generate_alert(weather, commodities):
    """
    Creates an alert dynamically from weather and commodity data.
    """

    statements = []

    if weather["temperature_f"] >= 100:
        statements.append(
            f"Extreme heat alert: the current temperature is "
            f"{weather['temperature_f']} degrees Fahrenheit."
        )

    elif weather["temperature_f"] >= 95:
        statements.append(
            f"Heat advisory: the current temperature is "
            f"{weather['temperature_f']} degrees Fahrenheit."
        )

    if weather["wind_speed_mph"] >= 20:
        statements.append(
            f"High wind advisory: wind speed is "
            f"{weather['wind_speed_mph']} miles per hour."
        )

    if weather["rain_chance_percent"] >= 70:
        statements.append(
            f"Heavy rain may affect field work. The current rain "
            f"chance is {weather['rain_chance_percent']} percent."
        )

    statements.append(
        f"The latest available wheat price is "
        f"${commodities['wheat_price']:.2f} per bushel."
    )

    return statements


# ---------------------------------------------------------
# 3. GROUNDING CHECK
# ---------------------------------------------------------

def check_statement(statement, weather, commodities):
    """
    Checks whether an alert statement is supported by source data.
    """

    lower_statement = statement.lower()

    if "extreme heat" in lower_statement:
        passed = weather["temperature_f"] >= 100
        return passed, "high" if passed else "low"

    if "heat advisory" in lower_statement:
        passed = 95 <= weather["temperature_f"] < 100
        return passed, "high" if passed else "low"

    if "high wind" in lower_statement:
        passed = weather["wind_speed_mph"] >= 20
        return passed, "high" if passed else "low"

    if "heavy rain" in lower_statement:
        passed = weather["rain_chance_percent"] >= 70
        return passed, "high" if passed else "low"

    if "wheat price" in lower_statement:
        expected_price = f"{commodities['wheat_price']:.2f}"
        passed = expected_price in statement
        return passed, "high" if passed else "low"

    return False, "low"


def run_grounding_check(statements, weather, commodities):
    """
    Checks every alert statement and records the result.
    """

    checked_statements = []

    for statement in statements:
        passed, confidence = check_statement(
            statement,
            weather,
            commodities
        )

        checked_statements.append({
            "statement": statement,
            "passed": passed,
            "confidence": confidence
        })

    return checked_statements


# ---------------------------------------------------------
# 4. CORRECT THE ALERT ONCE
# ---------------------------------------------------------

def rewrite_alert(checked_statements):
    """
    Keeps supported statements and removes unsupported statements.
    Only one correction step is allowed.
    """

    corrected_statements = []

    for result in checked_statements:
        if result["passed"]:
            corrected_statements.append(result["statement"])

    return corrected_statements


# ---------------------------------------------------------
# 5. SAVE AN OBSERVABILITY LOG
# ---------------------------------------------------------

def save_log(
    initial_alert,
    first_check,
    final_alert,
    final_check,
    rewrite_attempted
):
    """
    Records the entire workflow for later review.
    """

    Path("logs").mkdir(exist_ok=True)

    final_status = (
        "approved"
        if final_check and all(item["passed"] for item in final_check)
        else "held"
    )

    record = {
        "timestamp": datetime.now().isoformat(),
        "source_data": {
            "weather": weather_data,
            "commodities": commodity_data
        },
        "initial_alert": initial_alert,
        "first_grounding_check": first_check,
        "rewrite_attempted": rewrite_attempted,
        "final_alert": final_alert,
        "final_grounding_check": final_check,
        "final_status": final_status
    }

    with open("logs/alerts.jsonl", "a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(record) + "\n")


# ---------------------------------------------------------
# 6. RUN THE COMPLETE WORKFLOW
# ---------------------------------------------------------

def main():
    print("=" * 60)
    print("AGINSIGHT: TRUSTWORTHY FARM MONITORING AGENT")
    print("=" * 60)

    print("\nMONITORING CYCLE STARTED")

    print("\nSOURCE DATA")
    print("Weather:", weather_data)
    print("Commodity prices:", commodity_data)

    initial_alert = generate_alert(
        weather_data,
        commodity_data
    )

    print("\nINITIAL ALERT")
    for statement in initial_alert:
        print("-", statement)

    first_check = run_grounding_check(
        initial_alert,
        weather_data,
        commodity_data
    )

    print("\nFIRST GROUNDING CHECK")
    for result in first_check:
        status = "PASS" if result["passed"] else "FAIL"
        print(
            f"{status}: {result['statement']} "
            f"[Confidence: {result['confidence']}]"
        )

    rewrite_needed = any(
        not item["passed"] for item in first_check
    )

    if rewrite_needed:
        final_alert = rewrite_alert(first_check)

        final_check = run_grounding_check(
            final_alert,
            weather_data,
            commodity_data
        )

        print("\nFINAL ALERT AFTER ONE CORRECTION")

    else:
        final_alert = initial_alert
        final_check = first_check

        print("\nFINAL APPROVED ALERT")

    for statement in final_alert:
        print("-", statement)

    final_status = (
        "APPROVED"
        if final_check and all(item["passed"] for item in final_check)
        else "HELD"
    )

    print(f"\nFINAL STATUS: {final_status}")

    save_log(
        initial_alert,
        first_check,
        final_alert,
        final_check,
        rewrite_needed
    )

    print("\nObservability record saved to logs/alerts.jsonl")
    print("MONITORING CYCLE COMPLETE")


if __name__ == "__main__":
    main()