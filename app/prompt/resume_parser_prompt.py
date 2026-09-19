def parser_prompt(resume_input: str) -> str:
    return f"""
You are an intelligent resume parsing agent.

Your task is to extract structured information from the raw resume text provided below and return the output strictly in VALID JSON format.

## CRITICAL RULES (MANDATORY)

1. Output ONLY valid JSON. Do NOT include:
   - Explanations
   - Notes
   - Comments
   - Markdown
   - Code fences

2. The JSON must be:
   - Properly formatted
   - Parsable
   - Without trailing commas
   - Using double quotes only

3. The structure MUST EXACTLY match the schema provided.
   - Do NOT add fields.
   - Do NOT remove fields.
   - Do NOT rename fields.

4. Missing data handling:
   - Use null for missing single values.
   - Use [] for missing arrays.
   - Use 0 for unknown numeric fields.

5. Date format:
   - Use "YYYY-MM".
   - If only a year is available, use "YYYY-01".
   - For a current/ongoing role, set end_date to null unless the resume explicitly uses a value such as "Present" or "Ongoing". In that case, preserve the exact text in end_date.

6. Duration calculation:
   - duration_months = the number of months between start_date and end_date.
   - If end_date is null because the role is current, calculate duration through the current date.
   - If the resume explicitly says "Present", "Ongoing", or equivalent, preserve that text in end_date while still calculating duration_months through the current date.
   - Do not invent dates that are not supported by the resume.

7. total_experience_years:
   - Sum all experience durations.
   - Convert total months to years using months / 12.
   - Round to 1 decimal place.

8. Arrays MUST always be arrays, even when there is only one item.

9. Text normalization:
   - Trim leading and trailing whitespace.
   - Remove duplicate entries in arrays.
   - Preserve meaningful capitalization.
   - Do not randomly change casing.

10. Extract as much relevant information as possible from the resume.

11. For experience entries, if the resume explicitly uses terms such as "Present", "Current", "Ongoing", or "Till Date", preserve the original term in end_date.

12. Do not infer information that is not reasonably supported by the resume.

## OUTPUT SCHEMA (STRICT)

{{
  "full_name": null,
  "email": null,
  "phone": null,
  "location": null,
  "linkedin_url": null,
  "github_url": null,
  "summary": null,
  "skills": {{
    "primary": [],
    "secondary": [],
    "tools": []
  }},
  "experience": [
    {{
      "company": null,
      "role": null,
      "start_date": null,
      "end_date": null,
      "duration_months": 0,
      "responsibilities": [],
      "technologies": []
    }}
  ],
  "education": [
    {{
      "degree": null,
      "field": null,
      "institution": null,
      "start_year": 0,
      "end_year": 0
    }}
  ],
  "projects": [
    {{
      "name": null,
      "description": null,
      "technologies": [],
      "role": null
    }}
  ],
  "certifications": [
    {{
      "name": null,
      "issuer": null,
      "year": 0
    }}
  ],
  "languages": [],
  "total_experience_years": 0
}}

## INPUT

{resume_input}

## FINAL INSTRUCTION

Return ONLY the JSON output. Ensure that it is valid JSON and directly parsable.
"""
