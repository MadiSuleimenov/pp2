import re

text = "TOTAL: 1100"
m = re.search(r"TOTAL[:\s]+(\d+)", text)
print(m.group(1) if m else "NOT FOUND")


import re

text = "Date: 2026/02/28"
m = re.search(r"(\d{4})[-/](\d{2})[-/](\d{2})", text)
print(m.group(0) if m else "NOT FOUND")


import re

line = "Milk 2 x 450 = 900"
m = re.search(r"^(.+?)\s+(\d+)\s*x\s*(\d+)\s*=\s*(\d+)$", line)
print(m.groups() if m else "NO MATCH")

import re

text = """Milk 2 x 450 = 900
Bread 1 x 200 = 200
TOTAL: 1100"""

items = re.findall(r"^(.+?)\s+(\d+)\s*x\s*(\d+)\s*=\s*(\d+)$", text, re.M)
print(items)


import re

line = "Chocolate    2   x  350   =   700"
line = re.sub(r"\s+", " ", line).strip()
print(line)