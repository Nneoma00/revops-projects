import os
from datetime import datetime
from score_and_output import main as run_scoring
from sync_to_hubspot import sync_contacts

def run_pipeline():
    print(f"\n--- RevOps Pipeline Starting: {datetime.now()} ---\n")

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/top10_{today}.csv"

    if os.path.exists(filename):
        print(f"Today's CSV already exists. Skipping scoring...\n")
    else:
        print("Step 1: Scoring contacts and generating top 10...\n")
        run_scoring()

    print("\nStep 2: Syncing top 10 to HubSpot...\n")
    sync_contacts()

    print(f"\n--- Pipeline Complete: {datetime.now()} ---\n")

if __name__ == "__main__":
    run_pipeline()