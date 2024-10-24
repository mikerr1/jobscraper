import json
from datetime import datetime
import copy
import requests
from requests import Request, Session
from random_header_generator import HeaderGenerator
import os
import time
from pathlib import Path

query = """
query searchJobs($data: JobSearchConditionInput!) {
  searchJobs(data: $data) {
    jobsInPage {
      id
      title
      workArrangementOption
      status
      createdAt
      updatedAt
      isActivelyHiring
      isHot
      isApplied
      shouldShowSalary
      educationLevel
      type
      fraudReportFlag
      salaryEstimate {
        minAmount
        maxAmount
        CurrencyCode
        __typename
      }
      company {
        ...CompanyFields
        __typename
      }
      citySubDivision {
        id
        name
        __typename
      }
      city {
        ...CityFields
        __typename
      }
      country {
        ...CountryFields
        __typename
      }
      salaries {
        ...SalaryFields
        __typename
      }
      location {
        ...LocationFields
        __typename
      }
      minYearsOfExperience
      maxYearsOfExperience
      source
      type
      hierarchicalJobCategory {
        id
        level
        name
        children {
          name
          level
          id
          __typename
        }
        parents {
          id
          level
          name
          __typename
        }
        __typename
      }
      skills {
        skill {
          id
          name
          __typename
        }
        mustHave
        __typename
      }
      traceInfo
      __typename
    }
    numberOfJobsCreatedInLast14Days
    totalJobs
    expInfo
    __typename
  }
}
"""

url = "https://glints.com/api/v2/graphql?op=searchJobs"

payload = {
    "operationName": "searchJobs",
    "query": query,
    "variables": {
        "data": {
            "SearchTerm": "project manager",
            "CountryCode": "ID",
            "limit": 30,
            "offset": 90,
            "includeExternalJobs": True,
            "searchVariant": "VARIANT_A",
            "LocationIds": ["78d63064-78a1-4577-8516-036a6c5e903e"]
        }
    }
}

