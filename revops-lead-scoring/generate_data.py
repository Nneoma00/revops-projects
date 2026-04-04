import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)

NUM_CONTACTS = 1000
OUTPUT_FILE = "data/contacts.csv"

PLANS = ["free", "starter", "pro", "enterprise"]

COMPANIES = [
    {
        "name": fake.company(),
        "size": random.choice(["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5000+"]),
        "numemployees": random.randint(1, 50000),
        "industry": random.choice([
            "Software", "FinTech", "HealthTech", "E-commerce",
            "Cybersecurity", "EdTech", "AI/ML", "DevTools",
            "Enterprise SaaS", "Gaming"
        ]),
        "country": random.choice([
            "United States", "United Kingdom", "Germany", "Canada",
            "India", "Nigeria", "Singapore", "Australia", "France", "Netherlands"
        ])
    }
    for _ in range(150)
]

# Assign companies to contacts — some share companies (enterprise signal)
COMPANY_ASSIGNMENTS = []
for company in COMPANIES:
    count = random.choices([1, 2, 3, 4, 5], weights=[40, 25, 15, 10, 10])[0]
    for _ in range(count):
        COMPANY_ASSIGNMENTS.append(company)

random.shuffle(COMPANY_ASSIGNMENTS)
while len(COMPANY_ASSIGNMENTS) < NUM_CONTACTS:
    COMPANY_ASSIGNMENTS.append(random.choice(COMPANIES))
COMPANY_ASSIGNMENTS = COMPANY_ASSIGNMENTS[:NUM_CONTACTS]


def random_date(start_days_ago, end_days_ago):
    days = random.randint(end_days_ago, start_days_ago)
    return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")


