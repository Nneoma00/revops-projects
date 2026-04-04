👋🏾 Hi! 
My name is Nneoma Uche---most folk just call me Uche. I'm a backend engineer specializing in Revenue Operations for teams of various sizes. 
I handle AI Integrations, CRM automations, custom API development, sales pipelines, sales forecasting, among others.
My strength lies at the intersection of RevOps + Engineering.

To help you decide if I'm the right fit for your business, here are a few projects I've built (similar ones deployed for past clients), which required not just extensive experience with CRM software, 
but also hands-on engineering experience, data analysis & visualization. 
P.S: I don't use low-code tools very much as I can build custom integrations from scratch. But I do have clients who specifically request them, so I've learnt to use tools like n8n and Make.com, to drive the same reults.

# Projects ⬇️
## 01 — PLG lead scoring + outreach pipeline:

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

→ [View repo](link) · [Read docs](link)
