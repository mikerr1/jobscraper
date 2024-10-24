import json
from datetime import datetime
import copy
from requests import Request, Session
from random_header_generator import HeaderGenerator
import os
import time
from pathlib import Path


def convert_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    return date_obj.strftime("%d-%b-%y %H:%M")




project_folder = Path(os.getcwd()).parent
json_folder = os.path.join(project_folder, "resources", "json")
csv_folder = os.path.join(project_folder, "resources", "csv")

keywords = ["Business Analyst"]

sites = [
    {
        "name": "Dealls",
        "base_url": "https://dealls.com/",
        "search_url": "https://api.sejutacita.id/v1/explore-job/job",
        "search_payload": {
            "page": 1,
            "sortParam": "publishedAt",
            "sortBy": "desc",
            "search": "",
            "published": "true",
            "limit": 18,
            "status": "active"
        },
        "job_detail_url": "https://dealls.com/loker/" # sample: https://dealls.com/loker/business-process-and-standarization-analyst~astra-financial
    }
]

search_requests = []

for site in sites:
    print(site)

    # prepare url and payload base on each search keyword
    for keyword in keywords:
        search_url = site["search_url"]
        search_payload = copy.copy(site["search_payload"])
        search_payload["keywords"] = keyword
        search_request = {"url": search_url, "payload": search_payload}
        search_requests.append(search_request)

    # for request in search_requests:
    #     print(request)

    session = Session()
    for request in search_requests:
        http_req = Request(method="GET", url=request["url"], params=request["payload"])
        prep_req = http_req.prepare()
        http_resp = session.send(prep_req, timeout=5)

        if http_resp.status_code == 200:
            new_data = http_resp.json()
            filename = ".".join([request["payload"]["keywords"], site["name"], "json"])
            filename = os.path.join(json_folder, filename)
            with open(filename, "w") as json_file:
                json.dump(new_data, json_file, indent=4)

        time.sleep(2)
