# Run Instructions for HSN Code Validation Agent

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Setup

1. Clone or download the repository from GitHub.

```bash
git clone https://github.com/pragadeesh0218/HSN_Code_Validation_Agent-#.git
cd HSN_Code_Validation_Agent-#
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Make sure `HSN_SAC.xlsx` is in the project root directory.

## Running the App

```bash
python app.py
```

- The app will start on: `http://localhost:5000`
- Open it in your browser to use single or batch HSN code validation.

## Notes

- Batch results are stored in session for the current run.
- You can reset by refreshing or uploading a new file.