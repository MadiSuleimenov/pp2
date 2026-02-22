import json

s = '{"name":"Ann","age":20,"active":true}'
obj = json.loads(s)
print(obj["name"])  # Ann

import json

data = {"a": 1, "b": 2, "c": [3, 4]}
print(json.dumps(data))                
print(json.dumps(data, indent=2))       


import json

data = {"b": 1, "a": 2}
print(json.dumps(data, separators=(",", ":"), sort_keys=True))  # {"a":2,"b":1}


import json

with open("data.json", "r", encoding="utf-8") as f:
    obj = json.load(f)
print(obj)