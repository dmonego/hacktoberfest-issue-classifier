from dotenv import dotenv_values
import requests
import json

config = dotenv_values(".env")

def fetch_issues(q="label:hacktoberfest", page=1):
    req = requests.get("https://api.github.com/search/issues", 
        params={
            "q": q,
            "page": page,
            "per_page": 100
        },
        auth=(config["GITHUB_USER"], config["GITHUB_TOKEN"]))
    return req

def all_issues():
    page = 1
    issue_request = fetch_issues()
    issues = json.loads(issue_request.text)
    while len(issues["items"]) > 0:
        for issue in issues["items"]:
            yield issue
        page += 1 
        issue_request = fetch_issues(page=page)
        issues = json.loads(issue_request.text)



if __name__ == "__main__":
    fetch_issues()