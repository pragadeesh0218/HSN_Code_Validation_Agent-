# HSN Code Validation Agent – ADK-Based Design

## Overview
This intelligent agent is designed using the **Agent Developer Kit (ADK)** conceptual framework. Its purpose is to validate Harmonized System Nomenclature (HSN) codes using a provided master Excel dataset.

---

## 1. Agent Design using ADK

### a. Intents
| Intent Name        | Description                                 |
|--------------------|---------------------------------------------|
| `ValidateCode`     | Validate a single HSN code                  |
| `BatchValidation`  | Validate multiple HSN codes from a file     |

### b. Entities
| Entity Name | Type   | Description                                |
|-------------|--------|--------------------------------------------|
| `HSNCode`   | String | The HSN code input by the user             |
| `FileInput` | File   | Uploaded file containing HSN codes         |

### c. Fulfillment Modules
- **HSNValidator Module** (Python backend)
  - Validates if the code is numeric and of correct length
  - Checks if the code exists in the dataset
  - Optionally checks parent hierarchy for completeness

### d. Response Examples
- Valid Code:
  > ✅ "HSN Code `01011010` is valid. Description: PURE-BRED BREEDING ANIMALS HORSES"
- Invalid Code:
  > ❌ "HSN Code `011122` is invalid. Reason: Not found in master dataset"

---

## 2. Data Handling

- **Data Source**: `HSN_SAC.xlsx` (Excel file with HSNCode and Description)
- **Strategy**:
  - File is preloaded at agent startup
  - Converted to a searchable Pandas DataFrame
- **Scalability**:
  - Pandas handles thousands of rows efficiently in memory
  - For larger deployments, a database or cloud function would be ideal

---

## 3. Validation Logic

### a. Format Validation
- Input must be numeric
- Valid lengths: 2, 4, 6, or 8 digits

### b. Existence Validation
- Code must exist in the `HSNCode` column of the dataset

### c. (Optional) Hierarchical Validation
- For a code like `01011010`, validate existence of parent levels: `010110`, `0101`, `01`

---

## 4. Agent Architecture Diagram

```plaintext
User Input (Text / File)
       │
       ▼
  ADK Intent Parser
       │
       ▼
Entity Extraction → { HSNCode / FileInput }
       │
       ▼
Fulfillment Logic (HSNValidator.py)
       │
       ▼
Validation Result
       │
       ▼
Formatted Response to User
```

---

## 5. Extendability

- Dataset updates can be supported by reloading the Excel file
- Conversational interface (chatbot or Google Assistant) could replace the web form
- Future additions: voice input, API integration, user feedback loop

---

## 6. ADK-to-Flask Mapping (for clarity)

| ADK Component     | Your Flask Equivalent                 |
|------------------|----------------------------------------|
| Intent            | Flask route (`/validate`, `/batch`)   |
| Entity Extraction | `request.form.get('hsn_code')`         |
| Fulfillment       | `hsn_validator.validate()` function    |
| Data Store        | `HSN_SAC.xlsx` loaded via pandas       |
| Response          | `jsonify()` or `render_template()`     |