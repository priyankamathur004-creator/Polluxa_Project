# End-to-End Data Flow

## Overview

The data pipeline moves lead data from the source system through
ingestion and staging into the Star Schema and finally to the
presentation/reporting layer.

## Data Flow

```text
Source
  |
  | Lead CSV / API data
  v
FastAPI Ingestion
  |
  | Validation + API security
  v
SQLite Staging / Raw Leads
  |
  | Incremental loading
  | Idempotency
  | Error handling
  v
Transformation Layer
  |
  | Dimension key lookup
  | Data standardization
  v
Star Schema
  |
  +------------------+
  |                  |
  v                  v
Dimensions       Fact Table
  |             fact_outreach
  |
  +------------------+
           |
           v
Presentation / Reporting Layer
           |
           v
Dashboards / Analytics


Star Schema

The presentation layer is supported by the following Star Schema:

dim_date
dim_lead
dim_campaign
dim_account
fact_outreach
Fact Table Grain

One row in fact_outreach represents one outreach activity
for a lead, campaign, account, and date.

Relationships
dim_date
    |
    +---- date_key
              |
              v
        fact_outreach
              ^
              |
    +---------+---------+
    |         |         |
    |         |         |
dim_lead  dim_campaign  dim_account


Pipeline Stages
1. Source

Lead information originates from the supplied lead data source.

2. Ingestion

FastAPI endpoints receive and process the source data.

3. Staging

Raw lead information is stored in SQLite.

4. Transformation

Data is cleaned and dimension keys are assigned.

5. Star Schema

The transformed data is stored in fact and dimension tables.

6. Presentation

The Star Schema provides structured data for reporting,
analytics, and dashboards.


### Save the file

In VS Code:

**File → Save**

Make sure it is:

```text
data_flow.md


