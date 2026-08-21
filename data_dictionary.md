DATA DICTIONARY


Project: Lead Outreach Data Platform
Architecture: Star Schema

PURPOSE

This data dictionary defines the columns, data types, keys, and business
definitions for the Star Schema database.

The model contains four dimension tables and one fact table:

1. dim_date
2. dim_lead
3. dim_campaign
4. dim_account
5. fact_outreach



1. DIM_DATE


Table Purpose:
Stores calendar information used to analyze outreach activity by date.

Grain:
One record per calendar date.

Column: date_key
Type: INTEGER
Key: Primary Key
Business Definition:
Surrogate key representing a calendar date. Used by the fact table
to connect outreach activity to a specific date.

Column: full_date
Type: TEXT
Key: None
Business Definition:
The actual calendar date represented by the record.

Column: year
Type: INTEGER
Key: None
Business Definition:
Four-digit calendar year associated with the date.

Column: month
Type: INTEGER
Key: None
Business Definition:
Numeric month of the year, from 1 to 12.

Column: day
Type: INTEGER
Key: None
Business Definition:
Day of the month represented by the date.

Column: quarter
Type: INTEGER
Key: None
Business Definition:
Calendar quarter associated with the date, from 1 to 4.



2. DIM_LEAD


Table Purpose:
Stores descriptive information about leads targeted by outreach activities.

Grain:
One record per lead version. Historical versions are retained when
applicable using SCD Type 2 attributes.

Column: lead_key
Type: INTEGER
Key: Primary Key / Surrogate Key
Business Definition:
Unique surrogate identifier for a lead record in the dimension.

Column: linkedin_url
Type: TEXT
Key: Business Identifier
Business Definition:
LinkedIn URL used to identify the lead from the source data.

Column: first_name
Type: TEXT
Key: None
Business Definition:
First name of the lead.

Column: last_name
Type: TEXT
Key: None
Business Definition:
Last name of the lead.

Column: company
Type: TEXT
Key: None
Business Definition:
Company associated with the lead.

Column: job_title
Type: TEXT
Key: None
Business Definition:
Current or recorded job title of the lead.

Column: location
Type: TEXT
Key: None
Business Definition:
Geographic location associated with the lead.

Column: effective_from
Type: TEXT
Key: None
Business Definition:
Date from which this version of the lead record becomes effective.

Column: effective_to
Type: TEXT
Key: None
Business Definition:
Date until which this version of the lead record remains effective.

Column: is_current
Type: INTEGER
Key: None
Business Definition:
Indicates whether the record represents the current version of the
lead. A value of 1 indicates the current record and 0 indicates a
historical record.



3. DIM_CAMPAIGN


Table Purpose:
Stores descriptive information about outreach campaigns.

Grain:
One record per campaign version. Historical versions are retained when
applicable using SCD Type 2 attributes.

Column: campaign_key
Type: INTEGER
Key: Primary Key / Surrogate Key
Business Definition:
Unique surrogate identifier for a campaign record.

Column: campaign_name
Type: TEXT
Key: Business Identifier
Business Definition:
Name used to identify the outreach campaign.

Column: campaign_type
Type: TEXT
Key: None
Business Definition:
Type or category of the outreach campaign.

Column: target_segment
Type: TEXT
Key: None
Business Definition:
Target audience or lead segment that the campaign is designed to reach.

Column: effective_from
Type: TEXT
Key: None
Business Definition:
Date from which this version of the campaign record becomes effective.

Column: effective_to
Type: TEXT
Key: None
Business Definition:
Date until which this version of the campaign record remains effective.

Column: is_current
Type: INTEGER
Key: None
Business Definition:
Indicates whether the campaign record is the current version. A value
of 1 indicates the current record and 0 indicates a historical record.


4. DIM_ACCOUNT


Table Purpose:
Stores descriptive information about accounts used for outreach activities.

Grain:
One record per account version. Historical versions are retained when
applicable using SCD Type 2 attributes.

Column: account_key
Type: INTEGER
Key: Primary Key / Surrogate Key
Business Definition:
Unique surrogate identifier for an account record.

Column: account_name
Type: TEXT
Key: Business Identifier
Business Definition:
Name used to identify the outreach account.

Column: account_age_tier
Type: TEXT
Key: None
Business Definition:
Category representing the age or maturity tier of the account.

Column: daily_invite_limit
Type: INTEGER
Key: None
Business Definition:
Maximum number of connection invitations that the account is allowed
to send per day.

Column: daily_message_limit
Type: INTEGER
Key: None
Business Definition:
Maximum number of messages that the account is allowed to send per day.

Column: effective_from
Type: TEXT
Key: None
Business Definition:
Date from which this version of the account record becomes effective.

Column: effective_to
Type: TEXT
Key: None
Business Definition:
Date until which this version of the account record remains effective.

Column: is_current
Type: INTEGER
Key: None
Business Definition:
Indicates whether the account record is the current version. A value
of 1 indicates the current record and 0 indicates a historical record.



5. FACT_OUTREACH


Table Purpose:
Stores measurable outreach activity and connects the activity to the
date, lead, campaign, and account dimensions.

Grain:
One record per outreach activity associated with a date, lead,
campaign, and account.

Column: outreach_key
Type: INTEGER
Key: Primary Key / Surrogate Key
Business Definition:
Unique surrogate identifier for an outreach activity record.

Column: date_key
Type: INTEGER
Key: Foreign Key
References: dim_date.date_key
Business Definition:
Identifies the date on which the outreach activity occurred.

Column: lead_key
Type: INTEGER
Key: Foreign Key
References: dim_lead.lead_key
Business Definition:
Identifies the lead associated with the outreach activity.

Column: campaign_key
Type: INTEGER
Key: Foreign Key
References: dim_campaign.campaign_key
Business Definition:
Identifies the campaign associated with the outreach activity.

Column: account_key
Type: INTEGER
Key: Foreign Key
References: dim_account.account_key
Business Definition:
Identifies the account that performed the outreach activity.

Column: invites_sent
Type: INTEGER
Key: None
Business Definition:
Number of connection invitations sent during the outreach activity.

Column: connections_accepted
Type: INTEGER
Key: None
Business Definition:
Number of connection invitations accepted during the outreach activity.

Column: messages_sent
Type: INTEGER
Key: None
Business Definition:
Number of messages sent during the outreach activity.

Column: replies_received
Type: INTEGER
Key: None
Business Definition:
Number of replies received from leads during the outreach activity.

Column: meetings_booked
Type: INTEGER
Key: None
Business Definition:
Number of meetings booked as a result of the outreach activity.



SCD STRATEGY


The dim_lead, dim_campaign, and dim_account tables use a Slowly
Changing Dimension Type 2 approach where historical changes need to
be preserved.

The following columns support the SCD Type 2 implementation:

- effective_from
- effective_to
- is_current

When an attribute changes, the existing record can be retained as a
historical version and a new current record can be created.

The is_current column identifies the active version of the record.



KEY RELATIONSHIPS


fact_outreach.date_key
    -> dim_date.date_key

fact_outreach.lead_key
    -> dim_lead.lead_key

fact_outreach.campaign_key
    -> dim_campaign.campaign_key

fact_outreach.account_key
    -> dim_account.account_key



STAR SCHEMA SUMMARY


                    dim_date
                       |
                       |
dim_lead ---- fact_outreach ---- dim_campaign
                       |
                       |
                  dim_account

The fact_outreach table is the central fact table.
The four dimension tables provide descriptive context for analysing
outreach activity.