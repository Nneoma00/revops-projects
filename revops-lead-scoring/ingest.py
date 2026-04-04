import os
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from score_and_output import main as run_scoring

load_dotenv()

app = FastAPI()

class Contact(BaseModel):
    firstname: str
    lastname: str
    email: str
    plan: Optional[str] = None
    jobtitle: Optional[str] = None
    company: Optional[str] = None
    hs_email_domain: Optional[str] = None
    numemployees: Optional[int] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    api_requests_total: Optional[int] = 0
    date_of_first_cloud_api_request: Optional[str] = None
    last_api_request_date: Optional[str] = None
    days_since_last_cloud_api_request: Optional[int] = None
    total_company_api_calls: Optional[int] = 0
    createdate: Optional[str] = None


@app.get("/")
def welcome():
    return {"message": "Hello World. Welcome to my Lead Scoring API."}

@app.post("/ingest")
def ingest_contact(contact: Contact):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    # Upsert — update if email exists, insert if not
    cur.execute("""
        INSERT INTO contacts (
            firstname, lastname, email, plan, jobtitle,
            company, hs_email_domain, numemployees, industry, country,
            api_requests_total, date_of_first_cloud_api_request,
            last_api_request_date, days_since_last_cloud_api_request,
            total_company_api_calls, createdate
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT DO NOTHING
                
    """, (
        contact.firstname, contact.lastname, contact.email,
        contact.plan, contact.jobtitle, contact.company,
        contact.hs_email_domain, contact.numemployees,
        contact.industry, contact.country,
        contact.api_requests_total, contact.date_of_first_cloud_api_request,
        contact.last_api_request_date, contact.days_since_last_cloud_api_request,
        contact.total_company_api_calls, contact.createdate
    ))

    conn.commit()
    cur.close()
    conn.close()

    # Trigger scoring pipeline automatically
    run_scoring()

    return {"status": "success", "message": f"Contact {contact.email} ingested and scoring updated."}


@app.get("/top10")
def get_top10():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        SELECT
            firstname, lastname, email, jobtitle, company,
            api_requests_total,
            CASE
                WHEN api_requests_total BETWEEN 5 AND 50 THEN 10
                WHEN api_requests_total > 50 THEN 7
                WHEN api_requests_total BETWEEN 1 AND 4 THEN 3
                ELSE 0
            END
            +
            CASE
                WHEN date_of_first_cloud_api_request >= NOW() - INTERVAL '3 days' THEN 10
                WHEN date_of_first_cloud_api_request >= NOW() - INTERVAL '7 days' THEN 7
                WHEN date_of_first_cloud_api_request >= NOW() - INTERVAL '14 days' THEN 3
                ELSE 0
            END
            +
            CASE
                WHEN LOWER(jobtitle) LIKE ANY(ARRAY['%cto%','%founder%','%vp%','%director%','%lead%']) THEN 10
                WHEN LOWER(jobtitle) LIKE ANY(ARRAY['%senior%','%engineer%','%developer%']) THEN 7
                ELSE 3
            END
            +
            CASE
                WHEN numemployees BETWEEN 51 AND 500 THEN 10
                WHEN numemployees BETWEEN 501 AND 5000 THEN 7
                WHEN numemployees > 5000 THEN 5
                ELSE 3
            END
            AS total_score
        FROM contacts
        WHERE api_requests_total > 0
        ORDER BY total_score DESC, date_of_first_cloud_api_request DESC
        LIMIT 10
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "rank": i + 1,
            "name": f"{row[0]} {row[1]}",
            "email": row[2],
            "jobtitle": row[3],
            "company": row[4],
            "api_calls": row[5],
            "score": row[6]
        }
        for i, row in enumerate(rows)
    ]



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ingest:app", reload=True)