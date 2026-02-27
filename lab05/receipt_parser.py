from receipt_parser import parse_receipt

text = """MAGNUM
Date: 2026-02-28
Milk 2 x 450 = 900
Bread 1 x 200 = 200
TOTAL: 1100"""

data = parse_receipt(text)
print(data["total"])


from receipt_parser import parse_receipt

text = """SMALL MART
Date: 2026-02-28
Cola 1 x 550 = 550
Chips 2 x 300 = 600
TOTAL: 1150"""

data = parse_receipt(text)
for item in data["items"]:
    print(item["name"], item["qty"], item["price"], item["sum"])
    
    
from receipt_parser import parse_receipt

text = """MARKET
Date: 2026-02-28
Apple 3 x 120 = 360
Water 1 x 250 = 250
"""

data = parse_receipt(text)
calculated = sum(i["sum"] for i in data["items"])
print(calculated)