headers = {
    "authority": "glints.com",
    "method": "POST",
    "path": "/api/v2/graphql?op=searchJobs",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "id",
    "content-length": "2571",
    "content-type": "application/json",
    "cookie": "_ga=GA1.1.1104959957.1721995908; _gcl_au=1.1.1088349204.1721995908; _wpfuuid=6cc9e6b5-50a7-4af5-8a51-1510e12a0c83; _fbp=fb.1.1721995908803.561964591277480251; _tgpc=3d188e7f-6460-5423-bd54-c03ff3852f13; _tt_enable_cookie=1; _ttp=KapZduHlciqSX6fEZlwl_0V3fUP; session=Fe26.2**ec9c27fc5755fa0a78ea069fbe2ed570a36ce93e812d91b194a425d6e0e2557e*ORi13QTkxZlUR3iB9WIwVQ*OV_ePa7EIJGwGx5FeFTdbr_sxoQuZlL2q2y-uFj3zX17bKrY-YXXIcxRTPuLV-_l**cdf6ac11af754f18b7ed5f9014a68a02ab1b6dd3d4ef9a38b7ee69ece7dc43c0*GA9eP3oTTdpkvWHCvCmSIrT7OBs3NpK5ijXMxO3La4M; _ga_WMM977BJLD=GS1.1.1721998802.2.0.1721998802.60.0.0; AMP_14529b1d7b=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI5MDk5NTYxYy04MWZiLTQyMmUtOGE3Yy00ZTI0NTUxMmJjMDAlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjI5MTY0ZjM1NS03ZmU5LTQyOGYtODY0ZS1hNjI3M2M4M2U2ZmYlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzIyMzM0MDg0MDc3JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcyMjMzNDM5ODMxNCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMzklN0Q=; _ga_2XPDTDTJTW=GS1.1.1722334084.1.1.1722335923.60.0.0; _gcl_gs=2.1.k1$i1722402480; _gcl_aw=GCL.1722402484.CjwKCAjwnqK1BhBvEiwAi7o0X6Er4eXvgwNLgDF4DZqfyiG8cjYYTc2kkQBwUZKllkgy4pOTRvWBVBoCnS4QAvD_BwE; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229164f355-7fe9-428f-864e-a6273c83e6ff%22%2C%22first_id%22%3A%22190eef456e231f-0506d007ddb9e84-26001f51-2073600-190eef456e3b5b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22google%22%2C%22%24latest_utm_medium%22%3A%22cpc%22%2C%22%24latest_utm_campaign%22%3A%22ID%7CMarketplace%7CPerformancemax%7CMPA-75%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwZWVmNDU2ZTIzMWYtMDUwNmQwMDdkZGI5ZTg0LTI2MDAxZjUxLTIwNzM2MDAtMTkwZWVmNDU2ZTNiNWIiLCIkaWRlbnRpdHlfbG9naW5faWQiOiI5MTY0ZjM1NS03ZmU5LTQyOGYtODY0ZS1hNjI3M2M4M2U2ZmYiLCIkaWRlbnRpdHlfZW1haWwiOiJtaWNoYWVscmF5bW9uZDJAZ21haWwuY29tIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%229164f355-7fe9-428f-864e-a6273c83e6ff%22%7D%2C%22%24device_id%22%3A%22190eef456e231f-0506d007ddb9e84-26001f51-2073600-190eef456e3b5b%22%7D; builderSessionId=7a660d7122c0485b9c2de66929563350; _tguatd=eyJzYyI6IihkaXJlY3QpIn0=; _tgidts=eyJzaCI6ImQ0MWQ4Y2Q5OGYwMGIyMDRlOTgwMDk5OGVjZjg0MjdlIiwiY2kiOiJhMzU0Zjg5NC1iMWIwLTU2ZGEtODkzYi1mMmYwYzk3NDZlNDMiLCJzaSI6IjYwZTY5Yzc2LTZhZmQtNTU3YS1hMmQ5LTFhM2Y3NWFlYjhhMiJ9; traceInfo=%7B%22expInfo%22%3A%22mgtDstExperimentRecmdApplication%3Aw10_0315%22%2C%22requestId%22%3A%221c9a0515c3477c5a24f8a34152bcbb85%22%7D; amplitude_id_26bdf4b56b304d7bfc6275ea77f2310cglints.com=eyJkZXZpY2VJZCI6IjBlNDEwY2QyLTQxZDMtNDI3MC1iZjUxLWE0YzQ0ZTljMDAzMVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTcyMjY1MzY2MTI5NCwibGFzdEV2ZW50VGltZSI6MTcyMjY1NDU3NzY4MiwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MjksInNlcXVlbmNlTnVtYmVyIjoyOX0=; _tglksd=eyJzIjoiNjBlNjljNzYtNmFmZC01NTdhLWEyZDktMWEzZjc1YWViOGEyIiwic3QiOjE3MjI2NTM2NjEyMzEsInNvZCI6IihkaXJlY3QpIiwic29kdCI6MTcyMjU3OTc1MzA0MSwic29kcyI6ImMiLCJzb2RzdCI6MTcyMjY1NDU3NzY5NSwiZyI6IkNqd0tDQWp3bnFLMUJoQnZFaXdBaTdvMFg2RXI0ZVh2Z3dOTGdERjREWnFmeWlHOGNqWVlUYzJra1FCd1VaS2xsa2d5NHBPVFJ2V0JWQm9DblM0UUF2RF9Cd0UiLCJndCI6MTcyMjQwMjQ4MzU5OX0=; _ga_FQ75P4PXDH=GS1.1.1722653661.8.1.1722654577.60.0.0; _tgsid=eyJscGQiOiJ7XCJscHVcIjpcImh0dHBzOi8vZ2xpbnRzLmNvbSUyRmlkXCIsXCJscHRcIjpcIkdsaW50cyUzQSUyMFNpdHVzJTIwTG93b25nYW4lMjBLZXJqYSUyMFRlcmJhaWslMjBkaSUyMEluZG9uZXNpYVwiLFwibHByXCI6XCJcIn0iLCJwcyI6ImVmOWMwZWQwLTk0MWItNDZhNS1iYTRlLTVkOGYxOWVlYTcxOCIsInB2YyI6IjIiLCJzYyI6IjYwZTY5Yzc2LTZhZmQtNTU3YS1hMmQ5LTFhM2Y3NWFlYjhhMjotMSIsImVjIjoiOCIsInB2IjoiMSIsInRpbSI6IjYwZTY5Yzc2LTZhZmQtNTU3YS1hMmQ5LTFhM2Y3NWFlYjhhMjoxNzIyNjUzNjY0ODc1Oi0xIn0=",
    "origin": "https://glints.com",
    "priority": "u=1, i",
    "referer": "https://glints.com/id/opportunities/jobs/explore?keyword=project+manager&country=ID&locationId=78d63064-78a1-4577-8516-036a6c5e903e&locationName=DKI+Jakarta",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "traceparent": "00-d9a62ccdd629c9ddf8d51780c42d0b49-61680ad6274cc71a-01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "x-glints-country-code": "ID"
}

# s = Session()
# r = Request(method="POST", url=url, data=json.dumps(payload), headers=headers).prepare()



try:
    # response = s.send(r, timeout=5)
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print(response.status_code)
    print(response.text)
    print(json.dump(response.json(), indent=4))


    # with open("test_glints.txt", "w") as f:
    #     f.write(text)

    # new_data = response.json()
    # with open("test_glints.json", "w") as f:
    #     json.dump(new_data, f, indent=4)

except Exception as e:
    print(e)
