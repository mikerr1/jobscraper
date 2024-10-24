import json
import os
import time
from pathlib import Path
from datetime import datetime
import csv



def convert_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    return date_obj.strftime("%d-%b-%y %H:%M")

def convert_date2(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date_obj.strftime("%d-%b-%y %H:%M")


project_folder = Path(os.getcwd()).parent
json_folder = os.path.join(project_folder, "resources", "json")
csv_folder = os.path.join(project_folder, "resources", "csv")

files = os.listdir(json_folder)

for file in files:
    json_file = os.path.join(json_folder, file)
    csv_file = os.path.join(csv_folder, file.replace("json", "csv"))

    if "Jobstreet" in file:

        # read json file
        with open(json_file, "r") as f:
            data = json.load(f)

        headers = ["listing_date", "title", "company", "location", "work_type", "link"]
        rows = []

        for ad in data["data"]:

            title = ad["title"]
            company = ad["advertiser"]["description"]
            location = ad["location"]
            work_type = ad["workType"]
            listing_date = convert_date(ad["listingDate"])
            link = f"https://www.jobstreet.co.id/job/{ad["id"]}"

            rows.append([listing_date, title, company, location, work_type, link])

        with open(csv_file, "w", newline="") as c:
            writer = csv.writer(c, delimiter=";")
            writer.writerow(headers)
            try:
                writer.writerows(rows)
            except Exception as e:
                continue

    if "Dealls" in file:

        with open(json_file, "r") as f:
            data = json.load(f)

        headers = ["listing_date", "title", "company", "location", "work_type", "link"]
        rows = []

        for ad in data["data"]["docs"]:

            title = ad["role"]
            company = ad["company"]["name"]
            location = ad["city"]["name"] if ad["city"] is not None else "N/A"
            work_type = ad["employmentTypes"][0]
            listing_date = convert_date2(ad["createdAt"])
            link = f"https://dealls.com/loker/{ad["slug"]}~{ad["company"]["slug"]}"

            rows.append([listing_date, title, company, location, work_type, link])
            # print(listing_date, title, company, location, work_type, link)

        with open(csv_file, "w", newline="") as c:
            writer = csv.writer(c, delimiter=";")
            writer.writerow(headers)
            try:
                writer.writerows(rows)
            except Exception as e:
                continue


