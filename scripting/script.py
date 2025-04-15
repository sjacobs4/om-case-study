import json
import os
import sys

def parse_tfplan(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def should_proceed(plan):
    for resource in plan.get('resource_changes', []):
        action = resource.get('change', {}).get('actions', [])
        if 'create' in action:
            continue  # Allow create actions
        elif 'update' in action:
            # Check if only the tags attribute is being modified
            if 'tags' in resource.get('change', {}).get('after', {}):
                # Check if only GitCommitHash is being modified
                tags_after = resource['change']['after']['tags']
                tags_before = resource['change']['before']['tags']
                
                # Check if only GitCommitHash tag is modified
                if tags_after is not None and 'GitCommitHash' in tags_after:
                    continue  # Allow this modification
                else:
                    print(f"Modification not allowed for resource: {resource['address']}. "
                          f"Only 'GitCommitHash' tag can be modified.")
                    return False
            else:
                print(f"Modification not allowed for resource: {resource['address']}. "
                      f"Only 'tags' attribute can be modified.")
                return False
        elif 'delete' in action:
            print(f"Resource deletion not allowed: {resource['address']}.")
            return False
    return True

def main():
    # Assuming the script is executed in the directory containing the tfplan.json file
    #dirs=os.getcwd(); print(dirs)
    scripted_dir= os.path.dirname(os.path.abspath(__file__))
    os.chdir (scripted_dir)
    print(scripted_dir)
    json_files=[os.path.abspath(file) for file in os.listdir(scripted_dir) if file.lower().endswith(".json")]
    print (json_files)
    for files in json_files:
        plan = parse_tfplan(files)
        print('processing {} file.'.format(files))
        if should_proceed(plan):
            print("The apply can proceed.")
        else:
            print("The apply should not proceed.")

if __name__ == "__main__":
    main()