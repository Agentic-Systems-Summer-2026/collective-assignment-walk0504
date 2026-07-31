# Evaluation Results

The AgInsight prototype was evaluated using multiple weather scenarios to verify that the alert generation and grounding workflow behaved correctly under different conditions.

| Scenario | Description | Result |
|----------|-------------|--------|
| Scenario 1 | Extreme heat, high wind, low rain chance | PASS |
| Scenario 2 | Moderate temperature, high rain chance, low wind | PASS |

## Scenario 1

**Input**

- Temperature: 101°F
- Rain Chance: 15%
- Wind Speed: 22 mph

**Observed Behavior**

- Heat alert generated.
- High wind alert generated.
- Wheat price reported correctly.
- Heavy rain statement failed the grounding check because the rain chance was only 15%.
- The unsupported statement was removed during the rewrite.
- The corrected alert passed the second grounding check.

## Scenario 2

**Input**

- Temperature: 85°F
- Rain Chance: 80%
- Wind Speed: 10 mph

**Observed Behavior**

- No heat alert was generated because the temperature was below the threshold.
- No wind alert was generated because wind speed was below the threshold.
- Heavy rain statement passed the grounding check because the rain chance was high.
- Wheat price was reported correctly.
- The final alert was approved without removing any statements.

## Evaluation Summary

These early evaluation scenarios confirmed that AgInsight responded correctly to different weather conditions and that the grounding validation removed unsupported statements before alerts were approved. As the project developed, the evaluation process expanded into repeatable eight-case evaluation harness with defined metrics and automated regression testing. This final demo also integrates the OU LiteLLM Sandbox to generate a farmer-friendly summary only after the alert has passed grounding validation. This keeps the LLM from introducing unsupported information while still providing a readable summary for the user. 

## Build 4 Evaluation

I built an evaluation harness for AgInsight that tests the main parts of the system using fixed weather and commodity data. The harness checks whether AgInsight creates the correct alerts, avoids unsupported alerts, includes the correct wheat price, returns the right approval status, and follows the expected JSON format.

I created eight evaluation cases. The cases covered normal conditions, heat, extreme heat, high wind, heavy rain, multiple weather risks at once, exact threshold boundaries, and output formatting.

The final local sweep passed 8 out of 8 cases for a 100% pass rate. The required threshold was 80%.

## Metrics

- Total cases: 8
- Passed cases: 8
- Failed cases: 0
- Final pass rate: 100%
- Required threshold: 80%
- CI live sweep size: 5 cases
- Green GitHub Actions run: Passed
- Deliberately broken GitHub Actions run: Failed as expected
- Demo runs against: OU LiteLLM Sandbox (Qwen3 Coder 30B)

## Judge Calibration

I first ran the LLM judge on all eight cases and got a 75% pass rate. I reviewed the two failures by hand.

The heat case was actually correct, but the judge expected the output to clearly explain that 97 degrees was not extreme heat. That explanation was not required because the system already avoided creating an extreme heat alert.

The wind case was also correct, but the judge treated the wheat price as unrelated information. AgInsight is designed to include the wheat price in every monitoring cycle, so the judge criteria did not match the actual system design.

I updated the judge criteria to better match my own human labels. After calibration, the judge agreed with my labels on all eight cases, and the final pass rate increased to 100%.

## Error Analysis

The most important lesson from the failed cases was that an LLM judge can be wrong even when the system output is correct. The original judge criteria were too vague and allowed the judge to add requirements that were not part of AgInsight.

The heat output correctly included a heat advisory at 97 degrees and did not include an extreme heat alert. The judge still failed it because it wanted an extra explanation. The wind output correctly included a high wind advisory, but the judge failed it because it did not understand that the wheat price is always included by design.

These failures showed me that judge criteria need to be specific and tied directly to the system requirements. I changed the criteria so the judge checked only the expected alerts, the correct values, and the absence of unsupported alerts.

Another limitation is that the evaluation uses fixed test data. This makes the tests repeatable, but it does not fully test problems caused by live APIs, outdated source data, or temporary service failures. Those issues would need separate integration tests.

## CI Regression Gate

I connected the evaluation harness to GitHub Actions. The workflow runs on every push and tests the first five cases. The build fails if the pass rate drops below 80%.

I first pushed the working version and confirmed that the GitHub Actions run passed. I then deliberately changed the pass threshold to 110%, which caused the run to fail. This proved that the regression gate can catch a broken threshold or regression. I then restored the threshold to 80% and pushed again so the repository ended in a passing state.

## AI Delegation Log

I used ChatGPT as a development assistant throughout this project. It helped me understand the starter harness, troubleshoot Python and GitHub Action issues, explain concepts I was unfamiliar with, brainstorm evaluation cases, and integrate the shared OU LiteLLM Sandbox client into the final demo. I used its suggestions as a starting point, then modified, tested, and verified the code until it worked correctly with my AgInsight project. 

The main prompts I used focused on understanding the evaluation harness, creating AgInsight-specific test cases, interpreting failed judge results, integrating the shared OU LiteLLM Sandbox client, improving the final demo, and resolving isses such as the missing requests package in GitHub Actions. 

The AI was not correct every time. Some early instructions changed more of my capstone than necessary, and the first judge criteria caused two correct outputs to fail. I reviewed the code, checked the outputs myself, corrected the judge criteria, and reran the evaluation until the results matched my own labels.

I verified the final result by running the full local sweep, reviewing `last_run.json`, checking that all eight cases passed, confirming the green GitHub Actions run, creating a deliberate broken run, and restoring the repository to a passing state.

## Future Evaluation Improvements

The current evaluation suite focuses on representative scenarios that verify AgInsight's primary workflow. As the project continues to develop, the evaluation suite will be expanded to provide broader coverage and stronger confidence in system behavior.

Planned improvements include:

- Adding intentionally failing test cases to verify that the calibrated LLM judge is not overly permissive.
- Expanding the evaluation suite beyond the current representative scenarios to include additional weather patterns, commodity market conditions, and API edge cases.
- Adding refusal and malformed input cases, including missing weather fields, corrupted API responses, invalid numeric values, and conflicting data between sources.
- Creating more agent-focused failure cases that verify AgInsight correctly rejects unsupported alerts, prevents hallucinated recommendations, and safely handles simultaneous failures across multiple data sources.