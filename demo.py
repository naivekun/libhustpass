from libhustpass import main

ticket = main.doLogin("username", "<REDACTED>", "https://one.hust.edu.cn/dcp/")

# now copy ticket to browser is ok
# or open a new session

import requests

r = requests.session()
ret = r.get(ticket)

# now do whatever you want

print(ret.text)
