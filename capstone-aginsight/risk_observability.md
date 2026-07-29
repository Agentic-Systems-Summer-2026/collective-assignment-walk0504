# Risk and Observability

AgInsight is designed to monitor weather and commodity information that farmers may use when making decisions. Because inaccurate information could lead to poor decisions, the system includes safeguards that reduce risk and make its behavior easier to understand.

Rather than assuming every generated alert is correct, AgInsight validates each statement against the original source data before approving the final alert. Every monitoring cycle is also recorded in an observability log so that the system's decisions can be reviewed later.

## System Risks

The current prototype has several known risks:

- Live weather or commodity APIs may become unavailable.
- Live data may be delayed or temporarily inaccurate.
- Threshold-based alerts may not cover every real-world farming situation.
- Network failures could prevent new data from being collected.
- Users could misunderstand an alert if they do not review the supporting information.

AgInsight reduces these risks by using fallback data, validating every alert against the original source information, limiting corrections to one rewrite, and recording every monitoring cycle in a log.

## Observability

Every monitoring cycle is recorded in the observability log. This makes it possible to review how AgInsight reached its final decision and troubleshoot unexpected behavior.

Each log entry includes:

- Timestamp
- Weather data
- Commodity data
- Generated alert
- Grounding validation results
- Any correction that was made
- Final approved alert
- Overall monitoring status

The observability log is saved in:

```text
capstone-aginsight/logs/alerts.jsonl
```

## Future Improvements

This prototype demonstrates the core monitoring, validation, and observability workflow, but additional improvements would be needed before production deployment.

Future work could include:

- Monitoring multiple farms at the same time.
- Sending alerts by text message or email.
- Adding additional commodity markets.
- Storing historical monitoring data in a database.
- Expanding the evaluation suite with live integration tests.
- Adding user authentication and role-based access controls.