import fetch
import features
import json
import sys

dataset = sys.argv[1]
issues = fetch.all_issues()
raw = []
results = []
for x in range(150):
    print(x)
    i = next(issues)
    raw.append(i)
    ff = features.FeatureFinder(i)
    results.append(ff.get_results())
with open(f"datasets/{dataset}/raw.json", "w") as raw_results_file:
    json.dump(raw, raw_results_file, indent=2)
with open(f"datasets/{dataset}/issues.json", "w") as issuefile:
    json.dump(results, issuefile, indent=2)

#with open("repo_cache.json", "w") as repo_cache:
#    json.dump(features.repo_cache, repo_cache, indent=2)

#with open("user_cache.json", "w") as user_cache:
#    json.dump(features.user_cache, user_cache, indent=2)
