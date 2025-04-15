import json
import sys

def should_proceed(plan):
for resource in plan['resource_changes']:
    action = resource['change']['actions']
if 'delete' in action:
    print(f"Resource {resource['address']} is being destroyed. Apply should not proceed.")
return False
if 'update' in action:
    if 'tags' not in resource['change']['before'] or 'tags' not in resource['change']['after']:
print(f"Resource {resource['address']} is being modified in a way other than tags. Apply should not proceed.")
return False
if resource['change']['before']['tags'].get('GitCommitHash') != resource['change']['after']['tags'].get('GitCommitHash'):
    print(f"Resource {resource['address']} is modifying tags other than GitCommitHash. Apply should not proceed.")
return False
if 'create' in action:
    continue
return True

def main():
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_tfplan.json>")
sys.exit(1)

tfplan_path = sys.argv[1]
with open(tfplan_path, 'r') as file:
plan = json.load(file)

if should_proceed(plan):
    print("Apply can proceed.")
else:
print("Apply should not proceed.")

if __name__ == "__main__":
    main()
