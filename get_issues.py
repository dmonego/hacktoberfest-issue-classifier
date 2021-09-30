import fetch
import features
import json

issues = fetch.all_issues()
results = []
for x in range(100):
    print(x)
    i = next(issues)
    ff = features.FeatureFinder(i)
    results.append(ff.get_results())
with open("issues.json", "w") as issuefile:
    json.dump(results, issuefile, indent=2)

#with open("repo_cache.json", "w") as repo_cache:
#    json.dump(features.repo_cache, repo_cache, indent=2)

#with open("user_cache.json", "w") as user_cache:
#    json.dump(features.user_cache, user_cache, indent=2)