# HSN Code Validation Agent

This project validates HSN (Harmonized System Nomenclature) codes using a master Excel dataset. Users can validate a single code or upload a file for batch validation.

## Features

- Validate single HSN code via input form
- Upload CSV/Excel for batch HSN validation
- Displays result along with descriptions
- Flask-based interface

## ADK-Based Design Summary

Although implemented using Flask, this app is conceptually modeled using Google’s **Agent Developer Kit (ADK)**.

Key Concepts:

- **Intents**: Validate single or batch HSN codes
- **Entities**: Extracted codes and file inputs
- **Fulfillment**: Python logic to validate using master dataset

👉 See [`design_adk.md`](./design_adk.md) for the full design specification.

## Screenshots

![index](screenshots/index.png)
![batch results](screenshots/batch_results.png)

## License

MIT