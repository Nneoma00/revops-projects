import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

df = pd.read_csv("data/contacts.csv")

columns = [
    "firstname", "lastname", "email", "plan", "jobtitle",
    "company", "hs_email_domain", "numemployees", "industry", "country",
    "api_requests_total", "date_of_first_cloud_api_request",
    "last_api_request_date", "days_since_last_cloud_api_request",
    "total_company_api_calls", "createdate"
]

df = df[columns]

date_columns = [
    "date_of_first_cloud_api_request",
    "last_api_request_date",
    "createdate"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

inserted = 0
for _, row in df.iterrows():
    values = []
    for col in columns:
        val = row[col]
        if pd.isnull(val):
            values.append(None)
        else:
            values.append(val)

    cur.execute("""
        INSERT INTO contacts (
            firstname, lastname, email, plan, jobtitle,
            company, hs_email_domain, numemployees, industry, country,
            api_requests_total, date_of_first_cloud_api_request,
            last_api_request_date, days_since_last_cloud_api_request,
            total_company_api_calls, createdate
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, values)
    inserted += 1

conn.commit()
cur.close()
conn.close()

print(f"Imported {inserted} contacts into Neon.")