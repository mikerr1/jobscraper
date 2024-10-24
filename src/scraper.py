import json
import copy
from requests import Request, Session
from random_header_generator import HeaderGenerator
import os
import time
from pathlib import Path
import urllib.parse

project_folder = Path(os.getcwd()).parent
json_folder = os.path.join(project_folder, "resources", "json")
csv_folder = os.path.join(project_folder, "resources", "csv")

crawl = 0

keywords = ["VP", "AVP", "SVP", "Senior Manager", "Manager", "Assistant Manager",
            "Senior Project Manager", "IT Project Manager",
            "Project Manager", "Project Analyst", "IT PMO", "IT Manager",
            "Business Analyst", "Data Analyst", "Application Analyst",
            "Application Support", "Product Analyst",
            "IT Business Analyst", "Business System Analyst", "Technical Business Analyst",
            "Product Manager", "Business Intelligence", "Data Engineer",
            "IT Audit", "IT Governance", "Cyber Security", "Quality Assurance",
            "Backend Developer", "Frontend Developer", "Full Stack Developer",
            "Software Engineer", "Solution Architect",
            "System Administrator", "DBA", "IT Operation", "DevOps",
            "IT Department Head", "IT Division Head", "IT Unit Head"]

sites = [
    {
        "name": "Dealls",
        "base_url": "https://dealls.com/",
        "search_url": "https://api.sejutacita.id/v1/explore-job/job",
        "search_payload": {
            "page": 1,
            "sortParam": "mostRelevant",
            "sortBy": "asc",
            "search": "",
            "published": "true",
            "limit": 18,
            "status": "active"
        },
        "search_payload_dict_key": "search",  # to be replaced with search keyword
        "job_detail_url": "https://www.jobstreet.co.id/job/"
    },
    {
        "name": "Jobstreet",
        "base_url": "https://www.jobstreet.co.id",
        "search_url": "https://www.jobstreet.co.id/api/chalice-search/v4/search",
        "search_payload": {
            "siteKey": "ID-Main",
            "keywords": "",
            "classification": "6281,1203",  # 6281: Information technology, 1203: Banking / FinServ
            "pageSize": 100,
            "daterange": 7
        },
        "search_payload_dict_key": "keywords",  # to be replaced with search keyword
        "job_detail_url": "https://www.jobstreet.co.id/job/"
    }
]

# prepare placeholder to store list of requests to be made
search_requests = []

for site in sites:

    print(site["name"])
    if site["name"] == "Dealls":
        continue

    # prepare url and payload base on each search keyword
    for keyword in keywords:
        search_url = site["search_url"]
        search_payload = copy.copy(site["search_payload"])
        # search_payload[site["search_payload_dict_key"]] = urllib.parse.quote(keyword)
        search_payload[site["search_payload_dict_key"]] = keyword
        search_request = {"url": search_url, "payload": search_payload}
        search_requests.append(search_request)

    # for request in search_requests:
    #     print(request)

    session = Session()
    for request in search_requests:
        http_req = Request(method="GET", url=request["url"], params=request["payload"])
        prep_req = http_req.prepare()
        http_resp = session.send(prep_req, timeout=5)

        print(request)

        if http_resp.status_code == 200:
            print(f"Scraped {site["name"]} keyword {request["payload"][site["search_payload_dict_key"]]}")
            new_data = http_resp.json()
            filename = ".".join([request["payload"][site["search_payload_dict_key"]], site["name"], "json"])
            filename = os.path.join(json_folder, filename)
            with open(filename, "w") as json_file:
                json.dump(new_data, json_file, indent=4)

        time.sleep(0.5)
