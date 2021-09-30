from dotenv import dotenv_values
import requests
import json
from httpcache import CachingHTTPAdapter
s = requests.Session()
s.mount('http://', CachingHTTPAdapter())
s.mount('https://', CachingHTTPAdapter())

config = dotenv_values(".env")

repo_cache = {}
def get_repo(user, repo):
    if not user in repo_cache or not repo in repo_cache[user]:
        r = requests.get(f'http://api.github.com/repos/{user}/{repo}')
        if not user in repo_cache:
            repo_cache[user] = {}
        repo_cache[user][repo] = json.loads(r.text)
    return repo_cache[user][repo]

user_cache = {}
def get_user(user):
    if not user in user_cache:
        r = requests.get(f'http://api.github.com/users/{user}')
        repo_cache[user] = json.loads(r.text)
    return repo_cache[user]

class Feature:
    def __init__(self, issue):
        self.issue = issue

    def get_value(self):
        pass

class UserFeature(Feature):

    def getUser(self):
        project_url = self.issue["repository_url"]
        url_parts = project_url.split("/")
        user, _ = url_parts[-2:]
        return get_user(user)

class ProjectFeature(Feature):

    def getProject(self):
        project_url = self.issue["repository_url"]
        url_parts = project_url.split("/")
        user, repo = url_parts[-2:]
        return get_repo(user, repo)


class ProjectCreateDateFeature(ProjectFeature):
    name = "ProjectCreateDate"
    def get_value(self):
        project = self.getProject()
        return project["created_at"]

class ProjectStarsFeature(ProjectFeature):
    name = "ProjectStars"
    def get_value(self):
        project = self.getProject()
        return project["stargazers_count"]

class ProjectLicenseFeature(ProjectFeature):
    name = "ProjectLicense"
    def get_value(self):
        project = self.getProject()
        if "license" in project and project["license"] is not None:
            return project["license"].get("key", None)
        else:
            return None

class ProjectForksFeature(ProjectFeature):
    name = "ProjectForks"
    def get_value(self):
        project = self.getProject()
        return project["forks"]

class ProjectSizeFeature(ProjectFeature):
    name = "ProjectSize"
    def get_value(self):
        project = self.getProject()
        return project["size"]

class IssueCreateDateFeature(Feature):
    name = "IssueCreateDate"
    def get_value(self):
        return self.issue["created_at"]

class IssueUrlFeature(Feature):
    name = "IssueUrl"
    def get_value(self):
        return self.issue["html_url"]

class IssueNameFeature(Feature):
    name = "IssueName"
    def get_value(self):
        return self.issue["title"]

class ReportingUserFeature(Feature):
    name = "ReportingUser"
    def get_value(self):
        return self.issue["user"]["login"]

class RepoOwnerFeature(Feature):
    name = "RepoOwner"
    def get_value(self):
        repo_url_parts = self.issue["repository_url"].split("/")
        user = repo_url_parts[-2]
        return user

class RepoNameFeature(Feature):
    name = "RepoName"
    def get_value(self):
        repo_url_parts = self.issue["repository_url"].split("/")
        repo = repo_url_parts[-1]
        return repo

class RepoUrlFeature(Feature):
    name = "RepoUrl"
    def get_value(self):
        repo_url_parts = self.issue["repository_url"].split("/")
        user, repo = repo_url_parts[:-2]
        return f"https://github.com/{user}/{repo}"


class IssueBodyFeature(Feature):
    name = "IssueBody"
    def get_value(self):
        return self.issue["body"]

class IssueLabelCountFeature(Feature):
    name = "LabelCount"
    def get_value(self):
        return len(self.issue["labels"])

class IssueLabelsFeature(Feature):
    name = "Labels"
    def get_value(self):
        labels = ", ".join([ l["name"] for l in self.issue["labels"] ])
        return labels

class IssueAuthorAssociationFeature(Feature):
    name = "IssueAuthorAssociation"
    def get_value(self):
        return self.issue["author_association"]

class UserFollowersFeature(UserFeature):
    name = "UserFollowers"
    def get_value(self):
        user = self.getUser()
        return user["followers"]

class UserFollowingFeature(UserFeature):
    name = "UserFollowing"
    def get_value(self):
        user = self.getUser()
        return user["following"]

class FeatureFinder:
    features = [
        IssueNameFeature,
        IssueUrlFeature,
        IssueBodyFeature,
        IssueCreateDateFeature,
        IssueLabelCountFeature,
        IssueLabelsFeature,
        ReportingUserFeature,
        RepoOwnerFeature,
        RepoUrlFeature]

    enriched_features = [
        ProjectCreateDateFeature,
        ProjectStarsFeature,
        ProjectLicenseFeature,
        ProjectForksFeature,
        ProjectSizeFeature,
        UserFollowersFeature,
        UserFollowingFeature]
    

    def __init__(self, issue):
        self.issue = issue

    def get_results(self):
        results = {}
        for Feature in self.features:
            f = Feature(self.issue)
            results[f.name] = f.get_value()
        return results
