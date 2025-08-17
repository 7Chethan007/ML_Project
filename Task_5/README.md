# Task: Terminal Output & Real-time Logging

**Status:** Pending

## Description

Design a real-time command-line interface (CLI) that prints analysis results as the script processes each company. Use color coding (green for pros, red for cons) for better readability and display progress counters.

---

## Subtasks

- Show company name + ID being processed.
- Display top pros and cons.
- Print errors in red, successes in green.
- Log to both console and file (e.g., `log.txt`).

---

## Example Output

```plaintext
Processing: Acme Corp (ID: 12345)
    Pros:
        - Great work-life balance   [green]
        - Competitive salary        [green]
    Cons:
        - Long commute             [red]
        - Outdated technology      [red]
Progress: 3/10 companies processed

[Success] Analysis completed for Acme Corp (ID: 12345)   [green]
[Error] Failed to process Beta Inc (ID: 67890)           [red]
```

---

## Logging

- All output should be visible in the terminal (with colors).
- All messages should also be saved to a log file (`log.txt`) without color codes.
- Include timestamps for each log entry.