def generate_contact(i, company):
    api_bucket = random.choices(
        ["none", "early_builder", "active", "power"],
        weights=[30, 25, 25, 20]
    )[0]

    if api_bucket == "none":
        api_requests_total = 0
        open_source_api_requests_total = 0
        copilot_api_requests = 0
        scarf_total_api_requests = 0
        date_of_first_cloud_api_request = ""
        last_api_request_date = ""
        days_since_last_cloud_api_request = ""
        plan = "free"
    elif api_bucket == "early_builder":
        api_requests_total = random.randint(5, 50)
        open_source_api_requests_total = random.randint(0, 20)
        copilot_api_requests = random.randint(0, 10)
        scarf_total_api_requests = random.randint(0, 15)
        first_api = datetime.now() - timedelta(days=random.randint(1, 7))
        date_of_first_cloud_api_request = first_api.strftime("%Y-%m-%d %H:%M:%S")
        last_api_request_date = (first_api + timedelta(days=random.randint(0, 3))).strftime("%Y-%m-%d %H:%M:%S")
        days_since_last_cloud_api_request = random.randint(0, 5)
        plan = random.choice(["free", "starter"])
    elif api_bucket == "active":
        api_requests_total = random.randint(51, 500)
        open_source_api_requests_total = random.randint(10, 100)
        copilot_api_requests = random.randint(5, 50)
        scarf_total_api_requests = random.randint(10, 80)
        first_api = datetime.now() - timedelta(days=random.randint(7, 60))
        date_of_first_cloud_api_request = first_api.strftime("%Y-%m-%d %H:%M:%S")
        last_api_request_date = (datetime.now() - timedelta(days=random.randint(0, 10))).strftime("%Y-%m-%d %H:%M:%S")
        days_since_last_cloud_api_request = random.randint(0, 10)
        plan = random.choice(["starter", "pro"])
    else:
        api_requests_total = random.randint(500, 10000)
        open_source_api_requests_total = random.randint(100, 2000)
        copilot_api_requests = random.randint(50, 500)
        scarf_total_api_requests = random.randint(100, 1000)
        first_api = datetime.now() - timedelta(days=random.randint(30, 180))
        date_of_first_cloud_api_request = first_api.strftime("%Y-%m-%d %H:%M:%S")
        last_api_request_date = (datetime.now() - timedelta(days=random.randint(0, 3))).strftime("%Y-%m-%d %H:%M:%S")
        days_since_last_cloud_api_request = random.randint(0, 3)
        plan = random.choice(["pro", "enterprise"])

    scarf_api_total_all = (scarf_total_api_requests or 0) + random.randint(0, 20)
    base_docs = 0 if api_bucket == "none" else random.randint(1, 5)
    count_of_pages_viewed = base_docs + random.randint(0, 20)

    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "email": fake.email(),
        "plan": plan,
        "jobtitle": random.choice([
            "Software Engineer", "Backend Developer", "CTO", "Lead Engineer",
            "Full Stack Developer", "ML Engineer", "DevOps Engineer",
            "Product Manager", "Engineering Manager", "Founder"
        ]),
        "job_function": random.choice(["Engineering", "Product", "Leadership", "Data Science"]),
        "hs_seniority": random.choice(["Junior", "Mid-level", "Senior", "Lead", "Director", "C-Suite"]),
        "company_role": random.choice(["IC", "Manager", "Executive", "Founder"]),
        "company": company["name"],
        "company_size": company["size"],
        "numemployees": company["numemployees"],
        "hs_email_domain": fake.domain_name(),
        "industry": company["industry"],
        "country": company["country"],
        "createdate": random_date(180, 1),
        "hs_analytics_first_timestamp": random_date(180, 1),
        "hs_analytics_first_url": random.choice([
            "https://docs.copilotkit.com/quickstart",
            "https://copilotkit.com/",
            "https://docs.copilotkit.com/reference",
            "https://copilotkit.com/pricing"
        ]),
        "hs_analytics_last_timestamp": random_date(30, 0),
        "rb2b_captured_at": random_date(90, 1),
        "api_requests_total": api_requests_total,
        "open_source_api_requests_total": open_source_api_requests_total,
        "copilot_api_requests": copilot_api_requests,
        "scarf_total_api_requests": scarf_total_api_requests,
        "scarf_api_total_requests__all_endpoints_": scarf_api_total_all,
        "total_company_api_calls": api_requests_total + open_source_api_requests_total,
        "date_of_first_cloud_api_request": date_of_first_cloud_api_request,
        "last_api_request_date": last_api_request_date,
        "days_since_last_cloud_api_request": days_since_last_cloud_api_request,
        "date_of_first_open_source_api_request": date_of_first_cloud_api_request,
        "last_open_source_api_request_date": last_api_request_date,
        "number_of_company_active_contacts__with_cloud_api_activity_": random.randint(0, 5),
        "count_of_pages_viewed_at_docs_copilotkit_com": count_of_pages_viewed,
        "count_of_docs_page_views__from_company_": count_of_pages_viewed + random.randint(0, 10),
        "lifecyclestage": random.choice([
            "subscriber", "lead", "marketingqualifiedlead",
            "salesqualifiedlead", "opportunity"
        ]),
        "hubspotscore": random.randint(0, 100),
        "hs_lead_status": random.choice(["NEW", "OPEN", "IN_PROGRESS", "UNQUALIFIED", ""]),
        "sales_score__contact_": random.randint(0, 100),
        "hs_predictivecontactscore_v2": round(random.uniform(0, 1), 4),
        "hs_sequences_is_enrolled": random.choice([True, False]),
        "hs_sequences_enrolled_count": random.randint(0, 3),
        "hs_latest_sequence_enrolled_date": random_date(90, 1) if random.random() > 0.5 else "",
    }


import os
os.makedirs("data", exist_ok=True)

contacts = [generate_contact(i, COMPANY_ASSIGNMENTS[i]) for i in range(NUM_CONTACTS)]

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=contacts[0].keys())
    writer.writeheader()
    writer.writerows(contacts)

print(f"Generated {len(contacts)} contacts → {OUTPUT_FILE}")

buckets = {"none": 0, "early_builder": 0, "active": 0, "power": 0}
for c in contacts:
    calls = c["api_requests_total"]
    if calls == 0: buckets["none"] += 1
    elif calls <= 50: buckets["early_builder"] += 1
    elif calls <= 500: buckets["active"] += 1
    else: buckets["power"] += 1

print("\nDistribution:")
for k, v in buckets.items():
    print(f"  {k}: {v} contacts")