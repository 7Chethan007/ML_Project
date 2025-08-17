# Machine Learning Analysis Module

## Status
**Done**

## Description
Develop a logic-driven module to analyze financial data and categorize metrics into **Pros** (values > 10%) and **Cons** (values < 10%). The module will dynamically generate human-readable statements using context-aware templates (e.g., “Company is almost debt-free”).

## Objectives
- Classify financial metrics based on condition-based rules.
- Generate templated, context-aware explanations for each pro and con.
- Select and present the top 3 pros and cons for each company.
- Return results as a structured Python dictionary or object.

## Subtasks
1. **Rule-Based Classification**  
    - Implement logic to classify metrics as pros or cons based on value thresholds.

2. **Template Generation**  
    - Create reusable string templates for clear, human-readable explanations.

3. **Ranking and Selection**  
    - Identify and select the top 3 pros and cons per company.

4. **Structured Output**  
    - Format the results as a Python dictionary or object for downstream use.

---

**Example Output Structure:**

```python
{
     "company": "Example Corp",
     "pros": [
          "Company is almost debt-free.",
          "Revenue growth exceeds industry average.",
          "High return on equity."
     ],
     "cons": [
          "Operating margin below 10%.",
          "Low asset turnover ratio.",
          "Declining cash flow."
     ]
}
```