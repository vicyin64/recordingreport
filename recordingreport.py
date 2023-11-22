import csv
import requests

# Webex API endpoints
report_url = "https://webexapis.com/v1/recordingReport/accessSummary"
people_url = "https://webexapis.com/v1/people"

# Webex access token
access_token = "<BEARER_TOKEN>"

# Headers with the access token
headers = {
    "Authorization": "Bearer " + access_token,
    "Content-Type": "application/json",
}

# List to store host emails
host_emails = []

# Send a GET request to the People API to get all users
response = requests.get(people_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Get the response data
    data = response.json()

    # Extract the host emails from the response
    for person in data["items"]:
        email = person["emails"][0]
        host_emails.append(email)
else:
    print(f"Failed to retrieve user emails. Error: {response.text}")

# Create a CSV file to store the results
csv_file = open("recording_audit_report.csv", "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Recording ID", "Meeting Topic", "Host Email", "View Count", "Download Count", "Site URL", "Time Recorded"])

# Iterate through each host email
for email in host_emails:
    # Query parameters with host email
    params = {
        "hostEmail": email,
	"from":"2023-10-01T00:00:00Z",
	"to":"2023-11-09T00:00:00Z"
    }

    # Send a GET request to the Webex API
    response = requests.get(report_url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the response data
        data = response.json()

        # Process the recording audit report summaries
        for summary in data["items"]:
            # Extract the necessary information
            recording_id = summary["recordingId"]
            meeting_topic = summary["topic"]
            host_email = summary["hostEmail"]
            view_count = summary["viewCount"]
            download_count = summary["downloadCount"]
            site_url = summary["siteUrl"]
            time_recorded = summary.get("timeRecorded", "")

            # Write the summary details to the CSV file
            csv_writer.writerow([recording_id, meeting_topic, host_email, view_count, download_count, site_url, time_recorded])
    else:
        print(f"Failed to retrieve recording audit report summaries for host {email}. Error: {response.text}")

# Close the CSV file
csv_file.close()
