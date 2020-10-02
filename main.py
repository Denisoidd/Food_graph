from database import Database
import json

# # Initial graph
# build = [("core", None), ("A", "core"), ("B", "core"), ("C", "core"), ("C1", "C")]
# # Extract
# extract = {"img001": ["A", "B"], "img002": ["A", "C1"], "img003": ["B", "E"]}
# # Graph edits
# edits = [("A1", "A"), ("A2", "A"), ("C2", "C")]

with open('graph_build.json') as f:
    build = json.load(f)

with open('img_extract.json') as f:
    extract = json.load(f)

with open('graph_edits.json') as f:
    edits = json.load(f)

with open('expected_status.json') as f:
    results = json.load(f)

# Get status (this is only an example, test your code as you please as long as it works)
status = {}
if len(build) > 0:
    # Build graph
    db = Database(build[0][0])
    if len(build) > 1:
        db.add_nodes(build[1:])
    # Add extract
    db.add_extract(extract)
    # Graph edits
    db.add_nodes(edits)
    # Update status
    status = db.get_extract_status()
print(status)

# checker on json files
for key in status:
    if status[key] == results[key]:
        print("{}: CORRECT".format(key))
    else:
        print("WRONG, {}".format(key))
        print("My implementation: {}".format(status[key]))
        print("True results: {}".format(results[key]))
