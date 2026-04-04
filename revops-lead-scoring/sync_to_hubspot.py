import os
import csv
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_ACCESS_TOKEN")
BASE_URL = "https://api.hubapi.com/crm/v3/objects/contacts"
HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_API_KEY}",
    "Content-Type": "application/json"
}


def sync_contacts():
    # Find today's top 10 CSV
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/top10_{today}.csv"

    if not os.path.exists(filename):
        print(f"No file found for today: {filename}")
        return

    synced = 0
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            payload = {
                "properties": {
                    "firstname": row["firstname"],
                    "lastname": row["lastname"],
                    "email": row["email"],
                    "jobtitle": row["jobtitle"],
                    "company": row["company"],
                    "revops_score": row["score"],
                    "api_calls": row["api_calls"]
                }
            }

            response = requests.post(BASE_URL, headers=HEADERS, json=payload)

            if response.status_code == 201:
                print(f"Synced: {row['firstname']} {row['lastname']}")
                synced += 1
                # Mark as contacted in Neon
                conn = psycopg2.connect(os.getenv("DATABASE_URL"))
                cur = conn.cursor()
                cur.execute("""
                    UPDATE contacts 
                    SET contacted = TRUE, contacted_date = NOW()
                    WHERE email = %s
                """, (row["email"],))
                conn.commit()
                cur.close()
                conn.close()
            elif response.status_code == 409:
                print(f"Already exists: {row['email']}")
            else:
                print(f"Failed: {row['email']} — {response.text}")

    print(f"\n{synced} contacts synced to HubSpot.")


if __name__ == "__main__":
    sync_contacts()