import os
import csv
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def score_contacts():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            firstname,
            lastname,
            email,
            jobtitle,
            company,
            api_requests_total,
            date_of_first_cloud_api_request,
            numemployees,

            -- Signal 1: API calls
            CASE
                WHEN api_requests_total BETWEEN 5 AND 50 THEN 10
                WHEN api_requests_total > 50 THEN 7
                WHEN api_requests_total BETWEEN 1 AND 4 THEN 3
                ELSE 0
            END

            +

            -- Signal 2: Recency
            CASE
                WHEN date_of_first_cloud_api_request >= NOW() - INTERVAL '3 days' THEN 10
                WHEN date_of_first_cloud_api_request >= NOW() - INTERVAL '7 days' THEN 7
                WHEN date_of_first_cloud_api_request >= NOW() - INTERVAL '14 days' THEN 3
                ELSE 0
            END

            +

            -- Signal 3: Seniority
            CASE
                WHEN LOWER(jobtitle) LIKE ANY(ARRAY['%cto%','%founder%','%vp%','%director%','%lead%']) THEN 10
                WHEN LOWER(jobtitle) LIKE ANY(ARRAY['%senior%','%engineer%','%developer%']) THEN 7
                ELSE 3
            END

            +

            -- Signal 4: Company size
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

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def save_output(results):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/top10_{today}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "rank", "firstname", "lastname", "email",
            "jobtitle", "company", "api_calls", "score"
        ])
        for i, row in enumerate(results, 1):
            writer.writerow([
                i, row[1], row[2], row[3],
                row[4], row[5], row[6], row[9]
            ])

    print(f"Top 10 saved to {filename}")
    return filename

def main():
    print("\nRunning scoring pipeline...\n")
    results = score_contacts()

    print("Top 10 Sales-Ready Contacts:\n")
    for i, row in enumerate(results, 1):
        print(f"{i}. {row[1]} {row[2]} — {row[4]} at {row[5]}")
        print(f"   API Calls: {row[6]} | Score: {row[9]}\n")

    save_output(results)


if __name__ == "__main__":
    main()