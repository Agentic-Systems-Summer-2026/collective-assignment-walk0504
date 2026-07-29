# AgInsight

AgInsight is an agentic AI farm monitoring prototype designed to help farmers monitor important weather conditions and commodity information. The system collects live data, generates alerts, validates each alert against the original source data, and only approves alerts that are supported.

The current prototype monitors weather conditions for Weatherford, Oklahoma, and wheat commodity pricing. It demonstrates a complete end-to-end monitoring cycle that includes live data collection, fallback behavior, grounding validation, one correction attempt, observability logging, and repeatable evaluation.

## Project Purpose

Farmers often make time-sensitive decisions based on weather and market information. Incorrect alerts could lead to unnecessary costs or poor operational decisions. AgInsight was designed to improve trust by checking every alert statement before it is approved.

## Key Features

- Retrieves live weather data for Weatherford, Oklahoma.
- Retrieves live wheat commodity pricing.
- Uses labeled fallback data if an external service is unavailable.
- Generates alerts using defined weather thresholds.
- Validates every alert statement against the original source data.
- Performs one correction attempt to remove unsupported statements.
- Records every monitoring cycle in an observability log.
- Includes a repeatable evaluation harness with eight predefined test cases.

## System Workflow

Each monitoring cycle follows the same sequence:

1. Retrieve live weather data.
2. Retrieve live wheat commodity pricing.
3. Use fallback data if an API is unavailable.
4. Compare the data to predefined alert thresholds.
5. Generate weather and commodity alerts.
6. Validate every alert statement against the original source data.
7. Remove unsupported statements during one correction attempt.
8. Run a final grounding validation.
9. Approve or hold the alert.
10. Save the monitoring cycle to the observability log.

## Grounding Validation

AgInsight validates every alert statement before it is approved. Each statement is compared against the original weather or commodity data used to generate the alert.

The system checks:

- Extreme heat alerts only if the temperature is at least 100°F.
- Heat advisory alerts only if the temperature is between 95°F and 99°F.
- High wind alerts only if wind speed is at least 20 mph.
- Heavy rain alerts only if rain probability is at least 70%.
- Wheat price statements only if the reported price exactly matches the formatted source value.

If a statement cannot be supported by the original data, it is removed during one correction attempt. The alert is then checked a second time before being approved or held.

## Requirements

To run AgInsight, you will need:

- Python 3
- Internet access for live API requests
- The `requests` Python package
- An Alpha Vantage API key for live commodity pricing

## Install Dependencies

From the repository root, install the required package:

```bash
pip install -r capstone-aginsight/requirements.txt
```

## Run AgInsight

From the repository root, run:

```bash
python3 capstone-aginsight/main.py
```

When the program runs, it:

- Retrieves live weather data.
- Retrieves live wheat commodity data (or fallback data if needed).
- Generates alerts based on the current conditions.
- Validates every alert against the original data.
- Saves the monitoring results to the observability log.

## Output

Each monitoring cycle is saved to the following log file:

```text
capstone-aginsight/logs/alerts.jsonl
```

The log includes:

- Weather data
- Commodity data
- Generated alerts
- Grounding validation results
- Correction attempts
- Final approval status
- Timestamp for each monitoring cycle

## Evaluation

AgInsight includes a repeatable evaluation harness with eight predefined test cases. These cases use fixed weather and commodity inputs so the results are consistent and do not depend on changing live API data.

From the repository root, run:

```bash
python3 bc4-evals/harness.py
```

The evaluation checks whether AgInsight:

- Generates the correct alerts for each test condition.
- Includes the correct wheat price.
- Avoids unsupported statements.
- Handles exact alert threshold boundaries.
- Produces the required output structure.

The current evaluation result is:

- 8 out of 8 test cases passed.
- 100% pass rate.
- Required minimum threshold: 80%.