# Approved Changes

- **CR-102** (low): Add an index on tickets.created_at to speed up the nightly report query. — Adding a simple index on a single column for reporting purposes poses minimal risk to system stability.
- **CR-104** (low): Bump the Python base image from 3.11.8 to 3.11.9 in the agent container. — Minor patch version update for Python base image with no breaking changes expected.
- **CR-106** (low): Add a retry with exponential backoff to the webhook sender. — Adding retry logic with exponential backoff is a standard error handling improvement that enhances reliability without changing core functionality.
- **CR-108** (low): Increase the request timeout on the LLM gateway from 60s to 120s for long comple — Simple timeout configuration change that only extends maximum wait time for existing functionality.
