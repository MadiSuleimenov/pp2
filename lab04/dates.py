import datetime

now = datetime.datetime.now()
print(now)          # 2026-02-22 ...
print(now.date())   # 2026-02-22
print(now.time())   # ...


import datetime

d = datetime.date(2026, 2, 22)
print(d)            # 2026-02-22
print(d.weekday())  # 0=Mon ... 6=Sun


import datetime

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d"))       # 2026-02-22
print(now.strftime("%d.%m.%Y %H:%M")) # 22.02.2026 21:...

import datetime

now = datetime.datetime.now()
future = now + datetime.timedelta(days=7, hours=3)
print(future)