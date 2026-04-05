## Project Overview

Automated RevOps system that identifies product-qualified leads from raw 
user data, scores them by conversion intent, syncs the top prospects to 
a CRM, and triggers a personalised 3-email outreach sequence — zero 
manual intervention after deployment.

**Stack:** Python · FastAPI · PostgreSQL · Neon · HubSpot CRM · GitHub Actions

**Pipeline (runs daily via GitHub Actions):**

Neon DB → Scoring engine → FastAPI → HubSpot CRM → Email sequence
(1,000 contacts)  (4 signals/top 10)  (ingest + top10)  (scored contacts)  (3 emails)

**Scoring signals:**
- API calls in the 5–50 range (primary signal — active builder window)
- Recency of first API activity
- Job seniority (CTO, Founder, Lead)
- Company headcount sweet spot (51–500 employees)

Contacts are marked as `contacted = TRUE` in the database after sync, 
preventing duplicate outreach in future pipeline runs.


