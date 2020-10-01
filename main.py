from database import Database
import json

# # Initial graph
# build = [("core", None), ("A", "core"), ("B", "core"), ("C", "core"), ("C1", "C")]
# # Extract
# extract = {"img001": ["A"], "img002": ["C1"]}
# # Graph edits
# edits = [("A1", "A"), ("A2", "A")]

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
    # extract_new = {}
    # extract_new['img17.jpg'] = extract['img17.jpg']
    db.add_extract(extract)
    # Graph edits
    db.add_nodes(edits)
    # Update status
    status = db.get_extract_status()
print(status)

for key in status:
    if status[key] == results[key]:
        print("Yeah")
    else:
        print("Noah, {}".format(key))
        print("Algo: {}".format(status[key]))
        print("True: {}".format(results[key]))
