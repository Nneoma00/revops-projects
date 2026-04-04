import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        firstname VARCHAR(100),
        lastname VARCHAR(100),
        email VARCHAR(255),
        plan VARCHAR(50),
        jobtitle VARCHAR(100),
        company VARCHAR(255),
        hs_email_domain VARCHAR(255),
        numemployees INTEGER,
        industry VARCHAR(100),
        country VARCHAR(100),
        api_requests_total INTEGER DEFAULT 0,
        date_of_first_cloud_api_request TIMESTAMP,
        last_api_request_date TIMESTAMP,
        days_since_last_cloud_api_request INTEGER,
        total_company_api_calls INTEGER DEFAULT 0,
        createdate TIMESTAMP
    )
""")

conn.commit()
cur.close()
conn.close()

print("Table created successfully.")