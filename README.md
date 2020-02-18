## libhustpass

`pass.hust.edu.cn` changed it's login encryption from RSA to **SB** DES

#### Usage

```python
from libhustpass import main

ticket = main.doLogin("username","password","https://one.hust.edu.cn/dcp/")

# now copy ticket to browser is ok
# or open a new session in script

import requests
r=requests.session()
ret = r.get(ticket)

# now do whatever you want

print(ret.text)

```

#### Implementation

`des.js` use a spacial `__pc1` (sbDes.py:270) to generate DES 56 byte key

```python
__pc1 = [56, 48, 40, 32, 24, 16,  8,
        0, 57, 49, 41, 33, 25, 17,
        9,  1, 58, 50, 42, 34, 26,
        18, 10,  2, 59, 51, 43, 35,
        27, 19, 11, 3, 60, 52, 44,
        36, 28, 20, 12, 4, 61, 53,
        45,  37, 29, 21, 13, 5, 62,
        54, 46,  38, 30, 22, 14, 6 
]
```

So I modified pyDes.py from python library `pyDes` to sbDes.py

#### License

WTFPL